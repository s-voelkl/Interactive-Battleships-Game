from schema import *
import datetime as dt
import os
import random
import string
from constants import *


def print_log_messages(game: Game, related_player: str):
    for log_message in game.log_messages:
        if not (
            len(log_message.related_players) == 0
            or (related_player in log_message.related_players)
            or game.current_player == ""
        ):
            print("continue!")
            continue

        datetime_formatted: str = (
            str(log_message.time.hour)
            + ":"
            + str(log_message.time.minute)
            + ":"
            + str(log_message.time.second)
        )

        print(datetime_formatted, log_message.text, log_message.related_players)


def update_ui(game: Game):
    clear_console_window()
    print_battleships_map(game)
    print_log_messages(game, game.current_player)


def print_battleships_map(game: Game):
    # find the current player (object)
    current_player: Player = None
    for player in game.ingame_players:
        if player.name == game.current_player:
            current_player = player

    # Initialize the 2D lists with zeros
    own_player_ship_positions = [
        [0 for _ in range(game.total_board_width)]
        for _ in range(game.total_board_height)
    ]
    own_player_ship_hps_rel = [
        [0 for _ in range(game.total_board_width)]
        for _ in range(game.total_board_height)
    ]
    # only show other players ships if they are visible for the current player
    other_player_ship_positions = [
        [0 for _ in range(game.total_board_width)]
        for _ in range(game.total_board_height)
    ]
    other_player_ship_hps_rel = [
        [0 for _ in range(game.total_board_width)]
        for _ in range(game.total_board_height)
    ]

    # get ship positions and hps
    for player in game.ingame_players:
        anon_ship_positions = [
            [0 for _ in range(game.total_board_width)]
            for _ in range(game.total_board_height)
        ]
        anon_ship_hps_rel = [
            [0 for _ in range(game.total_board_width)]
            for _ in range(game.total_board_height)
        ]
        for ship in player.ships:
            # determine if ship is from other player and visible --> continue
            if (player.name != game.current_player) and ship_is_visible(
                current_player.ships, ship
            ):
                print("Ship: ", dir(ship))
                print("Ship from other player is visible -> skip!")
                continue

            # Vertical ship
            if ship.position_start_v == ship.position_end_v:
                lower_pos = min(ship.position_start_h, ship.position_end_h)
                higher_pos = max(ship.position_start_h, ship.position_end_h)
                for h in range(lower_pos, higher_pos + 1):
                    # set position and hp there
                    anon_ship_positions[ship.position_start_v][h] = 1
                    anon_ship_hps_rel[ship.position_start_v][h] = (
                        ship.current_hp / ship.ship_length
                    )

            # Horizontal ship
            elif ship.position_start_h == ship.position_end_h:
                lower_pos = min(ship.position_start_v, ship.position_end_v)
                higher_pos = max(ship.position_start_v, ship.position_end_v)
                for v in range(ship.position_start_v, ship.position_end_v + 1):
                    # set position and hp there
                    anon_ship_positions[v][ship.position_start_h] = 1
                    anon_ship_hps_rel[v][ship.position_start_h] = (
                        ship.current_hp / ship.ship_length
                    )

        # set values to a specific player
        if player.name == game.current_player:
            own_player_ship_positions = anon_ship_positions.copy()
            own_player_ship_hps_rel = anon_ship_hps_rel.copy()
        else:
            other_player_ship_positions = anon_ship_positions.copy()
            other_player_ship_hps_rel = anon_ship_hps_rel.copy()

    # print the map using all of the values.


def ship_is_visible(
    current_players_ships: List[Ship], other_players_ship: Ship
) -> bool:
    # True if the other players ship is still visible (e.g. after an attack?)
    if other_players_ship.remaining_visibility_rounds > 0:
        return True

    # Check if any of the current player's ships are within 2 tiles of the other player's ship
    for cp_ship in current_players_ships:
        # exact positions of other players ship
        op_ship_lower_pos_v = min(
            other_players_ship.position_start_v, other_players_ship.position_end_v
        )
        op_ship_higher_pos_v = max(
            other_players_ship.position_start_v, other_players_ship.position_end_v
        )
        op_ship_lower_pos_h = min(
            other_players_ship.position_start_h, other_players_ship.position_end_h
        )
        op_ship_higher_pos_h = max(
            other_players_ship.position_start_h, other_players_ship.position_end_h
        )

        # exact positions of current players ship
        cp_ship_lower_pos_v = min(cp_ship.position_start_v, cp_ship.position_end_v)
        cp_ship_higher_pos_v = max(cp_ship.position_start_v, cp_ship.position_end_v)
        cp_ship_lower_pos_h = min(cp_ship.position_start_h, cp_ship.position_end_h)
        cp_ship_higher_pos_h = max(cp_ship.position_start_h, cp_ship.position_end_h)

        # go through every possible combination of ship alignment (also suitable for ships with length > 5!)
        # vertical position - op
        for v_op in range(op_ship_lower_pos_v, op_ship_higher_pos_v + 1):
            # horizontal position - op
            for h_op in range(op_ship_lower_pos_h, op_ship_higher_pos_h + 1):

                # vertical position - cp
                for v_cp in range(cp_ship_lower_pos_v, cp_ship_higher_pos_v + 1):
                    # horizontal position - op
                    for h_cp in range(cp_ship_lower_pos_h, cp_ship_higher_pos_h + 1):
                        # get the absolute values (e.g. abs(-2) = 2)
                        if (abs(v_op - v_cp) <= 2) and (abs(h_op - h_cp) <= 2):
                            return True
    return False


def clear_console_window():
    # Clears the console window (cmd) for Linux "clear" and Windows "cls"
    # see SOURCES [1] -->
    os.system("cls" if os.name == "nt" else "clear")
    # --> see SOURCES [1]


def print_map_with_grid(values_map: list, color_map: list = []):
    # TESTING: print_map_with_grid([[random.choice([0, 1]) for _ in range(10)] for _ in range(10)])

    # Output partly generated, see SOURCES [3] -->

    # Print column headers (A to J)
    print(" ", sep=None)
    column_headers = "   ".join(
        string.ascii_uppercase[i] for i in range(len(values_map))
    )
    print("     " + column_headers)  # Print column headers
    print("   " + "----" * len(values_map) + "-")  # Top border

    for i, row in enumerate(values_map):
        # Print row with side borders and row headers (01 to 10)
        print(f"{i+1:02} | " + " | ".join(str(cell) for cell in row) + " |")
        print("   " + ("----" * len(values_map)) + "-")  # Row separator

    # --> partly generated Output until here, see SOURCES [3]


def styled_print(
    text: str,
    rgb_tuple: tuple = (255, 255, 255),
    # bold=False,
    underline=False,
    # thin=False,
    # blink=False,
    # italic=False,
):
    # How ANSI escape sequences work, see SOURCES [6]
    # Partly generated logic, see SOURCES [5] -->
    red_val, green_val, blue_val = rgb_tuple

    # Initialize style code
    style_code = ""

    # Add styles if specified
    # if bold:
    #     style_code += STYLES.BOLD.value
    if underline:
        style_code += STYLES.UNDERLINE.value
    # if thin:
    #     style_code += STYLES.THIN.value
    # if blink:
    #     style_code += STYLES.BLINK.value
    # if italic:
    #     style_code += STYLES.ITALIC.value

    # Print the text with the specified color and styles
    print(f"\033[38;2;{red_val};{green_val};{blue_val}m{style_code}{text}\033[0m")

    # --> partly generated, see SOURCES [5]


def test_colors_and_styling():
    for color in COLORS:
        styled_print(f"Color: {color.name}", color.value)

    styled_print("Style: underline.", underline=True)
