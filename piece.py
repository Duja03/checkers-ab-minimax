from enum import Enum


class Color(Enum):
    LIGHT = 1
    DARK = 2


class Type(Enum):
    EMPTY = 1
    BASE = 2
    QUEEN = 3


class Piece(object):
    def __init__(self, type=Type.EMPTY, color=Color.LIGHT):
        self.type = type
        self.color = color

    def __str__(self):
        if self.type == Type.BASE:
            if self.color == Color.LIGHT:
                return "1 "
            else:
                return "2 "
        elif self.type == Type.QUEEN:
            if self.color == Color.LIGHT:
                return "11"
            else:
                return "22"
        else:
            return "0 "

    def __repr__(self):
        return str(self)

    def set_empty(self):
        self.type = Type.EMPTY

    def empty(self):
        return self.type == Type.EMPTY

    def is_light(self):
        return not self.empty() and self.color == Color.LIGHT

    def is_dark(self):
        return not self.empty() and self.color == Color.DARK

    def is_queen(self):
        return not self.empty() and self.type == Type.QUEEN

    def is_base(self):
        return not self.empty() and self.type == Type.BASE

    def is_opposite_color(self, from_color: Color):
        return self.color != from_color

    def same_color_as(self, other_color: Color):
        return self.color == other_color

    def friend(self, piece):
        return not piece.empty() and self.same_color_as(piece.color)

    def enemy(self, piece):
        return not piece.empty() and self.is_opposite_color(piece.color)

    def promote(self):
        if self.is_queen():
            return
        self.type = Type.QUEEN

    def demote(self):
        if self.is_base():
            return
        self.type = Type.BASE
