import math
from enum import Enum

from settings import COLS, ROWS


class StateResult(Enum):
    DRAW = 1
    PLAYING = 2
    LIGHT_WON = 3
    DARK_WON = 4


class Computer(object):
    def __init__(self, time_limit, max_depth):
        self.time_limit = time_limit
        self.max_depth = max_depth
        self.cur_max_depth = 1
        self.best_move = None
        self.cur_best_move = None
        self.max_player = None

    def evaluate_piece(self, state, piece, row, col, stats, is_light=True):
        if piece.is_base():
            stats[0] += 1
        else:
            stats[1] += 1

        if (is_light and row == ROWS - 1) or (not is_light and row == 0):
            stats[2] += 1
            # Back pieces are protected:
            stats[6] += 1
            return

        self.evaluate_positioning(row, col, stats)
        self.evaluate_if_can_be_taken(state, piece, row, col, stats, is_light)
        self.evaluate_protection(state, piece, row, col, stats, is_light)
        self.evaluate_attack(state, piece, row, col, stats, is_light)

    def evaluate_positioning(self, row, col, stats):
        # Check if the piece is in the middle:
        if row == 3 or row == 4:
            # Check for mini box (2x4) in the middle:
            if 2 <= col <= 5:
                stats[3] += 1
            else:
                stats[4] += 1

    def evaluate_if_can_be_taken(self, state, piece, row, col, stats, is_light):
        # Get all nearby pieces and check for direct eating rules,
        # here won't be calculated jumping eating moves:
        if is_light and row > 0 and 0 < col < 7:
            ul = state[(row - 1) * COLS + (col - 1)]
            ur = state[(row - 1) * COLS + (col + 1)]
            dl = state[(row + 1) * COLS + (col - 1)]
            dr = state[(row + 1) * COLS + (col + 1)]

            if (
                (ul.enemy(piece) and dr.empty())
                or (ur.enemy(piece) and dl.empty())
                or (dl.enemy(piece) and dl.is_queen() and ur.empty())
                or (dr.enemy(piece) and dr.is_queen() and ul.empty())
            ):
                stats[5] += 1.5 if piece.is_queen() else 1

        elif not is_light and row < ROWS - 1 and 0 < col < 7:
            ul = state[(row - 1) * COLS + (col - 1)]
            ur = state[(row - 1) * COLS + (col + 1)]
            dl = state[(row + 1) * COLS + (col - 1)]
            dr = state[(row + 1) * COLS + (col + 1)]
            if (
                (dl.enemy(piece) and ur.empty())
                or (dr.enemy(piece) and ul.empty())
                or (ul.enemy(piece) and ul.is_queen() and dr.empty())
                or (ur.enemy(piece) and ur.is_queen() and dl.empty())
            ):
                stats[5] += 1.5 if piece.is_queen() else 1

    def evaluate_protection(self, state, piece, row, col, stats, is_light):
        behind_l = None
        behind_r = None
        if is_light and row < ROWS - 1:
            if col > 0:
                behind_l = state[(row + 1) * COLS + (col - 1)]
            if col < COLS - 1:
                behind_r = state[(row + 1) * COLS + (col + 1)]
        elif not is_light and row > 0:
            if col > 0:
                behind_l = state[(row - 1) * COLS + (col - 1)]
            if col < COLS - 1:
                behind_r = state[(row - 1) * COLS + (col + 1)]

        if behind_l and behind_r:
            if (
                behind_l.friend(piece) or (behind_l.enemy(piece) and behind_l.is_base())
            ) and (
                behind_r.friend(piece) or (behind_r.enemy(piece) and behind_r.is_base())
            ):
                stats[6] += 2 if piece.is_queen() else 1

    def evaluate_attack(self, state, piece, row, col, stats, is_light):
        if piece.is_queen():
            directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        else:
            directions = [(-1, -1), (-1, 1)] if is_light else [(1, -1), (1, 1)]

        for dr, dc in directions:
            rm, cm = row + dr, col + dc
            re, ce = row + 2 * dr, col + 2 * dc

            if 0 <= rm < ROWS and 0 <= cm < COLS and 0 <= re < ROWS and 0 <= ce < COLS:
                mid = state[rm * COLS + cm]
                end = state[re * COLS + ce]

                if mid.enemy(piece) and end.empty():
                    stats[7] += 1.5 if mid.is_queen() else 1

    def heuristic(self, state):
        # Index 0: number of base pieces
        # Index 1: number of queens
        # Index 2: number of pieces in back row
        # Index 3: number of pieces in the middle (2x4) box
        # Index 4: number of pieces in middle 2 rows, but not in the box
        # Index 5: number of pieces that can be taken this turn
        # Index 6: number of pieces that are protected
        # Index 7: number of pieces that can be captured

        light_stats = [0] * 8
        dark_stats = [0] * 8

        for tile in range(COLS * ROWS):
            piece = state[tile]
            if piece.empty():
                continue

            row = tile // ROWS
            col = tile % COLS

            if piece.is_light():
                self.evaluate_piece(state, piece, row, col, light_stats, is_light=True)
            else:
                self.evaluate_piece(state, piece, row, col, dark_stats, is_light=False)

        weights = [5, 7.5, 4, 2.5, 0.5, -3, 2, 2.5]
        score = 0
        for i in range(len(weights)):
            score += weights[i] * (light_stats[i] - dark_stats[i])

        return score
