from settings import COLS, ROWS


class Move(object):
    def __init__(self, start_tile, dest_tile, eaten_tiles: list[tuple] = None):
        self.start_tile = start_tile
        self.dest_tile = dest_tile

        # eaten tile is tuple (tile_ind, piece_type, piece_color):
        self.eaten_tiles = set()
        if eaten_tiles is not None:
            for tile in eaten_tiles:
                self.eaten_tiles.add(tile)

    def __str__(self):
        s_row = self.start_tile // ROWS
        s_col = self.start_tile % COLS
        d_row = self.dest_tile // ROWS
        d_col = self.dest_tile % COLS
        ans = [f"{{({s_row}, {s_col}) -> ({d_row}, {d_col}) njam ["]
        for eaten in self.eaten_tiles:
            row = eaten[0] // ROWS
            col = eaten[0] % COLS
            ans.append(f"({row}, {col})")
        ans.append(f"]}}")
        return " ".join(ans)

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return other.start_tile == self.start_tile and other.dest_tile == self.dest_tile

    def inverse_move(self):
        return Move(self.dest_tile, self.eaten_tiles, self.eaten_tiles)
