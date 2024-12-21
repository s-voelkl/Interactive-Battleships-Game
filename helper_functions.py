from schema import *
from ui import *
import math, random
from typing import Tuple, Dict


def adjust_players_ship_visibilities(player: Player, adjustment: int):
    # Reduce/Add visibility rounds for all ships of a player
    for ship in player.ships:
        ship.remaining_visibility_rounds += adjustment
        if ship.remaining_visibility_rounds < 0:
            ship.remaining_visibility_rounds = 0


def get_ship_by_position(game: Game, position_h: int, position_v: int) -> Ship | None:
    # Function shall return a ship object based on the given position or None

    for player in game.ingame_players:
        for ship in player.ships:
            ship_lower_h = min(ship.position_start_h, ship.position_end_h)
            ship_higher_h = max(ship.position_start_h, ship.position_end_h)
            ship_lower_v = min(ship.position_start_v, ship.position_end_v)
            ship_higher_v = max(ship.position_start_v, ship.position_end_v)

            if (
                ship_lower_h <= position_h <= ship_higher_h
                and ship_lower_v <= position_v <= ship_higher_v
                and ship.current_hp > 0
            ):
                return ship
    return None


def determine_ship_hit(game: Game, attacking_ship: Ship, attacked_ship: Ship) -> bool:
    # Function shall determine if a ship was hit by another ship based on a calculation.

    # get the ship length based probability, so based on the length of the attacked ship.
    #   longer ships can be hit better than shorter ships. used sqrt for a better distribution.
    ship_length_based_probability = math.sqrt(
        (attacked_ship.ship_length / game.avg_ship_length)
    )
    ship_length_based_probability = (
        1 if ship_length_based_probability > 1 else ship_length_based_probability
    )

    # get the minimum relative distance between two ships
    map_diagonal_distance = math.sqrt(
        game.total_board_height**2 + game.total_board_width**2
    )
    min_diagonal_ship_distance, _, _ = get_min_distances_between_ships(
        attacking_ship, attacked_ship
    )
    distance_based_probability = 1 - 0.5 * (
        min_diagonal_ship_distance / map_diagonal_distance
    )
    distance_based_probability = (
        1 if distance_based_probability > 1 else distance_based_probability
    )

    # probability for a health based probability. exponent of 0.7 for less impact of this value on the probability.
    hp_based_probability = math.sqrt(
        (attacking_ship.current_hp / attacking_ship.ship_length)
    )
    hp_based_probability = 1 if hp_based_probability > 1 else hp_based_probability

    probability_hit = (
        ship_length_based_probability
        * distance_based_probability
        * hp_based_probability
    )

    random_number = random.random()

    # debug information
    # print(f"ship_length_based_probability: {ship_length_based_probability}")
    # print(f"distance_based_probability: {distance_based_probability}")
    # print(f"hp_based_probability: {hp_based_probability}")
    # print(f"probability_hit: {probability_hit}")
    # print(f"random_number: {random_number}")

    if random_number <= probability_hit:
        return True
    return False


def determine_hit_damage() -> int:
    critical_hit_probability = 0.05
    random_number = random.random()

    if random_number <= critical_hit_probability:
        return 2
    return 1


def get_min_distances_between_ships(ship1: Ship, ship2: Ship) -> Tuple[float, int, int]:
    """Return the minimum distance between two ships.
    The return values are for diagonal distance (float), vertical distance (int) and horizontal distance (int).

    Args:
        ship1 (Ship): First ship
        ship2 (Ship): Second ship

    Returns:
        Tuple[float, int, int]: Tuple with the values:
            - minimum diagonal distance between the two ships
            - minimum vertical distance between the two ships
            - minimum horizontal distance between the two ships
    """

    # get the min and max values of the ships horizontal and vertical positions
    ship1_lower_h = min(ship1.position_start_h, ship1.position_end_h)
    ship1_higher_h = max(ship1.position_start_h, ship1.position_end_h)
    ship1_lower_v = min(ship1.position_start_v, ship1.position_end_v)
    ship1_higher_v = max(ship1.position_start_v, ship1.position_end_v)

    ship2_lower_h = min(ship2.position_start_h, ship2.position_end_h)
    ship2_higher_h = max(ship2.position_start_h, ship2.position_end_h)
    ship2_lower_v = min(ship2.position_start_v, ship2.position_end_v)
    ship2_higher_v = max(ship2.position_start_v, ship2.position_end_v)

    # get the calculated items into a list of distances
    diagonal_distances: List[float] = []
    vertical_distances: List[int] = []
    horizontal_distances: List[int] = []

    # get all distances and choose the smallest one
    for ship1_h in range(ship1_lower_h, ship1_higher_h + 1):
        for ship1_v in range(ship1_lower_v, ship1_higher_v + 1):
            for ship2_h in range(ship2_lower_h, ship2_higher_h + 1):
                for ship2_v in range(ship2_lower_v, ship2_higher_v + 1):

                    # calculate the diagonal distance using the vector length formula |vector|=sqrt(v1^2+v2^2).
                    diagonal_distances.append(
                        math.sqrt(
                            abs((ship1_h - ship2_h)) ** 2
                            + abs((ship1_v - ship2_v)) ** 2
                        )
                    )

                    vertical_distances.append(abs(ship1_v - ship2_v))
                    horizontal_distances.append(abs(ship1_h - ship2_h))

    result = tuple(
        (
            min(diagonal_distances) if diagonal_distances else 0,
            min(vertical_distances) if vertical_distances else 0,
            min(horizontal_distances) if horizontal_distances else 0,
        )
    )

    return result


def determine_max_ship_movement(ship_length: int) -> int:
    if ship_length < 3:
        result = 3
    elif ship_length == 3:
        result = 2
    else:
        result = 1

    # debug information
    # print(f"ship length: {ship_length},\tdetermine_max_ship_movement: {result}")

    return result


def determine_max_directional_ship_movement(
    game: Game, ship: Ship, max_movement: int
) -> Dict[int, int]:
    """Determines the maximum movement of a ship in each direction (north, east, south, west).

    Args:
        game (Game): Game
        ship (Ship): acting ship
        max_movement (int): the pre-calculated maximum movement of the ship, with another function

    Raises:
        Exception: Exception if the ship is placed diagonally

    Returns:
        Dict[int, int]: Dictionary with the values:
            {[key: direction], [value: max_distance]}
            e.g. Ship can only move vertically and the maximum distance is 3,
            also theres the top border in the way, so the ship can only move 1 field north.
            -> {1: 1, 2: 0, 3: 3, 4: 0}
    """
    # possible directions: ship can only move, where the map is not ending
    # movement is aligned to its own rotation
    # directions: north = 1, east = 2, south = 3, west = 4

    # dict with the values: {[key: direction], [value: max_distance]}
    max_directional_movement: Dict = {direction: 0 for direction in range(1, 5)}

    if ship.position_start_h == ship.position_end_h:
        # vertical movement -> north
        max_north: int = min(ship.position_start_v, ship.position_end_v)
        max_directional_movement[1] = (
            max_north if max_north < max_movement else max_movement
        )

        # vertical movement -> south
        max_south: int = (
            game.total_board_height
            - max(ship.position_start_v, ship.position_end_v)
            - 1
        )
        max_directional_movement[3] = (
            max_south if max_south < max_movement else max_movement
        )

    elif ship.position_start_v == ship.position_end_v:
        # horizontal movement -> east
        max_east: int = (
            game.total_board_width - max(ship.position_start_h, ship.position_end_h) - 1
        )
        max_directional_movement[2] = (
            max_east if max_east < max_movement else max_movement
        )

        # horizontal movement -> west
        max_west: int = min(ship.position_start_h, ship.position_end_h)
        max_directional_movement[4] = (
            max_west if max_west < max_movement else max_movement
        )

    else:
        raise Exception("Internal Error. Ship is placed diagonally.")

    # debug information
    # print("Movement directions, north = 1, east = 2, south = 3, west = 4")
    # print("max north movement:", max_directional_movement[1])
    # print("max east movement:", max_directional_movement[2])
    # print("max south movement:", max_directional_movement[3])
    # print("max west movement:", max_directional_movement[4])

    return max_directional_movement


def determine_if_ship_crash(ship1: Ship, ship2: Ship) -> bool:
    _, delta_h, delta_v = get_min_distances_between_ships(ship1, ship2)

    # 2 ships ram each other if the following conditions are fulfilled:
    # (1) the ships have more than 0 HP
    if ship1.current_hp <= 0 or ship2.current_hp <= 0:
        return False

    # (2a) the vertical and horizontal distances are 0 (not really possible)
    # (2b) one of the distances (v/h) is 0 (same column or row) and the other distance is 1 (next to each other)
    # this can be shortened to: if the sum of the distances is <= 1
    if (delta_h + delta_v) <= 1:
        return True

    # (3) the ships are not crashing in each other if they are only diagonally aligned to each other!
    return False


def act_ship_crashing_damages(acting_ship: Ship, crashed_ship: Ship) -> Tuple[int, int]:
    # check again if ship crash happens
    if not determine_if_ship_crash(acting_ship, crashed_ship):
        return (0, 0)

    dmg_against_acting_ship: int = 0
    dmg_against_crashed_ship: int = 0

    # calculate damage:
    # acting ship gets a bonus, if the other ship is rotated in another direction
    ships_differently_aligned: bool = (
        get_ship_orientation(acting_ship) % 2 != get_ship_orientation(crashed_ship) % 2
    )

    if ships_differently_aligned:
        dmg_against_acting_ship = math.ceil(crashed_ship.current_hp * 0.5)
        dmg_against_crashed_ship = acting_ship.current_hp
    else:
        dmg_against_acting_ship = crashed_ship.current_hp
        dmg_against_crashed_ship = acting_ship.current_hp

    # as the acting ship is moving, it has more velocity than the other (standing) ship -> bonus
    dmg_against_crashed_ship += 1

    # act the damage on the ships
    acting_ship.current_hp -= dmg_against_acting_ship
    crashed_ship.current_hp -= dmg_against_crashed_ship


def get_ship_orientation(ship: Ship) -> int:
    """get the ship orientation and alignment.

    Args:
        ship (Ship): This ship

    Returns:
        int: orientation: north = 1, east = 2, south = 3, west = 4
    """
    # orientation: north = 1, east = 2, south = 3, west = 4

    if ship.position_start_h == ship.position_end_h:
        # vertical aligned
        if ship.position_end_v > ship.position_start_v:
            return 3  # south
        else:
            return 1  # north
    else:
        # horizontal aligned
        if ship.position_end_h > ship.position_start_h:
            return 2  # east
        else:
            return 4  # west
