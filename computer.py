import math
import time
from copy import deepcopy

from piece import Color
from utility import *


class Computer(object):
    def __init__(self, time_limit_sec, max_depth):
        self.time_limit_sec = time_limit_sec
        self.max_depth = max_depth
        self.cur_max_depth = 1
        self.best_move = None
        self.cur_best_move = None
        self.max_player = None
        self.start_time_point = None

    def iterative_deepening(self, state, use_ab):
        working_state = deepcopy(state)
        max = working_state.turn_color == Color.LIGHT

        self.best_move = None
        self.start_time_point = time.perf_counter()

        for d in range(1, self.max_depth + 1):
            self.cur_max_depth = d
            try:
                if use_ab:
                    self.alphabeta(working_state, -math.inf, math.inf, 0, max)
                else:
                    self.minimax(working_state, 0, max)
                self.best_move = self.cur_best_move
            except TimeOutException:
                break

        print(f"We reached depth {self.cur_max_depth}")
        return self.best_move

    def get_next_best_move(self, state, use_ab=True):
        print("Thinking...")
        best_move = self.iterative_deepening(state, use_ab)
        print(f"Best move is {best_move}")
        return best_move

    # Expect deep copy of a state as initial parameter state:
    def minimax(self, state, depth, max):
        if time.perf_counter() - self.start_time_point > self.time_limit_sec:
            raise TimeOutException()

        if state.is_terminal() or depth >= self.cur_max_depth:
            return self.eval_state(state)

        if max:
            v = -math.inf
            for move in state.get_all_turn_moves():
                state.do_move(move)
                new_v = self.minimax(state, depth + 1, False)
                state.undo_move(move)
                if new_v > v:
                    v = new_v
                    if depth == 0:
                        self.cur_best_move = move
        else:
            v = math.inf
            for move in state.get_all_turn_moves():
                state.do_move(move)
                new_v = self.minimax(state, depth + 1, True)
                state.undo_move(move)
                if new_v < v:
                    v = new_v
                    if depth == 0:
                        self.cur_best_move = move
        return v

    def alphabeta(self, state, alpha, beta, depth, max):
        if time.perf_counter() - self.start_time_point > self.time_limit_sec:
            raise TimeOutException()

        if state.is_terminal() or depth >= self.cur_max_depth:
            return self.eval_state(state)

        if max:
            v = -math.inf
            for move in state.get_all_turn_moves():
                state.do_move(move)
                new_v = self.alphabeta(state, alpha, beta, depth + 1, False)
                state.undo_move(move)
                if new_v > v:
                    v = new_v
                    if depth == 0:
                        self.cur_best_move = move
                if new_v >= beta:
                    return v
                if new_v > alpha:
                    alpha = new_v
        else:
            v = math.inf
            for move in state.get_all_turn_moves():
                state.do_move(move)
                new_v = self.alphabeta(state, alpha, beta, depth + 1, True)
                state.undo_move(move)
                if new_v < v:
                    v = new_v
                    if depth == 0:
                        self.cur_best_move = move
                if new_v <= alpha:
                    return v
                if new_v < beta:
                    beta = new_v
        return v

    def eval_state(self, state):
        result = state.state_result()
        if result == StateResult.LIGHT_WON:
            return math.inf
        elif result == StateResult.DARK_WON:
            return -math.inf
        elif result == StateResult.DRAW:
            return 0
        return self.heuristic(state)

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
            ul = state.at(row - 1, col - 1)
            ur = state.at(row - 1, col + 1)
            dl = state.at(row + 1, col - 1)
            dr = state.at(row + 1, col + 1)

            if (
                (ul.enemy(piece) and dr.empty())
                or (ur.enemy(piece) and dl.empty())
                or (dl.enemy(piece) and dl.is_queen() and ur.empty())
                or (dr.enemy(piece) and dr.is_queen() and ul.empty())
            ):
                stats[5] += 1.5 if piece.is_queen() else 1

        elif not is_light and row < ROWS - 1 and 0 < col < 7:
            ul = state.at(row - 1, col - 1)
            ur = state.at(row - 1, col + 1)
            dl = state.at(row + 1, col - 1)
            dr = state.at(row + 1, col + 1)
            if (
                (dl.enemy(piece) and ur.empty())
                or (dr.enemy(piece) and ul.empty())
                or (ul.enemy(piece) and ul.is_queen() and dr.empty())
                or (ur.enemy(piece) and ur.is_queen() and dl.empty())
            ):
                stats[5] += 1.5 if piece.is_queen() else 1

    def evaluate_protection(self, state, piece, row, col, stats, is_light):
        bl = None
        br = None
        if is_light and row < ROWS - 1:
            if col > 0:
                bl = state.at(row + 1, col - 1)
            if col < COLS - 1:
                br = state.at(row + 1, col + 1)
        elif not is_light and row > 0:
            if col > 0:
                bl = state.at(row - 1, col - 1)
            if col < COLS - 1:
                br = state.at(row - 1, col + 1)

        if bl and br:
            if (bl.friend(piece) or (bl.enemy(piece) and bl.is_base())) and (
                br.friend(piece) or (br.enemy(piece) and br.is_base())
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
                mid = state.at(rm, cm)
                end = state.at(re, ce)

                if mid.enemy(piece) and end.empty():
                    stats[7] += 1.5 if mid.is_queen() else 1

    def heuristic(self, state):
        light_stats = [0] * 8
        dark_stats = [0] * 8

        for tile in range(COLS * ROWS):
            piece = state.atTile(tile)
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
