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
        # Jump testing:
        matrix[35].color = Color.DARK
        matrix[35].type = Type.BASE
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

    def get_all_turn_moves(self):
        all_moves = []
        for tile in range(COLS * ROWS):
            piece = self.tiles[tile]
            if piece.empty() or piece.color != self.turn_color:
                continue
            self.generate_moves_for_tile(tile, all_moves)
        return all_moves

    def generate_moves_for_tile(self, tile, all_moves: list):
        # for testing:
        piece = self.tiles[tile]
        if piece.empty() or piece.color != self.turn_color:
            return

        row = tile // ROWS
        col = tile % COLS
        piece_color = piece.color

        forward = -1 if piece_color == Color.LIGHT else 1
        # List of vectors for "short diagonal" in terms of (delta_row, delta_col):
        srt_vecs = [
            (forward, -1),
            (forward, 1),
        ]

        if piece.is_queen():
            srt_vecs.extend([(-forward, -1), (-forward, 1)])

        for vec in srt_vecs:
            drow = vec[0]
            dcol = vec[1]

            srt_row = row + drow
            srt_col = col + dcol
            # Validate short row and col, so they are inside the board:
            if not (0 <= srt_row < ROWS) or not (0 <= srt_col < COLS):
                continue

            srt_tile = srt_row * COLS + srt_col
            srt_piece = self.tiles[srt_tile]
            if srt_piece.empty():
                all_moves.append(Move(tile, srt_tile))
            elif srt_piece.is_opposite_color(piece_color):
                lng_row = srt_row + drow
                lng_col = srt_col + dcol
                # Validate long row and col, so they are inside the board:
                if not (0 <= lng_row < ROWS) or not (0 <= lng_col < COLS):
                    continue

                lng_tile = lng_row * COLS + lng_col
                lng_piece = self.tiles[lng_tile]
                if lng_piece.empty():
                    move = Move(tile, lng_tile)
                    move.add_eaten_tile(srt_tile, srt_piece.type, srt_piece.color)
                    all_moves.append(move)
                    # TODO: Recursively add new potential jumps...

    def do_move(self, move: Move):
        assert (
            self.tiles[move.start_tile].color == self.turn_color
        ), "Move color is not same as turn color!"

        start = move.start_tile
        dest = move.dest_tile

        start_piece = self.tiles[start]
        start_color, start_type = start_piece.color, start_piece.type

        # Updating start and dest tiles:
        self.tiles[start].color = self.tiles[dest].color
        self.tiles[start].type = self.tiles[dest].type
        self.tiles[dest].color = start_color
        self.tiles[dest].type = start_type

        for it in move.eaten_tiles:
            ind, t, c = it
            self.tiles[ind].set_empty()
