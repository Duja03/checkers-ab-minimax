from move import EatenInfo, Move
from piece import Color, Piece, Type
from settings import *


class State(object):
    def __init__(self):
        self.tiles = self.test_state()
        self.turn_color = Color.LIGHT

        self.total_lights = 0
        self.light_queens = 0
        self.total_darks = 0
        self.dark_queens = 0

    def initial_state(self):
        matrix = [Piece(Type.EMPTY) for _ in range(COLS * ROWS)]
        for r in range(ROWS):
            for c in range(COLS):
                if 0 <= r <= 2 and (r + c) % 2 == 1:
                    matrix[r * COLS + c].type = Type.BASE
                    matrix[r * COLS + c].color = Color.DARK
                    self.total_darks += 1
                    continue
                if 5 <= r <= 7 and (r + c) % 2 == 1:
                    matrix[r * COLS + c].type = Type.BASE
                    matrix[r * COLS + c].color = Color.LIGHT
                    self.total_lights += 1
                    continue
        return matrix

    def test_state(self):
        matrix = [Piece(Type.EMPTY) for _ in range(COLS * ROWS)]
        matrix[1].type = Type.QUEEN

        matrix[10].type = Type.BASE
        matrix[10].color = Color.DARK

        matrix[12].type = Type.BASE
        matrix[12].color = Color.DARK

        matrix[14].type = Type.BASE
        matrix[14].color = Color.DARK

        matrix[28].type = Type.BASE
        matrix[28].color = Color.DARK

        matrix[30].type = Type.BASE
        matrix[30].color = Color.DARK

        matrix[44].type = Type.BASE
        matrix[44].color = Color.DARK

        matrix[46].type = Type.BASE
        matrix[46].color = Color.DARK

        self.total_lights = 1
        self.light_queens = 1
        self.total_darks = 7
        self.dark_queens = 0

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
        all_moves = set()
        for tile in range(COLS * ROWS):
            piece = self.tiles[tile]
            if piece.empty() or piece.color != self.turn_color:
                continue
            self.generate_moves_for_tile(tile, all_moves)
        return all_moves

    def generate_moves_for_tile(self, org_tile, all_moves: set):
        o_piece = self.tiles[org_tile]
        if o_piece.empty() or o_piece.color != self.turn_color:
            return
        o_row = org_tile // ROWS
        o_col = org_tile % COLS
        o_color = o_piece.color

        srt_vecs = self.get_direction_vectors(o_piece)
        path = set([org_tile])

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
                all_moves.add(Move(org_tile, s_tile))
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
                    eaten = set([EatenInfo(s_tile, s_piece.type, s_piece.color)])
                    all_moves.add(Move(org_tile, l_tile, eaten))
                    self.generate_jumping_moves(
                        org_tile, l_tile, vec, all_moves, eaten, path
                    )

    def get_direction_vectors(self, piece: Piece, dir=(0, 0)):
        # Default (0, 0) means we are not in recursive part:
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
        self, org_tile, current_tile, dir, all_moves: set, eaten: set, path: set
    ):
        path = set(path)
        if current_tile in path:
            return

        path.add(current_tile)
        o_piece = self.tiles[org_tile]

        c_row = current_tile // ROWS
        c_col = current_tile % COLS
        o_color = o_piece.color
        srt_vecs = self.get_direction_vectors(o_piece, dir)

        for vec in srt_vecs:
            dr, dc = vec

            s_row, s_col = c_row + dr, c_col + dc
            if not (0 <= s_row < ROWS) or not (0 <= s_col < COLS):
                continue

            s_tile = s_row * COLS + s_col
            s_piece = self.tiles[s_tile]
            if s_piece.empty() or s_piece.same_color_as(o_color):
                continue

            l_row, l_col = s_row + dr, s_col + dc
            if not (0 <= l_row < ROWS) or not (0 <= l_col < COLS):
                continue

            l_tile = l_row * COLS + l_col
            l_piece = self.tiles[l_tile]
            if l_piece.empty():
                new_eaten = set(eaten)
                new_eaten.add(EatenInfo(s_tile, s_piece.type, s_piece.color))
                all_moves.add(Move(org_tile, l_tile, new_eaten))
                self.generate_jumping_moves(
                    org_tile, l_tile, vec, all_moves, new_eaten, path
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

        for info in move.eaten_tiles:
            self.tiles[info.tile_index].set_empty()
            if info.piece_color == Color.LIGHT:
                if info.piece_type == Type.QUEEN:
                    self.light_queens -= 1
                self.total_lights -= 1
            else:
                if info.piece_type == Type.QUEEN:
                    self.dark_queens -= 1
                self.total_darks -= 1

        self.change_turn_color()
