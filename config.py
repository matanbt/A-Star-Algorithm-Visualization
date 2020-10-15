import pygame


class CFG:
    """configuration object"""

    # CONSTANTS:
    SQUARE_SIZE_DICT = {
        'SM': 14, 'MD': 20, 'LG': 23, 'XL': 27
    }
    SLEEP_TIME_DICT = {
        'Normal': 0, 'Slow': 0.2, 'Very Slow': 0.5
    }
    ALGORITHM_CHOICE_DICT = {
        'A* Algorithm': False, 'Dijkstra': True
    }

    # SETTINGS VARS (can be modified by user in settings pop-up)
    SQUARE_SIZE = 20  # MD
    WIDTH_BY_GRIDS = 30
    SLEEP_TIME = 0  # Normal
    DIJKSTRA = False
    # SQUARE_SIZE , WIDTH_BY_GRIDS= 17 , 40

    # Derived variables (can be calculated given the above):
    WIDTH = SQUARE_SIZE * WIDTH_BY_GRIDS
    SCREEN = pygame.display.set_mode((WIDTH, WIDTH + 3 * SQUARE_SIZE))

    @staticmethod
    def calc():
        CFG.WIDTH = CFG.SQUARE_SIZE * CFG.WIDTH_BY_GRIDS
        CFG.SCREEN = pygame.display.set_mode((CFG.WIDTH, CFG.WIDTH + 3 * CFG.SQUARE_SIZE))

    @staticmethod
    def setup(square_size, sleep_time, dijkstra):
        CFG.SQUARE_SIZE, CFG.SLEEP_TIME, CFG.DIJKSTRA = square_size, sleep_time, dijkstra
        CFG.calc()


# Colors:
GRID_LINES_COLOR = (224, 224, 224)
BG_COLOR = (255, 255, 255)
BLOCKED_COLOR = (0, 0, 0)
START_COLOR = (54, 210, 30)
END_COLOR = (230, 43, 36)
CHECKING_COLOR = (113, 240, 255)
CHECKED_COLOR = (20, 90, 255)
MARK_PATH_COLOR = (163, 57, 210)  # (54,210,30)#

TEXT_COLOR = (255, 255, 255)
BAR_COLOR = (5, 20, 60)
