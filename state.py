from settings import *

class State(object):
    ROWS = 8
    COLS = 8

    def __init__(self):
        self.tiles = self.initial_state()

    def initial_state(self):
        matrix = [[EMPTY for _ in range(self.COLS)] for _ in range(self.ROWS)]
        for r in range(self.ROWS):
            for c in range(self.COLS):
                if 0 <= r <= 2 and (r + c) % 2 == 1:
                    matrix[r][c] = DARK_BASE
                    continue
                if 5 <= r <= 7 and (r + c) % 2 == 1:
                    matrix[r][c] = LIGHT_BASE
                    continue
        return matrix
