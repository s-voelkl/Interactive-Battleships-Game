from schema import *
import datetime as dt


def print_log_messages(game: Game, related_player: str):
    for log_message in game.log_messages:
        if not (
            len(log_message.related_players) == 0
            or (related_player in log_message.related_players)
            or game.current_player == ""
        ):
            print("continue!")
            continue

        datetime_formatted: str = str(log_message.time.time.hour) + ":"
        +str(log_message.time.time.minute) + ":"
        +str(log_message.time.time.second)

        print(datetime_formatted, log_message.text, log_message.related_players)


def update_ui(game: Game):
    print_battleships_map()
    print_log_messages(game, game.current_player)


def print_battleships_map():
    print("print_battleships_map...")
    pass
