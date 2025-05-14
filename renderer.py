import pygame

from piece import *
from settings import *


class Renderer(object):
    def __init__(self, window):
        self.window = window

    def draw_tiles(self):
        for tile in range(ROWS * COLS):
            row = tile // ROWS
            col = tile % COLS

            color = LIGHT_TILE_COLOR if (row + col) % 2 == 0 else DARK_TILE_COLOR

            x = col * TILE_SIZE
            y = row * TILE_SIZE
            pygame.draw.rect(self.window, color, (x, y, TILE_SIZE, TILE_SIZE))

    def draw_pieces(self, state):
        for tile in range(ROWS * COLS):
            row = tile // ROWS
            col = tile % COLS

            piece = state[tile]

            if piece.type == Type.EMPTY:
                continue

            color = LIGHT_PIECE_COLOR if piece.is_light() else DARK_PIECE_COLOR
            shadow = LIGHT_PIECE_SHADOW if piece.is_light() else DARK_PIECE_SHADOW

            center_x = (col + 0.5) * TILE_SIZE
            center_y = (row + 0.5) * TILE_SIZE

            pygame.draw.circle(
                self.window,
                shadow,
                (center_x, center_y + PIECE_HEIGHT / 2),
                PIECE_RADIUS,
            )
            pygame.draw.circle(
                self.window,
                color,
                (center_x, center_y - PIECE_HEIGHT / 2),
                PIECE_RADIUS,
            )

            if piece.is_queen():
                pygame.draw.circle(
                    self.window,
                    shadow,
                    (center_x, center_y - PIECE_HEIGHT / 2),
                    QUEEN_RADIUS,
                )
