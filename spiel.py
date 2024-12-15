from schema import *
from game_functions import *
from ui import *
import time


def startup():
    clear_console_window()
    print("Battleships Game is starting...")

    # color and style activation
    os.system("")
    test_colors_and_styling()
    time.sleep(0)
    clear_console_window()

    # start game
    game: Game = Game()
    game.set_quick_start_settings()
    update_ui(game)

    game.debug_display_game_props()


if __name__ == "__main__":
    startup()
