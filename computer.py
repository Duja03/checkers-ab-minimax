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
                if piece.is_base():
                    light_stats[0] += 1
                else:
                    light_stats[1] += 1

                if row == ROWS - 1:
                    light_stats[2] += 1
                    light_stats[6] += 1

                if row == 3 or row == 4:
                    if col >= 2 and col <= 5:
                        light_stats[3] += 1
                    else:
                        light_stats[4] += 1

                # Check if piece can be taken this turn:
                if row > 0 and col > 0 and col < 7:
                    ul_piece = state[(row - 1) * COLS + (col - 1)]
                    ur_piece = state[(row - 1) * COLS + (col + 1)]
                    dl_piece = state[(row + 1) * COLS + (col - 1)]
                    dr_piece = state[(row + 1) * COLS + (col + 1)]
                    if (ul_piece.enemy(piece) and dr_piece.empty()) or (
                        ur_piece.enemy(piece) and dl_piece.empty()
                    ):
                        light_stats[5] += 1

                # Check for protected pieces:
                if row < ROWS - 1:
                    if col == 0 or col == 7:
                        light_stats[6] += 1
                    else:
                        # Behind us in both left and right must be our piece
                        # or enemy base piece; queen would still capture us from behind:
                        dl_piece = state[(row + 1) * COLS + (col - 1)]
                        dr_piece = state[(row + 1) * COLS + (col + 1)]
                        if (
                            dl_piece.friend(piece)
                            or (dl_piece.enemy(piece) and dl_piece.is_base())
                        ) and (
                            dr_piece.friend(piece)
                            or (dr_piece.enemy(piece) and dr_piece.is_base())
                        ):
                            # Protected queen is more valuable than base piece:
                            if piece.is_queen():
                                light_stats[6] += 2
                            else:
                                light_stats[6] += 1

                # Check if I can take enemy piece:
                if piece.is_queen():
                    directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
                else:
                    directions = [(-1, -1), (-1, 1)]

                for dr, dc in directions:
                    mid_row = row + dr
                    mid_col = col + dc
                    end_row = row + 2 * dr
                    end_col = col + 2 * dc
                    if (
                        0 <= mid_row < ROWS and 0 <= mid_col < COLS and
                        0 <= end_row < ROWS and 0 <= end_col < COLS
                    ):
                        mid_piece = state[mid_row * COLS + mid_col]
                        end_piece = state[end_row * COLS + end_col]
                        if mid_piece.enemy(piece) and end_piece.empty():
                            # Capturing queen is more valuable:
                            if mid_piece.is_queen():
                                light_stats[7] += 1.5
                            else:
                                light_stats[7] += 1
            else:
                if piece.is_base():
                    dark_stats[0] += 1
                else:
                    dark_stats[1] += 1

                if row == 0:
                    dark_stats[2] += 1
                    dark_stats[6] += 1

                if row == 3 or row == 4:
                    if col >= 2 and col <= 5:
                        dark_stats[3] += 1
                    else:
                        dark_stats[4] += 1

                # Check if piece can be taken this turn:
                if row < ROWS - 1 and col > 0 and col < 7:
                    ul_piece = state[(row - 1) * COLS + (col - 1)]
                    ur_piece = state[(row - 1) * COLS + (col + 1)]
                    dl_piece = state[(row + 1) * COLS + (col - 1)]
                    dr_piece = state[(row + 1) * COLS + (col + 1)]
                    if (dl_piece.enemy(piece) and ur_piece.empty()) or (
                        dr_piece.enemy(piece) and ul_piece.empty()
                    ):
                        dark_stats[5] += 1

                # Check for protected pieces:
                if row > 0:
                    if col == 0 or col == 7:
                        dark_stats[6] += 1
                    else:
                        ul_piece = state[(row - 1) * COLS + (col - 1)]
                        ur_piece = state[(row - 1) * COLS + (col + 1)]
                        if (
                            ul_piece.friend(piece)
                            or (ul_piece.enemy(piece) and ul_piece.is_base())
                        ) and (
                            ur_piece.friend(piece)
                            or (ur_piece.enemy(piece) and ur_piece.is_base())
                        ):
                            if piece.is_queen():
                                dark_stats[6] += 2
                            else:
                                dark_stats[6] += 1
                
                if piece.is_queen():
                    directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
                else:
                    directions = [(1, -1), (1, 1)]

                for dr, dc in directions:
                    mid_row = row + dr
                    mid_col = col + dc
                    end_row = row + 2 * dr
                    end_col = col + 2 * dc
                    if (
                        0 <= mid_row < ROWS and 0 <= mid_col < COLS and
                        0 <= end_row < ROWS and 0 <= end_col < COLS
                    ):
                        mid_piece = state[mid_row * COLS + mid_col]
                        end_piece = state[end_row * COLS + end_col]
                        if mid_piece.enemy(piece) and end_piece.empty():
                            if mid_piece.is_queen():
                                dark_stats[7] += 1.5
                            else:
                                dark_stats[7] += 1

        weights = [5, 7.5, 4, 2.5, 0.5, -3, 2, 2.5]
        score = 0
        for i in range(len(weights)):
            score += weights[i] * (light_stats[i] - dark_stats[i])

        return score
