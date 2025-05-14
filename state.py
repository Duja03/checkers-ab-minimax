from move import Move
from piece import Color, Piece, Type
from settings import *


class State(object):
    def __init__(self):
        self.tiles = self.initial_state()
        self.turn_color = Color.LIGHT

    def initial_state(self):
        matrix = [Piece(Type.EMPTY) for _ in range(COLS * ROWS)]
        for r in range(ROWS):
            for c in range(COLS):
                if 0 <= r <= 2 and (r + c) % 2 == 1:
                    matrix[r * COLS + c].type = Type.BASE
                    matrix[r * COLS + c].color = Color.DARK
                    continue
                if 5 <= r <= 7 and (r + c) % 2 == 1:
                    matrix[r * COLS + c].type = Type.BASE
                    matrix[r * COLS + c].color = Color.LIGHT
                    continue
        return matrix

    def __str__(self):
        output = []
        for r in range(ROWS):
            row = []
            for c in range(COLS):
                row.append(str(self.tiles[r * COLS + c]))
            row.append("\n")
            output.append(" ".join(row))
        return "".join(output)

    def __repr__(self):
        return str(self)

    def __getitem__(self, tile) -> Piece:
        assert 0 <= tile < ROWS * COLS, "Tile is outside the board!"
        return self.tiles[tile]

    def __setitem__(self, tile, piece):
        raise Exception("Nema setovanja na ovaj nacin, koristi .color i .type!")

    def do_move(self, move: Move):
        assert (
            self.tiles[move.start_tile].color == self.turn_color
        ), "Move color is not same as turn color!"

        # swapping:
        self.tiles[move.start_tile], self.tiles[move.dest_tile] = (
            self.tiles[move.dest_tile],
            self.tiles[move.start_tile],
        )

        for it in move.eaten_tiles:
            ind, t, c = it
            self.tiles[ind].set_empty()
