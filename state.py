from move import EatenInfo, Move
from piece import Color, Piece, Type
from utility import *


class State(object):
    def __init__(self):
        self.total_lights = 0
        self.light_queens = 0
        self.total_darks = 0
        self.dark_queens = 0

        self.tiles = self.initial_state()
        self.turn_color = Color.LIGHT

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

    def state_result(self):
        if self.total_lights == 0:
            return StateResult.DARK_WON
        if self.total_darks == 0:
            return StateResult.LIGHT_WON
        if len(self.get_all_turn_moves()) == 0:
            return StateResult.DRAW
        return StateResult.PLAYING

    def is_terminal(self):
        return self.state_result() != StateResult.PLAYING

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

    def atTile(self, tile):
        return self.tiles[tile]

    def at(self, row, col):
        return self.tiles[row * COLS + col]

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

    def generate_moves_for_tile(self, org_tile, all_moves):
        o_piece = self.tiles[org_tile]
        if o_piece.empty() or o_piece.color != self.turn_color:
            return

        o_row = org_tile // ROWS
        o_col = org_tile % COLS

        path = set([org_tile])

        forward = -1 if o_piece.color == Color.LIGHT else 1
        for vec in [(forward, 1), (forward, -1), (-forward, 1), (-forward, -1)]:
            dr, dc = vec
            if o_piece.is_base() and dr == -forward:
                continue

            # Calculate short diagonal coords (forward left, ...):
            s_row, s_col = o_row + dr, o_col + dc
            # Validate so that they are inside the board:
            if not (0 <= s_row < ROWS) or not (0 <= s_col < COLS):
                continue

            s_tile = s_row * COLS + s_col
            s_piece = self.tiles[s_tile]
            # Free space => valid move:
            if s_piece.empty():
                # Check for potential queen promotion:
                promoted = o_piece.is_base() and (
                    (o_piece.color == Color.DARK and s_row == ROWS - 1)
                    or (o_piece.color == Color.LIGHT and s_row == 0)
                )
                all_moves.append(Move(org_tile, s_tile, None, promoted))
            # We can't jump over our pieces:
            elif s_piece.is_opposite_color(o_piece.color):
                # Checking for tile in same direction that is
                # behind the opponent piece:
                l_row, l_col = s_row + dr, s_col + dc
                if not (0 <= l_row < ROWS) or not (0 <= l_col < COLS):
                    continue

                l_tile = l_row * COLS + l_col
                l_piece = self.tiles[l_tile]

                # Free behind enemy => valid eating move:
                if l_piece.empty():
                    eaten = [EatenInfo(s_tile, s_piece.type, s_piece.color)]
                    # Check for potential queen promotion:
                    promoted = o_piece.is_base() and (
                        (o_piece.color == Color.DARK and l_row == ROWS - 1)
                        or (o_piece.color == Color.LIGHT and l_row == 0)
                    )

                    all_moves.append(Move(org_tile, l_tile, tuple(eaten), promoted))
                    self.generate_jumping_moves(
                        org_tile, l_tile, vec, all_moves, eaten, path
                    )

    def generate_jumping_moves(
        self, org_tile, current_tile, dir, all_moves, eaten, path: set
    ):
        path = set(path)
        if current_tile in path:
            return

        path.add(current_tile)
        o_piece = self.tiles[org_tile]
        c_row = current_tile // ROWS
        c_col = current_tile % COLS

        forward = -1 if o_piece.color == Color.LIGHT else 1
        old_dr, old_dc = dir
        for vec in [(forward, 1), (forward, -1), (-forward, 1), (-forward, -1)]:
            dr, dc = vec
            if (dr == -old_dr and dc == -old_dc) or (
                o_piece.is_base() and dr == -forward
            ):
                continue

            s_row, s_col = c_row + dr, c_col + dc
            if not (0 <= s_row < ROWS) or not (0 <= s_col < COLS):
                continue

            s_tile = s_row * COLS + s_col
            s_piece = self.tiles[s_tile]
            if s_piece.empty() or s_piece.same_color_as(o_piece.color):
                continue

            l_row, l_col = s_row + dr, s_col + dc
            if not (0 <= l_row < ROWS) or not (0 <= l_col < COLS):
                continue

            l_tile = l_row * COLS + l_col
            l_piece = self.tiles[l_tile]
            if l_piece.empty():
                new_eaten = list(eaten)
                new_eaten.append(EatenInfo(s_tile, s_piece.type, s_piece.color))
                # Check for potential queen promotion:
                promoted = o_piece.is_base() and (
                    (o_piece.color == Color.DARK and l_row == ROWS - 1)
                    or (o_piece.color == Color.LIGHT and l_row == 0)
                )

                all_moves.append(Move(org_tile, l_tile, tuple(new_eaten), promoted))
                self.generate_jumping_moves(
                    org_tile, l_tile, vec, all_moves, new_eaten, path
                )

    def do_move(self, move: Move):
        start = move.start
        dest = move.dest

        # Remember initial state:
        s_piece = self.tiles[start]
        s_color, s_type = s_piece.color, s_piece.type

        # Updating start and dest tiles:
        self.tiles[start].type = Type.EMPTY
        self.tiles[dest].color = s_color
        self.tiles[dest].type = s_type

        # Promote if possible:
        if move.promoted:
            self.tiles[dest].promote()
            if self.tiles[dest].color == Color.DARK:
                self.dark_queens += 1
            else:
                self.light_queens += 1

        # Removing eaten pieces:
        for info in move.eaten:
            self.tiles[info.tile].eat()
            if info.p_color == Color.LIGHT:
                if info.p_type == Type.QUEEN:
                    self.light_queens -= 1
                self.total_lights -= 1
            else:
                if info.p_type == Type.QUEEN:
                    self.dark_queens -= 1
                self.total_darks -= 1

        self.change_turn_color()

    def undo_move(self, move: Move):
        start = move.dest
        dest = move.start

        # Reviving eaten pieces:
        for info in move.eaten:
            self.tiles[info.tile].color = info.p_color
            self.tiles[info.tile].type = info.p_type

            if info.p_color == Color.LIGHT:
                if info.p_type == Type.QUEEN:
                    self.light_queens += 1
                self.total_lights += 1
            else:
                if info.p_type == Type.QUEEN:
                    self.dark_queens += 1
                self.total_darks += 1

        # Demote if possible:
        if move.promoted:
            self.tiles[start].demote()
            if self.tiles[start].color == Color.DARK:
                self.dark_queens -= 1
            else:
                self.light_queens -= 1

        start_piece = self.tiles[start]
        s_color, s_type = start_piece.color, start_piece.type

        # Updating start and dest tiles:
        self.tiles[start].type = Type.EMPTY
        self.tiles[dest].color = s_color
        self.tiles[dest].type = s_type

        self.change_turn_color()
