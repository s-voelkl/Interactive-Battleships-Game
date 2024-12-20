from schema import *
from ui import *
import math, random


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
    distance_based_probability = 1 - 0.5 * (
        get_min_diagonal_distance_between_ships(attacking_ship, attacked_ship)
        / map_diagonal_distance
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


def get_min_diagonal_distance_between_ships(ship1: Ship, ship2: Ship) -> float:

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
    distances: List[float] = []

    # get all distances and choose the smallest one
    for ship1_h in range(ship1_lower_h, ship1_higher_h + 1):
        for ship1_v in range(ship1_lower_v, ship1_higher_v + 1):
            for ship2_h in range(ship2_lower_h, ship2_higher_h + 1):
                for ship2_v in range(ship2_lower_v, ship2_higher_v + 1):
                    # calculate the distance using the vector length formula |vector|=sqrt(v1^2+v2^2).
                    distances.append(
                        math.sqrt(
                            abs((ship1_h - ship2_h)) ** 2
                            + abs((ship1_v - ship2_v)) ** 2
                        )
                    )

    return min(distances) if distances else 0
