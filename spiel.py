from schema import *
from ui import *
import time
from interaction import *


def startup():
    clear_console_window()
    ("Battleships Game is starting...")

    # color and style activation
    os.system("")
    test_colors_and_styling()
    time.sleep(0)
    clear_console_window()

    # start game
    game: Game = Game()
    game.set_quick_start_settings()
    update_ui(game)

    # setup ships
    setup_ship_positions(game)
    update_ui(game)

    game.debug_display_game_props()


if __name__ == "__main__":
    startup()
