from schema import *
from typing import List
import datetime as dt
import os
import string
from constants import *


def print_log_messages(game: Game, related_player: str, max_messages: int = 20):
    for log_message in game.log_messages[-max_messages:]:
        if not (
            len(log_message.related_players) == 0
            or (related_player in log_message.related_players)
            or game.current_player == ""
        ):
            continue

        datetime_formatted: str = (
            f"{log_message.time.hour:02}:{log_message.time.minute:02}:{log_message.time.second:02}"
        )

        styled_print(
            datetime_formatted
            + " "
            + log_message.text
            + " "
            + str(log_message.related_players),
            rgb_tuple=COLORS.GRAY_LOG_MESSAGES.value,
        )


def update_ui(game: Game):
    clear_console_window()
    styled_print(
        f"INTERACTIVE BATTLESHIPS GAME - {game.current_player}\n\n",
        rgb_tuple=COLORS.WATER_MISSED_OFTEN.value,
    )
    print_battleships_map(game)
    styled_print("\nNachrichten:", rgb_tuple=COLORS.GRAY_LOG_MESSAGES.value)
    print_log_messages(game, game.current_player)


def print_battleships_map(game: Game):

    # test. REDO
    # game.ingame_players[0].ships.append(Ship(5, 0, 4, 0, 0))
    # game.ingame_players[0].ships.append(Ship(2, 0, 1, 9, 9))
    # game.ingame_players[1].ships.append(Ship(4, 6, 9, 0, 0))
    # game.ingame_players[1].ships.append(Ship(4, 7, 10, 2, 2))
    # game.ingame_players[1].ships.append(Ship(2, 5, 5, 5, 6))
    # game.ingame_players[1].ships[-1].remaining_visibility_rounds = 2
    # game.ingame_players[0].missed_shots.append((3, 3))
    # game.ingame_players[0].missed_shots.append((5, 5))
    # game.ingame_players[0].missed_shots.append((9, 9))

    # find the current player (object)
    current_player: Player = game.get_current_player_object()

    # Initialize the 2D lists with zeros
    ship_positions_current_player = [
        [0 for _ in range(game.total_board_width)]
        for _ in range(game.total_board_height)
    ]
    ship_hps_current_player = [
        [0 for _ in range(game.total_board_width)]
        for _ in range(game.total_board_height)
    ]
    # only show other players ships if they are visible for the current player
    ship_positions_other_player = [
        [0 for _ in range(game.total_board_width)]
        for _ in range(game.total_board_height)
    ]
    ship_hps_other_player = [
        [0 for _ in range(game.total_board_width)]
        for _ in range(game.total_board_height)
    ]
    missed_shots_current_player = [
        [0 for _ in range(game.total_board_width)]
        for _ in range(game.total_board_height)
    ]

    # get ship positions and hps
    for player in game.ingame_players:
        # yet anonymous
        ship_positions_anon = [
            [0 for _ in range(game.total_board_width)]
            for _ in range(game.total_board_height)
        ]
        ship_hps_anon = [
            [0 for _ in range(game.total_board_width)]
            for _ in range(game.total_board_height)
        ]
        for ship in player.ships:
            # determine if ship is from other player and visible
            if (player.name != game.current_player) and not (
                ship_is_visible(current_player.ships, ship)
            ):
                # testing - REDO
                # print("Ship from other player is not visible -> skip!")
                # print(
                #     f"  Ship infos: Length {ship.ship_length}, Horizontal: {ship.position_start_h} - {ship.position_end_h},"
                #     + f" Vertical: {ship.position_start_v} - {ship.position_end_v}"
                # )
                continue

            # Vertical ship
            if ship.position_start_v == ship.position_end_v:
                lower_pos = min(ship.position_start_h, ship.position_end_h)
                higher_pos = max(ship.position_start_h, ship.position_end_h)

                for h in range(lower_pos, higher_pos + 1):
                    # set position (value = ship lenth) and HP there
                    ship_positions_anon[ship.position_start_v][h] = ship.ship_length
                    ship_hps_anon[ship.position_start_v][h] = (
                        ship.current_hp / ship.ship_length
                    )

            # Horizontal ship
            elif ship.position_start_h == ship.position_end_h:
                lower_pos = min(ship.position_start_v, ship.position_end_v)
                higher_pos = max(ship.position_start_v, ship.position_end_v)

                for v in range(lower_pos, higher_pos + 1):
                    # set position (value = ship lenth) and HP there
                    ship_positions_anon[v][ship.position_start_h] = ship.ship_length
                    ship_hps_anon[v][ship.position_start_h] = (
                        ship.current_hp / ship.ship_length
                    )
            else:
                raise Exception(
                    "Internal Error: Ship is too large or diagonally placed!"
                )

        # set values to a specific player
        if player.name == game.current_player:
            ship_positions_current_player = ship_positions_anon.copy()
            ship_hps_current_player = ship_hps_anon.copy()

            # fill out missed shots of this player:
            for missed_shot in player.missed_shots:
                pos_H, pos_V = missed_shot
                missed_shots_current_player[pos_H][pos_V] += 1

        else:
            ship_positions_other_player = ship_positions_anon.copy()
            ship_hps_other_player = ship_hps_anon.copy()

    # test: REDO
    maps: list[list[list]] = [
        ship_positions_current_player,
        # ship_positions_other_player,
        # missed_shots_current_player,
    ]

    # redo
    # for i, map in enumerate(maps):
    #     print("Map: ", i + 1)
    #     for row in map:
    #         print(row)
    #     print()

    # print the map using all of the values.
    print_map_infos_with_grid(
        ship_positions_current_player,
        ship_positions_other_player,
        ship_hps_current_player,
        ship_hps_other_player,
        missed_shots_current_player,
    )


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


def print_map_infos_with_grid(
    ship_positions_current_player: list,
    ship_positions_other_player: list,
    ship_hps_current_player: list,
    ship_hps_other_player: list,
    missed_shots_current_player: list,
):
    # CHECK if there are conflicts
    # check if horizontal lengths are the same
    if len(ship_positions_current_player) != len(ship_positions_other_player):
        raise Exception(
            "Internal Error: The size of the battlemaps do not align horizontally!"
        )
    # check if the map is larger than 0
    if len(ship_positions_current_player) == 0:
        raise Exception("Internal Error: The horizontal battlemap size is 0!")

    # check if the vertical lengths are the same
    for ship_row in ship_positions_current_player:
        if len(ship_row) != len(ship_row):
            raise Exception(
                "Internal Error: The size of the battlemaps do not align vertically!"
            )
    # check if battlemaps have ships at the same positions
    for i in range(len(ship_positions_current_player)):
        for k in range(len(ship_positions_current_player[i])):
            if (ship_positions_current_player[i][k] != 0) and (
                ship_positions_other_player[i][k] != 0
            ):
                raise Exception(
                    "Internal Error: There are 2 ships at the same position!"
                )

    # get BASIC VALUES
    total_width: int = len(ship_positions_current_player[0])
    total_height: int = len(ship_positions_current_player)

    # PRINT the map
    borders_rgb: tuple = COLORS.GRAY_MAP_BORDER.value
    info_letters_rgb: tuple = COLORS.GRAY_MAP_LETTERS.value

    # Inspired by generated output, see SOURCES [3] -->
    # Column headers (A to Z)
    column_headers = "  ".join(string.ascii_uppercase[i] for i in range(total_width))
    styled_print("      " + column_headers, rgb_tuple=info_letters_rgb)

    # Top border
    styled_print("    " + "---" * total_width + "--", rgb_tuple=borders_rgb)

    for row in range(total_height):
        # # better readability
        # if ((row) % 10 == 0) and total_height > (row + 1) and row != 0:
        #     styled_print("    |" + " " * total_width * 3 + "|", borders_rgb)

        styled_print(f" {row+1:02} |", end="", rgb_tuple=borders_rgb)
        # --> inspired by generated Output until here, see SOURCES [3]

        for col in range(total_width):
            # set foreground color and value for the tile based on the maps
            tile_symbol: str = "."
            tile_rgb_color: tuple

            # case: current player's ship
            if ship_positions_current_player[row][col] != 0:
                __ship_hp_rel: int = ship_hps_current_player[row][col]
                tile_symbol = str(ship_positions_current_player[row][col])

                if __ship_hp_rel <= 0:
                    tile_rgb_color = COLORS.GREEN_DESTROYED.value
                elif __ship_hp_rel > 0 and __ship_hp_rel < 0.25:
                    tile_rgb_color = COLORS.GREEN_CRITICAL_HEALTH.value
                elif __ship_hp_rel >= 0.25 and __ship_hp_rel < 0.50:
                    tile_rgb_color = COLORS.GREEN_LOW_HEALTH.value
                elif __ship_hp_rel >= 0.50 and __ship_hp_rel < 0.75:
                    tile_rgb_color = COLORS.GREEN_MEDIUM_HEALTH.value
                elif __ship_hp_rel >= 0.75 and __ship_hp_rel < 1:
                    tile_rgb_color = COLORS.GREEN_HIGH_HEALTH.value
                else:
                    tile_rgb_color = COLORS.GREEN_FULL_HEALTH.value

            # case: other player's ship
            elif ship_positions_other_player[row][col] != 0:
                __ship_hp_rel: int = ship_hps_other_player[row][col]
                tile_symbol = str(ship_positions_other_player[row][col])

                if __ship_hp_rel <= 0:
                    tile_rgb_color = COLORS.RED_DESTROYED.value
                elif __ship_hp_rel > 0 and __ship_hp_rel < 0.25:
                    tile_rgb_color = COLORS.RED_CRITICAL_HEALTH.value
                elif __ship_hp_rel >= 0.25 and __ship_hp_rel < 0.50:
                    tile_rgb_color = COLORS.RED_LOW_HEALTH.value
                elif __ship_hp_rel >= 0.50 and __ship_hp_rel < 0.75:
                    tile_rgb_color = COLORS.RED_MEDIUM_HEALTH.value
                elif __ship_hp_rel >= 0.75 and __ship_hp_rel < 1:
                    tile_rgb_color = COLORS.RED_HIGH_HEALTH.value
                else:
                    tile_rgb_color = COLORS.RED_FULL_HEALTH.value

            # case: missed attack on the tile
            elif missed_shots_current_player[row][col] != 0:
                __missed_shots: int = missed_shots_current_player[row][col]
                tile_symbol = "x"

                if __missed_shots == 1:
                    tile_rgb_color = COLORS.WATER_MISSED_ONCE.value
                elif __missed_shots == 2:
                    tile_rgb_color = COLORS.WATER_MISSED_TWICE.value
                else:
                    tile_rgb_color = COLORS.WATER_MISSED_OFTEN.value

            # case: no information available (water)
            else:
                tile_symbol = "."
                tile_rgb_color = COLORS.WATER_BASE.value

            styled_print(" " + str(tile_symbol) + " ", rgb_tuple=tile_rgb_color, end="")

        styled_print("|", borders_rgb)
    styled_print("    " + ("---" * total_width) + "--", borders_rgb)


def styled_print(
    text: str,
    rgb_tuple: tuple = (255, 255, 255),
    # bold=False,
    underline=False,
    # thin=False,
    # blink=False,
    # italic=False,
    sep: str | None = " ",
    end: str | None = "\n",
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
    print(
        f"\033[38;2;{red_val};{green_val};{blue_val}m{style_code}{text}\033[0m",
        sep=sep,
        end=end,
    )

    # --> partly generated, see SOURCES [5]


def test_colors_and_styling():
    for color in COLORS:
        styled_print(f"Color: {color.name}", color.value)

    styled_print("Style: underline.", underline=True)
