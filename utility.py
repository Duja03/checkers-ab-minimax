from enum import Enum


class TimeOutException(Exception):
    pass


ROWS = 8
COLS = 8

TILE_SIZE = 71

SCREEN_WIDTH = COLS * TILE_SIZE
SCREEN_HEIGHT = ROWS * TILE_SIZE

PIECE_RADIUS = 0.76 * TILE_SIZE / 2
QUEEN_RADIUS = 8
PIECE_HEIGHT = 0.01 * SCREEN_HEIGHT

LIGHT_PIECE_COLOR = (238, 90, 90)
LIGHT_PIECE_SHADOW = tuple(3 * x / 4 for x in LIGHT_PIECE_COLOR)

DARK_PIECE_COLOR = (87, 74, 74)
DARK_PIECE_SHADOW = tuple(3 * x / 4 for x in DARK_PIECE_COLOR)

DARK_TILE_COLOR = (125, 149, 94)
LIGHT_TILE_COLOR = (238, 238, 212)
ACTIVE_TILE_COLOR = tuple(2 * x / 3 for x in DARK_TILE_COLOR)


class StateResult(Enum):
    DRAW = 1
    PLAYING = 2
    LIGHT_WON = 3
    DARK_WON = 4


class GameState(Enum):
    MAIN_MENU = 1
    PLAYING = 2
    GAME_OVER = 3


class GameMode(Enum):
    PLAYER_VS_PLAYER = 1
    PLAYER_VS_COMPUTER = 2


def get_selected_tile(mouse_pos):
    x, y = mouse_pos
    x //= TILE_SIZE
    y //= TILE_SIZE
    return y * COLS + x
