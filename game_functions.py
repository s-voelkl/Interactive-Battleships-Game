from schema import *
import math

def set_game_settings():
    # set game settings
    game = set_quick_start_settings()

def set_quick_start_settings() -> Game:
    game = Game()
    
    # define board
    game.initial_board_height = 10
    game.initial_board_width = 10
    game.initial_fog_width = 4
    game.total_board_height = game.initial_board_height
    game.total_board_width = game.initial_board_width + game.initial_fog_width
    
    # define ships
    game.max_ship_length = 5
    game.general_ship_infos = [
        GeneralShipInfo(length=5, title="Flugzeugträger", count=1),
        GeneralShipInfo(length=4, title="Kreuzer", count=2),
        GeneralShipInfo(length=3, title="Zerstörer", count=3),
        GeneralShipInfo(length=2, title="U-Boot", count=4),
    ]
    game.total_ships_per_player = 10
    
    # get the average ship length
    avg_counter: int = 0
    for ship_info in game.general_ship_infos:
        avg_counter += ship_info.length * ship_info.count
        
    game.avg_ship_length = avg_counter / game.total_ships_per_player
    
    
    log_info("Quick start setup done!")
    return game


def log_info(info: str):
    print(info)