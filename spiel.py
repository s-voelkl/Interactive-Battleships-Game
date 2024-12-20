from schema import *
from ui import *
import time
from interaction import *
from typing import List, Dict
import sys


def startup():
    clear_console_window()
    print("Battleships Game is starting...")

    # color and style activation
    os.system("")
    test_colors_and_styling()
    time.sleep(0.25)  # redo
    clear_console_window()

    # start game
    game: Game = Game()
    print_game_header(game)
    game.set_quick_start_settings()
    update_ui(game)
    game_loop: bool = True

    # game loop
    while True:
        # setup ships
        setup_ship_positions(game)
        update_ui(game)

        # round loop: check if a player has won and do player turns
        players_won: List[Player] = []
        players_lost: List[Player] = []
        while True:
            for player in game.ingame_players:

                # check if players have won.
                #   dict with dict[player.name] = if_all_own_ships_destroyed
                players_with_all_destroyed_ships: Dict[str, bool] = {}
                for player in game.ingame_players:
                    players_with_all_destroyed_ships[player.name] = (
                        player.count_own_destroyed_ships()
                        == game.total_ships_per_player
                    )

                # check if tie: is a tie if all ships of all players were destroyed
                if all(players_with_all_destroyed_ships.values()):
                    players_won = []
                    players_lost = game.ingame_players
                    break

                # check if one or more but not all players won
                if any(players_with_all_destroyed_ships.values()):
                    for player in game.ingame_players:
                        if players_with_all_destroyed_ships[player.name]:
                            players_lost.append(player)
                        else:
                            players_won.append(player)
                    break

                # do player turns
                take_turn(game)
                update_current_player(game)

            if players_lost or players_won:
                break

        # print game statistics
        game.add_log_message("Das Spiel ist vorbei. Das Ergebnis ist...")
        update_ui(game)
        time.sleep(3)

        # adjust player wins
        for player in players_won:
            player.games_won += 1

        if len(players_won) == 1:
            game.add_log_message(
                f"Der folgende Spieler hat gewonnen: {players_won[0].name}!"
            )
            game.add_log_message(
                f"{players_won[0].name} hatte {game.total_ships_per_player - players_won[0].count_own_destroyed_ships()}"
                + f"/{game.total_ships_per_player} Schiffen."
            )

        elif len(players_won) == len(game.ingame_players) or len(players_lost) == len(
            game.ingame_players
        ):
            game.add_log_message("Das Spiel ist unentschieden! (Wie selten...)")

        else:
            winners_str = ", ".join(player.name for player in players_won)
            losers_str = ", ".join(player.name for player in players_lost)

            game.add_log_message(f"Die folgenden Spieler haben gewonnen: {winners_str}")
            game.add_log_message(f"Die folgenden Spieler haben verloren: {losers_str}")

        update_ui(game)

        # end / restart game with same players
        user_input = input("Spiel beenden? [j/n]: ")

        if user_input.lower() == "j":
            game.add_log_message("Spiel wird beendet...")
            update_ui(game)
            time.sleep(1)
            sys.exit()
            break
        else:
            game.log_messages.clear()
            game.add_log_message("Neues Spiel!")
            update_ui(game)
            time.sleep(1)

        # debug information
        game.debug_display_game_props()


if __name__ == "__main__":
    startup()
