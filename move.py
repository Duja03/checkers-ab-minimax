from settings import COLS, ROWS


class EatenInfo:
    def __init__(self, tile_index, piece_type, piece_color):
        self.tile_index = tile_index
        self.piece_type = piece_type
        self.piece_color = piece_color

    def __eq__(self, other):
        return (
            self.tile_index == other.tile_index
            and self.piece_type == other.piece_type
            and self.piece_color == other.piece_color
        )

    def __hash__(self):
        return hash((self.tile_index, self.piece_type, self.piece_color))

    def __str__(self):
        row = self.tile_index // ROWS
        col = self.tile_index % COLS
        return f"({row}, {col})"

    def __repr__(self):
        return str(self)


class Move:
    def __init__(
        self,
        start_tile: int,
        dest_tile: int,
        eaten_tiles: set[EatenInfo] = None,
        promoted=False,
    ):
        self.start_tile = start_tile
        self.dest_tile = dest_tile
        self.eaten_tiles = eaten_tiles if eaten_tiles is not None else set()
        self.promoted = promoted

    def __eq__(self, other):
        return (
            self.start_tile == other.start_tile
            and self.dest_tile == other.dest_tile
            and self.eaten_tiles == other.eaten_tiles
            and self.promoted == other.promoted
        )

    def __hash__(self):
        return hash(
            (
                self.start_tile,
                self.dest_tile,
                tuple(sorted(self.eaten_tiles, key=lambda e: e.tile_index)),
                self.promoted,
            )
        )

    def __str__(self):
        s_row = self.start_tile // ROWS
        s_col = self.start_tile % COLS
        d_row = self.dest_tile // ROWS
        d_col = self.dest_tile % COLS

        ans = [f"{{ ({s_row}, {s_col}) -> ({d_row}, {d_col}) njam ["]

        for eaten in self.eaten_tiles:
            ans.append(str(eaten))
        ans.append("]")
        if self.promoted:
            ans.append("promoted")
        ans.append("}")
        return " ".join(ans)

    def __repr__(self):
        return str(self)

    def inverse(self):
        return Move(
            self.dest_tile, self.start_tile, set(self.eaten_tiles), self.promoted
        )

    def set_as_promoted(self):
        self.promoted = True
