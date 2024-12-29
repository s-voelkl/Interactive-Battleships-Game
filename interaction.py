from schema import *
from constants import *
from ui import *
from helper_functions import *
import time
from typing import Dict


def setup_ship_positions(game: Game):
    game.add_log_message("Aufsetzen der Schiffspositionen.\n ")
    update_ui(game)

    # split map into two pieces. player 1 left, player 2 right
    player_1_min_position_h = 0
    player_1_max_position_h = game.initial_board_width - 1
    player_1_min_position_v = 0
    player_1_max_position_v = game.initial_board_height - 1

    player_2_min_position_h = game.total_board_width - game.initial_board_width
    player_2_max_position_h = game.total_board_width - 1
    player_2_min_position_v = 0
    player_2_max_position_v = game.initial_board_height - 1

    # automatic placement for debugging and testing of the game
    # comment the following line out to disable the automatic placement
    __automatic_ship_position_setup(game)
    game.add_log_message(
        "Info: Automatische Schiffsplatzierung für Testen aktiviert, siehe Skript."
    )

    # manual placement
    # 1st player
    __place_multiple_ships_on_map(
        game,
        player_1_min_position_h,
        player_1_max_position_h,
        player_1_min_position_v,
        player_1_max_position_v,
    )
    update_current_player(game)

    # 2nd player
    __place_multiple_ships_on_map(
        game,
        player_2_min_position_h,
        player_2_max_position_h,
        player_2_min_position_v,
        player_2_max_position_v,
    )
    update_current_player(game)


def update_current_player(game: Game):
    # get the current player by accessing the next player by index
    player_names: List[str] = [player.name for player in game.ingame_players]
    current_player_index = player_names.index(game.current_player)
    # get the next player index by modulo the current index with the length of the player names
    next_player_index = (current_player_index + 1) % len(player_names)

    # set new player
    styled_print(
        f"{player_names[next_player_index]} ist am Zug...\n",
        rgb_tuple=COLORS.LOG_MESSAGES.value,
    )
    game.add_log_message(f"----- {player_names[next_player_index]} ist am Zug -----\n")

    time.sleep(3)
    clear_console_window()
    styled_print(
        f"{player_names[next_player_index]} ist am Zug.",
        rgb_tuple=COLORS.LOG_MESSAGES.value,
    )
    input(
        f"{player_names[next_player_index]}: Bitte ENTER (Return) drücken zum Fortfahren..."
    )

    game.current_player = player_names[next_player_index]

    # automatically reduce the visibility rounds for all ships of the current player
    adjust_players_ship_visibilities(game.get_current_player_object(), -1)
    update_ui(game)


def validate_own_ship_placement(
    game: Game,
    current_player: Player,
    start_position_h,
    end_position_h,
    start_position_v,
    end_position_v,
) -> bool:
    # compare all existing ships with the ship that shall be placed
    # ship to place if valid if all tiles of other ships are >1 tile distanced from it.
    # es = existing ship, cs = current ship (to be placed and validated)
    for es in current_player.ships:
        es_lower_pos_v = min(es.position_start_v, es.position_end_v)
        es_higher_pos_v = max(es.position_start_v, es.position_end_v)
        es_lower_pos_h = min(es.position_start_h, es.position_end_h)
        es_higher_pos_h = max(es.position_start_h, es.position_end_h)

        # exact positions of current players ship
        cs_lower_pos_v = min(start_position_v, end_position_v)
        cs_higher_pos_v = max(start_position_v, end_position_v)
        cs_lower_pos_h = min(start_position_h, end_position_h)
        cs_higher_pos_h = max(start_position_h, end_position_h)

        # go through every possible combination of ship alignments (also suitable for ships with length > 5!)
        # vertical position - op
        for es_vertical_tile in range(es_lower_pos_v, es_higher_pos_v + 1):
            # horizontal position - op
            for es_horizontal_tile in range(es_lower_pos_h, es_higher_pos_h + 1):

                # vertical position - cp
                for cs_vertical_tile in range(cs_lower_pos_v, cs_higher_pos_v + 1):
                    # horizontal position - op
                    for cs_horizontal_tile in range(
                        cs_lower_pos_h, cs_higher_pos_h + 1
                    ):
                        # get the absolute values (e.g. abs(-2) = 2)
                        if (abs(es_vertical_tile - cs_vertical_tile) <= 1) and (
                            abs(es_horizontal_tile - cs_horizontal_tile) <= 1
                        ):
                            return False

    return True


def take_turn(game: Game):
    current_player: Player = game.get_current_player_object()
    valid_input: bool = False
    chosen_ship: Ship = None
    ship_action: int = 0
    reset_ship_selection: bool = True

    while reset_ship_selection:
        styled_print(
            f"Bitte Schiff für Aktion auswählen [sortiert nach Platzierung]",
            rgb_tuple=COLORS.LOG_MESSAGES.value,
        )

        # choose a ship for the turn, by player input
        valid_input: bool = False
        while not valid_input:

            # Selecting a ship for the turn. Must have >0 hp
            # the not anymore existing ships are not displayed but block their original enumerated number in the list.
            #   this helps the user.
            for i, ship in enumerate(current_player.ships):
                if ship.current_hp > 0:
                    styled_print(
                        f" [{i + 1}]\t{ship.ship_length}er Schiff\t mit {ship.current_hp} HP\t bei horizontal {string.ascii_uppercase[ship.position_start_h]}"
                        + f" und vertikal {ship.position_start_v + 1},\tnoch sichtbar für {ship.remaining_visibility_rounds} Runden.",
                        rgb_tuple=COLORS.LOG_MESSAGES.value,
                    )

            try:
                user_input: str = input(
                    f"Eingabe für Schiff [{1} - {game.total_ships_per_player}]: "
                )
                game.add_log_message(
                    f"Eingabe für Schiff: {user_input}",
                    [game.current_player],
                )
                update_ui(game)

                if not user_input.isnumeric():
                    game.add_log_message(
                        "Der Wert muss eine Zahl sein!",
                        [game.current_player],
                    )
                    update_ui(game)
                    valid_input = False
                    continue

                value: int = int(user_input) - 1

                if not (0 <= value <= game.total_ships_per_player - 1):
                    game.add_log_message(
                        f"Der Wert muss zwischen {1} und {game.total_ships_per_player} liegen!",
                        [game.current_player],
                    )
                    update_ui(game)
                    valid_input = False
                    continue

                if current_player.ships[value].current_hp <= 0:
                    game.add_log_message(
                        f"Das gewählte Schiff hat keine HP mehr und kann keine Aktion mehr ausführen!",
                        [game.current_player],
                    )
                    update_ui(game)
                    valid_input = False
                    continue

                chosen_ship: Ship = current_player.ships[value]
                valid_input = True

            except Exception:
                valid_input = False

        game.add_log_message(
            f"{chosen_ship.ship_length}er Schiff [{current_player.ships.index(chosen_ship) + 1}] ausgewählt. ",
            [game.current_player],
        )
        update_ui(game)

        styled_print(
            "Welche Aktion soll ausgeführt werden", rgb_tuple=COLORS.LOG_MESSAGES.value
        )
        styled_print("[1]\tSchießen", rgb_tuple=COLORS.LOG_MESSAGES.value)
        styled_print("[2]\tBewegen", rgb_tuple=COLORS.LOG_MESSAGES.value)
        # styled_print("[3]\tRotieren", rgb_tuple=COLORS.LOG_MESSAGES.value)
        styled_print(
            "[3]\tAnderes Schiff auswählen", rgb_tuple=COLORS.LOG_MESSAGES.value
        )

        # choose an action for the chosen ship
        valid_input = False
        while not valid_input:
            try:
                user_input: str = input(
                    f"Eingabe für Aktion [1 = Schießen, 2 = Bewegen, 3 = Anderes Schiff]: "
                )
                game.add_log_message(
                    f"Eingabe für Aktion: {user_input}",
                    [game.current_player],
                )
                update_ui(game)

                if not user_input.isnumeric():
                    game.add_log_message(
                        "Der Wert muss eine Zahl sein!",
                        [game.current_player],
                    )
                    update_ui(game)
                    valid_input = False
                    continue

                ship_action = int(user_input)

                if not (1 <= ship_action <= 3):
                    game.add_log_message(
                        f"Der Wert muss zwischen 1 und 3 liegen!",
                        [game.current_player],
                    )
                    update_ui(game)
                    valid_input = False
                    continue

                valid_input = True

            except Exception:
                valid_input = False

        if ship_action == 1:
            __attack_with_ship(game, chosen_ship)
        elif ship_action == 2:
            __move_ship(game, chosen_ship)
        # elif ship_action == 3:
        #     __rotate_ship(game, chosen_ship)
        elif ship_action == 3:
            reset_ship_selection = True
            styled_print(
                "Schiffauswahl zurückgesetzt.", rgb_tuple=COLORS.LOG_MESSAGES.value
            )
            continue
        else:
            raise Exception("Interner Fehler: Ungültige Aktion für Schiff ausgewählt.")

        break


def __place_multiple_ships_on_map(
    game: Game, min_position_h, max_position_h, min_position_v, max_position_v
):
    # current player:
    current_player: Player = game.get_current_player_object()

    game.add_log_message(
        "Bitte platziere Deine Schiffe auf der Karte. "
        + "Sie sollten wie folgt positioniert sein: \n"
        + f"- Horizontale Position: {string.ascii_uppercase[min_position_h]} bis {string.ascii_uppercase[max_position_h]}\n"
        + f"- Vertikale Position: {min_position_v + 1} bis {max_position_v + 1}\n"
        + f'(i) Die Eingabe lässt sich mit "reset" zurücksetzen',
        [game.current_player],
    )
    update_ui(game)
    reset_actions: bool = True

    while reset_actions:
        # loop for the same ship lengths
        for ship in game.general_ship_infos:

            # already auto-placed ships from the player
            n_player_ships_with_same_length: int = 0
            for s in current_player.ships:
                if s.ship_length == ship.length:
                    n_player_ships_with_same_length += 1
            reset_actions = False

            # loop for the same ship
            for i in range(ship.count - n_player_ships_with_same_length):
                valid_input: bool = False
                ship_start_position_h: int = 0
                ship_end_position_h: int = 0
                ship_start_position_v: int = 0
                ship_end_position_v: int = 0

                # 1 = north, 2 = east, 3 = south, 4 = west
                ship_rotation: int = 0

                # loop for the current ship
                while not valid_input:

                    game.add_log_message(
                        f"Platziere {i + 1}. {ship.title} mit der Länge {ship.length}:",
                        [game.current_player],
                    )
                    update_ui(game)

                    # Horizontal position (normally A - X)
                    while not valid_input and not reset_actions:
                        try:
                            user_input: str = input(
                                f"Horizontaler Wert [{string.ascii_uppercase[min_position_h]} - "
                                + f"{string.ascii_uppercase[max_position_h]}]: "
                            )
                            game.add_log_message(
                                f"Eingabe horizontale Position: {user_input}",
                                [game.current_player],
                            )
                            update_ui(game)

                            # validate
                            if user_input.lower() == "reset":
                                reset_actions = True
                                break

                            if len(user_input) != 1 or not user_input.isalpha():
                                game.add_log_message(
                                    f"Der horizontale Wert muss ein einzelner Buchstabe sein!",
                                    [game.current_player],
                                )
                                update_ui(game)
                                valid_input = False
                                continue

                            value: int = ord(user_input.upper()) - ord("A")

                            if not (min_position_h <= value <= max_position_h):
                                game.add_log_message(
                                    f"Der horizontale Wert muss zwischen {string.ascii_uppercase[min_position_h]}"
                                    + f" und {string.ascii_uppercase[max_position_h]} liegen!",
                                    [game.current_player],
                                )
                                update_ui(game)
                                valid_input = False
                                continue

                            valid_input = True
                            ship_start_position_h = value

                        except Exception:
                            valid_input = False

                    # Vertical position (0 - 10)
                    valid_input = False
                    while not valid_input and not reset_actions:
                        try:
                            user_input: str = input(
                                f"Vertikaler Wert [{min_position_v + 1} - {max_position_v + 1}]: "
                            )
                            game.add_log_message(
                                f"Eingabe vertikale Position: {user_input}",
                                [game.current_player],
                            )
                            update_ui(game)

                            # validate
                            if user_input.lower() == "reset":
                                reset_actions = True
                                break

                            if not user_input.isnumeric():
                                game.add_log_message(
                                    "Der vertikale Wert muss eine Zahl sein!",
                                    [game.current_player],
                                )
                                update_ui(game)
                                valid_input = False
                                continue

                            value: int = int(user_input) - 1

                            if not (min_position_v <= value <= max_position_v):
                                game.add_log_message(
                                    f"Der vertikale Wert muss zwischen {min_position_v + 1} und {max_position_v + 1} liegen!",
                                    [game.current_player],
                                )
                                update_ui(game)
                                valid_input = False
                                continue

                            valid_input = True
                            ship_start_position_v = value

                        except Exception:
                            valid_input = False

                    # Rotation (1-4)
                    valid_input = False
                    while not valid_input and not reset_actions:
                        try:
                            user_input: str = input(
                                "Rotation Wert [1=Norden, 2=Osten, 3=Süden, 4=Westen]: "
                            )
                            game.add_log_message(
                                f"Eingabe Rotation: {user_input}", [game.current_player]
                            )
                            update_ui(game)

                            # validate
                            if user_input.lower() == "reset":
                                reset_actions = True
                                break

                            if not user_input.isnumeric():
                                game.add_log_message(
                                    "Die Rotation muss eine Zahl sein!",
                                    [game.current_player],
                                )
                                update_ui(game)
                                valid_input = False
                                continue

                            value: int = int(user_input)

                            if not (1 <= value <= 4):
                                game.add_log_message(
                                    f"Der Wert der Rotation muss zwischen 1 (Norden) und 4 (Westen) liegen!",
                                    [game.current_player],
                                )
                                update_ui(game)
                                valid_input = False
                                continue

                            valid_input = True
                            ship_rotation = value

                        except Exception:
                            valid_input = False

                    if reset_actions:
                        current_player.ships = []
                        game.add_log_message(
                            "Alle Eingaben wurden erfolgreich zurückgesetzt!",
                            related_players=[game.current_player],
                        )
                        update_ui(game)
                        break

                    # set ship end positions based on rotation
                    if ship_rotation == 1:  # north
                        ship_end_position_h = ship_start_position_h
                        ship_end_position_v = ship_start_position_v - ship.length + 1
                    elif ship_rotation == 2:  # east
                        ship_end_position_h = ship_start_position_h + ship.length - 1
                        ship_end_position_v = ship_start_position_v
                    elif ship_rotation == 3:  # south
                        ship_end_position_h = ship_start_position_h
                        ship_end_position_v = ship_start_position_v + ship.length - 1
                    else:  # west
                        ship_end_position_h = ship_start_position_h - ship.length + 1
                        ship_end_position_v = ship_start_position_v

                    # validate that the end positions are in the min/max horizontal/vertical positions
                    if not (
                        min_position_h <= ship_end_position_h <= max_position_h
                    ) or not (min_position_v <= ship_end_position_v <= max_position_v):
                        game.add_log_message(
                            f"Die Position des Schiffs {ship.title} ist nicht valide, da es"
                            + " außerhalb der zulässigen Grenzen gesetzt wurde.",
                            [game.current_player],
                        )
                        update_ui(game)
                        valid_input = False
                        continue

                    # check if ship position is valid
                    ship_is_valid: bool = validate_own_ship_placement(
                        game,
                        current_player,
                        ship_start_position_h,
                        ship_end_position_h,
                        ship_start_position_v,
                        ship_end_position_v,
                    )

                    if not ship_is_valid:
                        game.add_log_message(
                            f"Die Position des Schiffs {ship.title} ist nicht valide, da dort"
                            + " eventuell bereits ein anderes Schiff steht. Bitte versuche es erneut.",
                            [game.current_player],
                        )
                        update_ui(game)
                        valid_input = False
                        continue
                    else:
                        game.add_log_message(
                            f'Schiff "{ship.title}" erfolgreich gesetzt!',
                            related_players=[game.current_player],
                        )
                        update_ui(game)

                    # add ship
                    valid_input = True
                    current_player.ships.append(
                        Ship(
                            ship.length,
                            ship_start_position_h,
                            ship_end_position_h,
                            ship_start_position_v,
                            ship_end_position_v,
                        )
                    )
                    update_ui(game)
                if reset_actions:
                    break
            if reset_actions:
                break
        if reset_actions:
            continue


def __rotate_ship(game: Game, ship: Ship):
    # not implemented yet.
    pass


def __move_ship(game: Game, ship: Ship):
    valid_input: bool = False
    movement_direction: int = 0
    movement_distance: int = 0
    max_movement: int = determine_max_ship_movement(ship.ship_length)

    # ask player for the direction and distance of the movement
    # directions: north = 1, east = 2, south = 3, west = 4
    # dict with the values: {[key: direction], [value: max_distance]}
    directions: Dict[int, int] = determine_max_directional_ship_movement(
        game, ship, max_movement
    )
    allowed_directions: list = [key for key, val in directions.items() if val > 0]
    direction_names: Dict[int, str] = {1: "Norden", 2: "Osten", 3: "Süden", 4: "Westen"}

    # skip over user input if only one direction possible
    if len(allowed_directions) == 1:
        movement_direction = allowed_directions[0]
        game.add_log_message(
            f"Einzig mögliche Bewegungsrichtung: {direction_names[movement_direction]} [{movement_direction}]",
            [game.current_player],
        )
        update_ui(game)
        valid_input = True

    # user input for the movement direction
    while not valid_input:
        for key in allowed_directions:
            styled_print(
                f"[{key}] {direction_names[key]}",
                rgb_tuple=COLORS.LOG_MESSAGES.value,
            )
        try:
            user_input: str = input(
                f"Bewegungsrichtung [{', '.join([str(d) for d in allowed_directions])}]: "
            )
            game.add_log_message(
                f"Eingabe Bewegungsrichtung: {user_input}",
                [game.current_player],
            )
            update_ui(game)

            if not user_input.isnumeric():
                game.add_log_message(
                    "Der vertikale Wert muss eine Zahl sein!",
                    [game.current_player],
                )
                update_ui(game)
                valid_input = False
                continue

            movement_direction: int = int(user_input)

            if not (movement_direction in allowed_directions):
                game.add_log_message(
                    f"Die Bewegungsrichtung muss einen dieser Werte haben: {', '.join(allowed_directions)}",
                    [game.current_player],
                )
                update_ui(game)
                valid_input = False
                continue

            valid_input = True

        except Exception:
            valid_input = False

    # user input for the movement distance
    valid_input = False
    if directions[movement_direction] == 1:
        movement_distance = 1
        game.add_log_message(
            f"Einzig mögliche Bewegungsreichweite: {movement_distance}",
            [game.current_player],
        )
        update_ui(game)
        valid_input = True

    while not valid_input:
        try:
            user_input: str = input(
                f"Anzahl der bewegten Felder [1 - {directions[movement_direction]}]: "
            )
            game.add_log_message(
                f"Eingabe bewegte Felder: {user_input}",
                [game.current_player],
            )
            update_ui(game)

            if not user_input.isnumeric():
                game.add_log_message(
                    "Der vertikale Wert muss eine Zahl sein!",
                    [game.current_player],
                )
                update_ui(game)
                valid_input = False
                continue

            movement_distance: int = int(user_input)

            if not (1 <= movement_distance <= directions[movement_direction]):
                game.add_log_message(
                    f"Die Anzahl der bewegten Felder muss zwischen 1 und {directions[movement_direction]} liegen!",
                    [game.current_player],
                )
                update_ui(game)
                valid_input = False
                continue

            valid_input = True
        except Exception:
            valid_input = False

    # move for each tile:
    movement_done: int = 0
    while movement_done < movement_distance:
        # Movement: adjust the positional values
        act_single_ship_movement(game, ship, movement_direction, 1)
        movement_done += 1

        # check if ship crash
        for player in game.ingame_players:
            for other_ship in player.ships:

                # shall not be the acting ship itself
                if other_ship is ship:
                    continue

                if determine_if_ship_crash(ship, other_ship):
                    if ship.remaining_visibility_rounds < 1:
                        ship.remaining_visibility_rounds = 1
                    if other_ship.remaining_visibility_rounds < 1:
                        other_ship.remaining_visibility_rounds = 1

                    ship_hp_before: int = ship.current_hp
                    other_ship_hp_before: int = other_ship.current_hp
                    act_ship_crashing_damages(ship, other_ship)

                    game.add_log_message(
                        f"Crash zwischen zwei Schiffen! "
                        + f"Das bewegte Schiff nahm {abs(ship.current_hp - ship_hp_before)} Schaden, "
                        + f"das gecrashte Schiff {abs(other_ship.current_hp - other_ship_hp_before)} Schaden"
                    )
                    update_ui(game)

                    if other_ship.current_hp <= 0:
                        game.add_log_message(f"Das gecrashte Schiff ist versunken!")
                    update_ui(game)
                    if ship.current_hp <= 0:
                        game.add_log_message(
                            f"Das bewegte Schiff ist versunken und kann sich nicht mehr bewegen!"
                        )
                        update_ui(game)
                        break

        # UI Update
        update_ui(game)
        styled_print(
            f"{ship.ship_length}er Schiff um {movement_done} bewegt...",
            rgb_tuple=COLORS.LOG_MESSAGES.value,
        )
        time.sleep(1.5)


def __attack_with_ship(game: Game, attacking_ship: Ship):
    # Player has attacks based on the current health of the ship.
    attack_count: int = attacking_ship.current_hp

    for i in range(attack_count):
        if attacking_ship.current_hp <= 0:
            game.add_log_message(
                f"Dieses Schiff ist zerstört, der Zug ist beendet.",
                [game.current_player],
            )
            update_ui(game)
            break

        # Attacking
        valid_input: bool = False
        pos_h: int = 0
        pos_v: int = 0

        game.add_log_message(
            f"Angriff {i + 1}/{attack_count} mit diesem Schiff. Bitte Angriffsposition angeben.",
            [game.current_player],
        )
        update_ui(game)

        # Let player enter the horizontal position for the attack
        while not valid_input:
            try:
                user_input: str = input(
                    f"Horizontaler Wert [{string.ascii_uppercase[0]} - "
                    + f"{string.ascii_uppercase[game.total_board_width - 1]}]: "
                )
                game.add_log_message(
                    f"Eingabe horizontaler Wert: {user_input}",
                    [game.current_player],
                )
                update_ui(game)

                if len(user_input) != 1 or not user_input.isalpha():
                    game.add_log_message(
                        f"Der horizontale Wert muss ein einzelner Buchstabe sein!",
                        [game.current_player],
                    )
                    update_ui(game)
                    valid_input = False
                    continue

                pos_h: int = ord(user_input.upper()) - ord("A")

                if not (0 <= pos_h <= game.total_board_width - 1):
                    game.add_log_message(
                        f"Der horizontale Wert muss zwischen {string.ascii_uppercase[0]}"
                        + f" und {string.ascii_uppercase[game.total_board_width]} liegen!",
                        [game.current_player],
                    )
                    update_ui(game)
                    valid_input = False
                    continue

                valid_input = True

            except Exception:
                valid_input = False

        # Let player enter the vertical position for the attack
        valid_input = False
        while not valid_input:
            try:
                user_input: str = input(
                    f"Vertikaler Wert [{1} - {game.total_board_height}]: "
                )
                game.add_log_message(
                    f"Eingabe vertikaler Wert: {user_input}",
                    [game.current_player],
                )
                update_ui(game)

                if not user_input.isnumeric():
                    game.add_log_message(
                        "Der vertikale Wert muss eine Zahl sein!",
                        [game.current_player],
                    )
                    update_ui(game)
                    valid_input = False
                    continue

                pos_v: int = int(user_input) - 1

                if not (0 <= pos_v <= game.total_board_height - 1):
                    game.add_log_message(
                        f"Der vertikale Wert muss zwischen {1} und {game.total_board_height} liegen!",
                        [game.current_player],
                    )
                    update_ui(game)
                    valid_input = False
                    continue

                valid_input = True

            except Exception:
                valid_input = False

        # check if a ship was hit, get damage, update based on consequences
        attacked_ship: Ship | None = get_ship_by_position(game, pos_h, pos_v)
        current_player = game.get_current_player_object()

        if not attacked_ship:
            game.add_log_message(
                f"Wasser bei horizontal {string.ascii_uppercase[pos_h]}"
                + f" und vertikal {pos_v + 1}!",
                [],
            )
            current_player.missed_shots.append((pos_h, pos_v))
        else:
            ship_was_hit: bool = determine_ship_hit(game, attacking_ship, attacked_ship)
            if attacked_ship.remaining_visibility_rounds <= 1:
                attacked_ship.remaining_visibility_rounds = 1

            # damage calculation
            damage_done: int = determine_hit_damage()
            new_ship_hp: int = attacked_ship.current_hp - damage_done
            hit_str = "kritisch" if damage_done > 1 else "einfach"

            # consequences
            if ship_was_hit and new_ship_hp > 0:
                attacked_ship.current_hp = new_ship_hp

                game.add_log_message(
                    f"Das Schiff bei horizontal {string.ascii_uppercase[attacked_ship.position_start_h]}"
                    + f" und vertikal {attacked_ship.position_start_v + 1} wurde {hit_str} getroffen!",
                    [],
                )
            elif ship_was_hit and new_ship_hp <= 0:
                attacked_ship.current_hp = new_ship_hp
                attacked_ship.remaining_visibility_rounds += 1000000

                game.add_log_message(
                    f"Das Schiff bei horizontal {string.ascii_uppercase[attacked_ship.position_start_h]}"
                    + f" und vertikal {attacked_ship.position_start_v + 1} wurde {hit_str} versenkt!",
                    [],
                )
            else:
                game.add_log_message(
                    f"Das Schiff bei horizontal {string.ascii_uppercase[attacked_ship.position_start_h]}"
                    + f" und vertikal {attacked_ship.position_start_v + 1} wurde verfehlt!",
                    [],
                )
        update_ui(game)

    # adjust visibility for the attacking ship.
    attacking_ship.remaining_visibility_rounds += 1


def __automatic_ship_position_setup(game: Game):
    # here is the automatic placement of the ships for a faster testing of the software
    game.ingame_players[0].ships = [
        Ship(5, 0, 4, 0, 0),
        Ship(4, 0, 3, 2, 2),
        Ship(4, 6, 9, 0, 0),
        Ship(3, 5, 5, 9, 7),
        Ship(3, 9, 7, 5, 5),
        Ship(3, 2, 4, 5, 5),  # redo
        Ship(2, 0, 0, 8, 9),  #
        Ship(2, 8, 9, 9, 9),  #
        Ship(2, 7, 8, 2, 2),  #
        Ship(2, 3, 2, 9, 9),  #
    ]
    game.ingame_players[1].ships = [
        Ship(5, 19, 23, 0, 0),
        Ship(4, 18, 21, 2, 2),
        Ship(4, 23, 23, 3, 6),
        Ship(3, 16, 18, 6, 6),
        Ship(3, 19, 21, 9, 9),
        Ship(3, 21, 21, 5, 7),
        Ship(2, 23, 23, 9, 8),
        Ship(2, 14, 14, 1, 0),
        Ship(2, 14, 15, 9, 9),
    ]
