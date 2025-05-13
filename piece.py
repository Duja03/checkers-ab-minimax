class Piece(object):
    EMPTY = 0
    LIGHT_BASE = 1
    DARK_BASE = 2
    LIGHT_QUEEN = 3
    DARK_QUEEN = 4

    def __init__(self, type=EMPTY):
        self.type = type

    def __str__(self):
        return str(self.type)

    def __repr__(self):
        return str(self)

    def is_empty(self):
        return self.type == self.EMPTY

    def is_light(self):
        return not self.is_empty() and (
            self.type == self.LIGHT_BASE or self.type == self.LIGHT_QUEEN
        )

    def is_dark(self):
        return not self.is_empty() and not self.is_light()

    def is_queen(self):
        return not self.is_empty() and (
            self.type == self.LIGHT_QUEEN or self.type == self.DARK_QUEEN
        )

    def promote(self):
        assert not self.is_empty(), "Empty tile can't be promoted!"
        assert not self.is_queen(), "Tile is already a queen, can't be promoted!"
        if self.is_light():
            self.type = self.LIGHT_QUEEN
        else:
            self.type = self.DARK_QUEEN

    def demote(self):
        assert not self.is_empty(), "Empty tile can't be demoted!"
        assert self.is_queen(), "Tile is not a queen, can't be demoted!"
        if self.is_light():
            self.type = self.LIGHT_BASE
        else:
            self.type = self.DARK_BASE
