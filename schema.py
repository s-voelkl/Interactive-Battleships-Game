from typing import List

class GeneralShipInfo:
    length: int
    title: str
    count: int

class Ship:
    ship_length: int
    # vertical (V) and horizontal (H) position of the ship on the map, 
    # starts at top left with 0/0
    position_start_v: int
    position_start_h: int
    position_end_v: int
    position_end_h: int
    # simplification of the actual positions of the ships. 
    # max HP of a ship == ship_length. 
    current_hp: int
    
class Player:
    name: str = "Player"
    ships: List[Ship] 
    games_won: int = 0
    
class Game:
    # the board height/width that the players can use to place their ships at the beginning
    initial_board_height: int = 10
    initial_board_width: int = 10
    # the calculated total height/width, including 2 * players inital board width [+ inital fog width]
    total_board_height: int = 10
    total_board_width: int = 10
    initial_fog_width: int = 4
    max_ship_length: int = 5
    general_ship_infos: List[GeneralShipInfo]
    total_ships_per_player: int = 10
    avg_ship_length: float
    ingame_players: List[Player]
    current_player: Player
    
    
