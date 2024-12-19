from typing import List
from datetime import datetime


class GeneralShipInfo:
    length: int
    title: str
    count: int

    def __init__(self, length, title, count):
        self.length = length
        self.title = title
        self.count = count


class Ship:
    ship_length: int
    # vertical (V) and horizontal (H) position of the ship on the map,
    # starts at top left with 0/0
    position_start_h: int
    position_end_h: int
    position_start_v: int
    position_end_v: int
    # simplification of the actual positions of the ships.
    # max HP of a ship == ship_length.
    current_hp: int
    # How many rounds the ship is visible after being detected.
    remaining_visibility_rounds: int

    def __init__(
        self,
        ship_length: int,
        position_start_h: int,
        position_end_h: int,
        position_start_v: int,
        position_end_v: int,
        current_hp: int = None,
    ):
        self.ship_length = ship_length
        self.position_start_h = position_start_h
        self.position_end_h = position_end_h
        self.position_start_v = position_start_v
        self.position_end_v = position_end_v
        self.current_hp = ship_length if current_hp is None else current_hp
        self.remaining_visibility_rounds = 0


class Player:
    name: str = "Spieler"
    ships: List[Ship] = []
    # list of already tried positions with tuple-pairs for the horizontal and vertical position
    missed_shots: List[tuple]
    games_won: int = 0

    def __init__(self, name: str):
        self.name = name
        self.games_won = 0
        self.ships = []
        self.missed_shots = []

    def count_own_destroyed_ships(self) -> int:
        destroyed_ships: int = 0

        for ship in self.ships:
            if ship.current_hp <= 0:
                destroyed_ships += 1

        return destroyed_ships


class LogMessage:
    text: str
    time: datetime
    # to which players the log message is being sent. if empty, send it to all players.
    related_players: List[str]

    def __init__(
        self,
        text: str,
        time: datetime = None,
        related_players: List[Player] = [],
    ):
        self.text = text
        self.time = time if time is not None else datetime.now()
        self.related_players = related_players


class Game:
    # the board height/width that the players can use to place their ships at the beginning
    initial_board_height: int = 10
    initial_board_width: int = 10
    # the calculated total height/width, including 2 * players inital board width [+ inital fog width]
    total_board_height: int = 10
    total_board_width: int = 24
    initial_fog_width: int = 4
    max_ship_length: int = 5
    general_ship_infos: List[GeneralShipInfo]
    total_ships_per_player: int = 10
    avg_ship_length: float
    ingame_players: List[Player]
    current_player: str
    log_messages: List[LogMessage]

    def add_log_message(
        self,
        text: str,
        related_players: list[str] = [],
        time: datetime = datetime.now(),
    ):
        self.log_messages.append(
            LogMessage(related_players=related_players, text=text.strip())
        )
        return self

    def set_ingame_players(self, quick_starting: bool = True) -> list[Player]:
        players: List[Player] = []

        # if quick start, then set names to Player 1 and 2
        if quick_starting:
            players.append(Player("Spieler 1"))
            players.append(Player("Spieler 2"))
            self.ingame_players = players

            self.add_log_message("Spieler 1 und Spieler 2 erfolgreich hinzugefügt.")
            return players

        while len(players) < 2:
            player_name: str = ""
            self.add_log_message(
                "Bitte Namen für SpielerIn " + str(len(players) + 1) + " eingeben:"
            )
            player_name = input("Spielername: ").strip()

            if player_name != "" and not any(player_name == p.name for p in players):
                self.add_log_message(
                    'Hinzufügen des Spielers " ' + player_name + '" war erfolgreich.'
                )
                players.append(Player(name=player_name))
            else:
                self.add_log_message(
                    "Der Name darf nicht bereits vergeben oder leer sein. "
                    + "Bitte erneut versuchen!"
                )

        self.ingame_players = players
        return players

    def set_quick_start_settings(self):
        self.log_messages = []

        # define board
        self.initial_board_height = 10
        self.initial_board_width = 10
        self.initial_fog_width = 4
        self.total_board_height = self.initial_board_height
        self.total_board_width = 2 * self.initial_board_width + self.initial_fog_width

        # define ships
        self.max_ship_length = 5
        self.general_ship_infos = [
            GeneralShipInfo(5, "Flugzeugträger", 1),
            GeneralShipInfo(4, "Kreuzer", 2),
            GeneralShipInfo(3, "Zerstörer", 3),
            GeneralShipInfo(2, "U-Boot", 4),
        ]
        self.total_ships_per_player = 10

        # get the average ship length
        avg_counter: int = 0
        for ship_info in self.general_ship_infos:
            avg_counter += ship_info.length * ship_info.count

        self.avg_ship_length = avg_counter / self.total_ships_per_player

        # set ingame players
        self.set_ingame_players()
        self.current_player = (
            self.ingame_players[0].name if self.ingame_players[0] is not None else ""
        )

        self.add_log_message("Game setup done.")

        return self

    def debug_display_game_props(self):
        """Debug method to display all properties of the object game."""

        print("\n\n\nDEBUG INFOS ABOUT THE GAME OBJECT:")

        # SOURCE [2] for this variable "props" and output
        props = [
            f"initial_board_height: {self.initial_board_height}",
            f"initial_board_width: {self.initial_board_width}",
            f"total_board_height: {self.total_board_height}",
            f"total_board_width: {self.total_board_width}",
            f"initial_fog_width: {self.initial_fog_width}",
            f"max_ship_length: {self.max_ship_length}",
            f"total_ships_per_player: {self.total_ships_per_player}",
            f"avg_ship_length: {self.avg_ship_length}",
            f"current_player: {self.current_player} (Player object)",
        ]
        for prop in props:
            print(prop)
        # SOURCE [2] until here.

        print("\ngeneral_ship_infos:")
        for ship in self.general_ship_infos:
            print(ship.count, "x", ship.length, "er (", ship.title, ")")

        print("\ningame_players:")
        for player in self.ingame_players:
            print(player.name, "with ships: ", len(player.ships))
            for ship in player.ships:
                print(
                    "- Ship:",
                    ship.ship_length,
                    "at (H)",
                    ship.position_start_h,
                    "-",
                    ship.position_end_h,
                    "and (V)",
                    ship.position_start_v,
                    "-",
                    ship.position_end_v,
                    "with HP:",
                    ship.current_hp,
                )
            print()

        print()

    def get_current_player_object(self) -> Player:
        if self.current_player == None:
            raise Exception("Internal Error: Current player is not available!")

        for player in self.ingame_players:
            if player.name == self.current_player:
                return player
