from move import Move
from state import State

if __name__ == "__main__":
    s = State()
    m = Move(40, 32)
    # m.add_eaten_tile(s, 1)
    # m.add_eaten_tile(s, 3)
    # m.add_eaten_tile(s, 5)
    # m.add_eaten_tile(s, 7)
    s.do_move(m)
    print(s)
