from schema import *
from game_functions import *


def startup():
    game: Game = Game()
    game.set_quick_start_settings()
    update_ui(game)
    print(" END ")
    print(game)


if __name__ == "__main__":
    startup()
