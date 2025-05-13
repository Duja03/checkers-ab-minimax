class Piece(object):
    BASE = 1
    QUEEN = 2
    LIGHT = 4
    DARK = 8

    def __init__(self, type=BASE, color=None):
        self.type = type
        self.color = color

    def __str__(self):
        return (
            "0 "
            if self.is_empty()
            else str(
                self.color | self.type,
            ).ljust(2, " ")
        )

    def __repr__(self):
        return str(self)

    def set_empty(self):
        self.color = None

    def is_empty(self):
        return self.color == None

    def is_light(self):
        return not self.is_empty() and self.color == self.LIGHT

    def is_dark(self):
        return not self.is_empty() and self.color == self.DARK

    def is_queen(self):
        return not self.is_empty() and self.type == self.QUEEN

    def is_base(self):
        return not self.is_empty() and self.type == self.BASE

    def promote(self):
        assert self.is_base(), "Tile can't be promoted!"
        self.type = self.QUEEN

    def demote(self):
        assert self.is_queen(), "Tile can't be demoted!"
        self.type = self.BASE
