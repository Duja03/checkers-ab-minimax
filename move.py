from piece import Color, Type
from settings import COLS, ROWS


class EatenInfo:
    def __init__(self, tile: int, p_type: Type, p_color: Color):
        self.tile: int = tile
        self.p_type: Type = p_type
        self.p_color: Color = p_color

    def __eq__(self, other):
        return (
            self.tile == other.tile
            and self.p_type == other.p_type
            and self.p_color == other.p_color
        )

    def __hash__(self):
        return hash((self.tile, self.p_type, self.p_color))

    def __str__(self):
        row = self.tile // ROWS
        col = self.tile % COLS
        return f"({row}, {col})"

    def __repr__(self):
        return str(self)


class Move:
    def __init__(
        self,
        start: int,
        dest: int,
        eaten: tuple[EatenInfo] = None,
        promoted=False,
    ):
        self.start = start
        self.dest = dest
        self.eaten = eaten if eaten is not None else tuple()
        self.promoted = promoted

    def __eq__(self, other):
        return (
            self.start == other.start
            and self.dest == other.dest
            and self.eaten == other.eaten
            and self.promoted == other.promoted
        )

    def __hash__(self):
        return hash(
            (
                self.start,
                self.dest,
                self.eaten,
                self.promoted,
            )
        )

    def __str__(self):
        s_row = self.start // ROWS
        s_col = self.start % COLS
        d_row = self.dest // ROWS
        d_col = self.dest % COLS

        ans = [f"{{ ({s_row}, {s_col}) -> ({d_row}, {d_col}) njam ["]

        for eaten in self.eaten:
            ans.append(str(eaten))
        ans.append("]")
        if self.promoted:
            ans.append("promoted")
        ans.append("}")
        return " ".join(ans)

    def __repr__(self):
        return str(self)
