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

    def change_turn_color(self):
        if self.turn_color == Color.DARK:
            self.turn_color = Color.LIGHT
        else:
            self.turn_color = Color.DARK

    def get_all_turn_moves(self):
        all_moves = []
        for tile in range(COLS * ROWS):
            piece = self.tiles[tile]
            if piece.empty() or piece.color != self.turn_color:
                continue
            self.generate_moves_for_tile(tile, all_moves)
        return all_moves

    def generate_moves_for_tile(self, original_tile, all_moves: list):
        o_piece = self.tiles[original_tile]
        if o_piece.empty() or o_piece.color != self.turn_color:
            return
        o_row = original_tile // ROWS
        o_col = original_tile % COLS
        o_color = o_piece.color

        srt_vecs = self.get_direction_vectors(o_piece)

        for vec in srt_vecs:
            dr, dc = vec

            # Calculate short diagonal coords (forward left, ...):
            s_row, s_col = o_row + dr, o_col + dc
            # Validate so that they are inside the board:
            if not (0 <= s_row < ROWS) or not (0 <= s_col < COLS):
                continue

            s_tile = s_row * COLS + s_col
            s_piece = self.tiles[s_tile]

            # Free space => valid move:
            if s_piece.empty():
                all_moves.append(Move(original_tile, s_tile))
            # We can't jump over our pieces:
            elif s_piece.is_opposite_color(o_color):
                # Checking for tile in same direction that is
                # behind the opponent piece:
                l_row, l_col = s_row + dr, s_col + dc
                if not (0 <= l_row < ROWS) or not (0 <= l_col < COLS):
                    continue

                l_tile = l_row * COLS + l_col
                l_piece = self.tiles[l_tile]

                # Free behind enemy => valid eating move:
                if l_piece.empty():
                    # Accumulate eaten tiles for potential jumping  moves:
                    eaten = [(s_tile, s_piece.type, s_piece.color)]

                    move = Move(original_tile, l_tile)
                    move.add_eaten_tile(s_tile, s_piece.type, s_piece.color)
                    all_moves.append(move)

                    # Recursively check for multiple jumps in a row:
                    self.generate_jumping_moves(
                        original_tile, l_tile, vec, all_moves, eaten
                    )

    def get_direction_vectors(self, piece: Piece, dir=(0, 0)):
        vecs = []
        dr, dc = dir
        forward = -1 if piece.color == Color.LIGHT else 1
        if not (-dr == forward and -dc == 1):
            vecs.append((forward, 1))
        if not (-dr == forward and -dc == -1):
            vecs.append((forward, -1))

        if piece.is_queen():
            # This time we don't want to include direction that led us
            # to current position, otherwise we will just go back and forth:
            if not (-dr == -forward and -dc == 1):
                vecs.append((-forward, 1))
            if not (-dr == -forward and -dc == -1):
                vecs.append((-forward, -1))

        return vecs

    def generate_jumping_moves(
        self, original_tile, current_tile, dir, all_moves, eaten
    ):
        o_piece = self.tiles[original_tile]

        c_row = current_tile // ROWS
        c_col = current_tile % COLS
        o_color = o_piece.color
        srt_vecs = self.get_direction_vectors(o_piece, dir)

        for vec in srt_vecs:
            dr, dc = vec

            s_row, s_col = c_row + dr, c_col + dc
            # Validate so that they are inside the board:
            if not (0 <= s_row < ROWS) or not (0 <= s_col < COLS):
                continue

            s_tile = s_row * COLS + s_col
            s_piece = self.tiles[s_tile]
            # This time we only continue if current position's
            # short diagonal is occupied by opponent piece:
            if s_piece.empty() or s_piece.same_color_as(o_color):
                continue

            l_row, l_col = s_row + dr, s_col + dc
            if not (0 <= l_row < ROWS) or not (0 <= l_col < COLS):
                continue

            l_tile = l_row * COLS + l_col
            l_piece = self.tiles[l_tile]
            # Again, free behind enemy => valid eating move, and go again:
            if l_piece.empty():
                eaten.append((s_tile, s_piece.type, s_piece.color))
                move = Move(original_tile, l_tile)
                for e in eaten:
                    ti, tp, cl = e
                    move.add_eaten_tile(ti, tp, cl)
                all_moves.append(move)

                self.generate_jumping_moves(
                    original_tile, l_tile, vec, all_moves, eaten
                )

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

        # Check for potential queen promotion:
        row = dest // ROWS
        dest_piece = self.tiles[dest]
        if (dest_piece.color == Color.DARK and row == COLS - 1) or (
            dest_piece.color == Color.LIGHT and row == 0
        ):
            self.tiles[dest].promote()

        for it in move.eaten_tiles:
            ind, t, c = it
            self.tiles[ind].set_empty()

        self.change_turn_color()
