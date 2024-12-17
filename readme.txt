START: python3 spiel.py


INFORMATION:
Version: 3.11.9 64-bit
IDE: VS Code
Test Environment: VS Code Console, CMD (Windows Command Prompt)
Sources: See "SOURCES" below.

Note: I have some prior knowledge, so some code samples are obviously without a source, 
    even though the topic hasn't been done in lecture.


IN CASE OF BUGS:
- ...



TODO:
- Runden schreiben
* Bewegen nach vorne/hinten (+ Validierung)
* drehen um die Achse (+ Validierung, selbe, wie Bewegung)
* Angreifen mit Schiff auf Feld (inkl. Trefferwahrscheinlichkeit, Anzahl der Schüsse, HP-Anpassung, Sichtanpassung)

- evtl. Zusatz:
* Rammen
* Kritische Treffer (+Wahrscheinlichkeit)
* Erneutes Aufklärungsschüsse.


SOURCES:
[1]: Clear CMD: stackoverflow.com/questions/517970/how-can-i-clear-the-interpreter-console

[2]: Generated Variable, using BingChat
    PROMPT:
    Ich möchte folgende Properties der Klasse nacheinander ausgegeben haben. zB: 
    "initial_board_width: 10"

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

    ANSWER:
    [wiederholter Code]
        properties = [
            f"initial_board_height: {self.initial_board_height}",
            f"initial_board_width: {self.initial_board_width}",
            f"total_board_height: {self.total_board_height}",
            f"total_board_width: {self.total_board_width}",
            f"initial_fog_width: {self.initial_fog_width}",
            f"max_ship_length: {self.max_ship_length}",
            f"total_ships_per_player: {self.total_ships_per_player}",
            f"avg_ship_length: {self.avg_ship_length}",
            f"current_player: {self.current_player}"
        ]
        for prop in properties:
            print(prop)
    [wiederholter Code]

[3]: print_map_with_grid - partly generated with BingChat
    PROMPT:
    Hello. I want to output a formatted Python Battleships map. 
    The map is 10 x 10 big and has values of 0 or 1.
    There should be vertical and horizontal lines.
    The column headers should have values between A and Z, format these as one digit long.
    The row headers should have the values 1, 2, 3, ... 12, and so on. format these numbers as two digits long.
    The values of the map should be seperated by lines from each other.

    ANSWER:
    [...]
    def print_map_with_grid(map):
    # Print column headers (A to J)
    column_headers = " ".join(string.ascii_uppercase[i] for i in range(10))
    print("   " + column_headers)  # Print column headers
    print("  +" + "---" * 10 + "+")  # Top border
    
    for i, row in enumerate(map):
        # Print row with side borders and row headers (01 to 10)
        print(f"{i+1:02}| " + " | ".join(str(cell) for cell in row) + " |")
        print("  +" + "---" * 10 + "+")  # Row separator
    [...]

[5]: styled_print - partly generated with BingChat
    PROMPT:
    Write a Python function styled_print that prints text with customizable styles and 
    RGB colors using ANSI escape codes. Parameters: text (str), rgb_tuple (tuple), bold (bool), 
    underline (bool), thin (bool), blink (bool), italic (bool). Ensure text color resets after printing.

    ANSWER:
    [...]
    def styled_print(text, rgb_tuple, bold=False, underline=False, thin=False, blink=False, italic=False):
        # ANSI escape code for RGB color
        color_code = f"\033[38;2;{rgb_tuple[0]};{rgb_tuple[1]};{rgb_tuple[2]}m"
        # ANSI escape codes for styles
        styles = []
        if bold:
            styles.append("\033[1m")
        if underline:
            styles.append("\033[4m")
        if thin:
            styles.append("\033[2m")
        if blink:
            styles.append("\033[5m")
        if italic:
            styles.append("\033[3m")
        # Combine all styles and color code
        style_code = ''.join(styles)
        # Print the styled text
        print(f"{color_code}{style_code}{text}\033[0m")

    # Example usage
    styled_print("Hello, World!", (255, 0, 0), bold=True, underline=True)

[5]: Overview about ANSI escape sequences: stackoverflow.com/questions/4842424/list-of-ansi-color-escape-sequences

[6]: Colors and Styles were adjusted together with Bing Chat in multiple prompts.
    PROMPTS:
    - Generation of green, red, blue and gray rgb colors.
    - Changes of colors (steps smaller/bigger, darker, lighter, mixes with other colors)
    - rename of the colors to the health-levels (from 0 to 100%, translated into relative health)
    ANSWER: 
    see constants -> COLORS and STYLES