from piece import Piece
from settings import *


class State(object):
    def __init__(self):
        self.tiles = self.initial_state()

    def initial_state(self):
        matrix = [Piece() for _ in range(COLS * ROWS)]
        for r in range(ROWS):
            for c in range(COLS):
                if 0 <= r <= 2 and (r + c) % 2 == 1:
                    matrix[r * COLS + c].type = Piece.DARK_BASE
                    continue
                if 5 <= r <= 7 and (r + c) % 2 == 1:
                    matrix[r * COLS + c].type = Piece.LIGHT_BASE
                    continue
        return matrix

    def __getitem__(self, tile) -> Piece:
        assert 0 <= tile <= ROWS * COLS, "Tile is outside the board!"
        return self.tiles[tile]

    def __setitem__(self, tile, piece):
        assert 0 <= tile <= ROWS * COLS, "Tile is outside the board!"
        assert (
            piece == Piece.EMPTY
            or piece == Piece.LIGHT_BASE
            or piece == Piece.LIGHT_QUEEN
            or piece == Piece.DARK_BASE
            or piece == Piece.DARK_QUEEN
        )
        self.tiles[tile] = piece
