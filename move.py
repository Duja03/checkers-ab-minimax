from settings import COLS, ROWS


class Move(object):
    def __init__(self, start_tile, dest_tile, eaten_tiles=None):
        self.start_tile = start_tile
        self.dest_tile = dest_tile

        # eaten tile is tuple (tile_ind, piece_type, piece_color):
        self.eaten_tiles = set() if eaten_tiles is None else eaten_tiles

    def __str__(self):
        return f"{{{self.start_tile} -> {self.dest_tile} [{self.eaten_tiles}]}}"

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return other.start_tile == self.start_tile and other.dest_tile == self.dest_tile

    def add_eaten_tile(self, tile, type, color):
        assert 0 <= tile <= ROWS * COLS, "Eaten tile is outside the board!"
        self.eaten_tiles.add((tile, type, color))

    def inverse_move(self):
        return Move(self.dest_tile, self.eaten_tiles, self.eaten_tiles)
