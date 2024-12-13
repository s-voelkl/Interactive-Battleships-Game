from enum import Enum


from enum import Enum


class COLORS(Enum):
    # Dark Green to Light Green
    GREEN0 = (0, 100, 0)
    GREEN1 = (0, 125, 0)
    GREEN2 = (0, 150, 0)
    GREEN3 = (0, 175, 0)
    GREEN4 = (0, 200, 0)
    GREEN5 = (0, 225, 0)
    GREEN6 = (0, 250, 0)
    GREEN7 = (50, 255, 50)
    GREEN8 = (100, 255, 100)
    GREEN9 = (150, 255, 150)

    # Strong/Dark Red to Orange/Yellow
    RED0 = (255, 0, 0)
    RED1 = (255, 25, 0)
    RED2 = (255, 50, 0)
    RED3 = (255, 75, 0)
    RED4 = (255, 100, 0)
    RED5 = (255, 125, 0)
    RED6 = (255, 150, 0)
    RED7 = (255, 175, 0)
    RED8 = (255, 200, 0)
    RED9 = (255, 225, 0)

    # Dark Blue to Light Blue
    BLUE0 = (0, 0, 255)
    BLUE1 = (20, 20, 255)
    BLUE2 = (40, 40, 255)
    BLUE3 = (60, 60, 255)
    BLUE4 = (80, 80, 255)
    BLUE5 = (100, 100, 255)
    BLUE6 = (120, 120, 255)
    BLUE7 = (140, 140, 255)
    BLUE8 = (160, 160, 255)
    BLUE9 = (180, 180, 255)

    # White to Dark Gray
    GRAY0 = (255, 255, 255)
    GRAY1 = (240, 240, 240)
    GRAY2 = (225, 225, 225)
    GRAY3 = (210, 210, 210)
    GRAY4 = (195, 195, 195)
    GRAY5 = (180, 180, 180)
    GRAY6 = (165, 165, 165)
    GRAY7 = (150, 150, 150)
    GRAY8 = (135, 135, 135)
    GRAY9 = (120, 120, 120)


class STYLES(Enum):
    # some are not working in CMD :(
    # BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    # THIN = "\033[2m"
    # BLINK = "\033[5m"
    # ITALIC = "\033[3m"
