from typing import List
import datetime as dt


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
    position_start_v: int
    position_start_h: int
    position_end_v: int
    position_end_h: int
    # simplification of the actual positions of the ships.
    # max HP of a ship == ship_length.
    current_hp: int


class Player:
    name: str = "Spieler"
    ships: List[Ship] = []
    games_won: int = 0

    def __init__(self, name: str):
        self.name = name
        self.games_won = 0
        self.ships = []


class LogMessage:
    text: str
    time: dt
    # to which players the log message is being sent. if empty, send it to all players.
    related_players: List[str]

    def __init__(
        self,
        text: str,
        related_players: List[Player] = [],
        time=dt.datetime.now(),
    ):
        self.related_players = related_players
        self.text = text
        self.time = time


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
    current_player: str
    log_messages: List[LogMessage]

    def add_log_message(
        self, text: str, related_players: list[str] = [], time: dt = dt.datetime.now()
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
        self.total_board_width = self.initial_board_width + self.initial_fog_width

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
        self.current_player = self.ingame_players[0]

        self.add_log_message("Game setup done.")

        return self
