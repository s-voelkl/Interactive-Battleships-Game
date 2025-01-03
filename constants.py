from enum import Enum


# Colors and Styles adjusted in coorporation with Bing Chat, see SOURCES [6] -->
class COLORS(Enum):
    # GREEN HEALTH
    GREEN_FULL_HEALTH = (0, 150, 0)  # Full health (100%)
    GREEN_HIGH_HEALTH = (50, 180, 50)  # High health (>75%)
    GREEN_MEDIUM_HEALTH = (85, 205, 85)  # Medium health (>50%)
    GREEN_LOW_HEALTH = (130, 230, 130)  # Low health (<50%)
    GREEN_CRITICAL_HEALTH = (170, 255, 170)  # Critical health (<25%)
    GREEN_DESTROYED = (105, 130, 105)  # Destroyed (0%)

    # RED HEALTH
    RED_FULL_HEALTH = (255, 190, 0)  # Full health (100%)
    RED_HIGH_HEALTH = (255, 150, 0)  # High health (>75%)
    RED_MEDIUM_HEALTH = (255, 110, 0)  # Medium health (>50%)
    RED_LOW_HEALTH = (255, 70, 0)  # Low health (<50%)
    RED_CRITICAL_HEALTH = (255, 30, 0)  # Critical health (<25%)
    RED_DESTROYED = (125, 100, 100)  # Destroyed (0%)

    # -------------

    # WATER / MISSED
    WATER_BASE = (180, 180, 255)
    WATER_MISSED_ONCE = (80, 80, 255)
    WATER_MISSED_TWICE = (60, 60, 255)
    WATER_MISSED_OFTEN = (40, 40, 255)

    # BORDERS
    MAP_BORDER = (180, 180, 180)
    MAP_LETTERS = (210, 210, 210)

    # MESSAGES, GAME HEADER
    LOG_MESSAGES = (210, 210, 210)
    GAME_INFO = (40, 40, 255)


class STYLES(Enum):
    # some are not working in CMD :(
    # BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    # THIN = "\033[2m"
    # BLINK = "\033[5m"
    # ITALIC = "\033[3m"


# --> Colors and Styles adjusted in coorporation with Bing Chat, see SOURCES [6]
