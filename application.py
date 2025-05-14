import pygame

from renderer import Renderer
from settings import *
from state import State


class Application(object):
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Checkers!")
        self.running = True
        self.renderer = Renderer(self.window)
        self.state = State()

        self.selected_tile = None
        self.available_moves = []

    def draw_frame(self):
        self.renderer.draw_tiles()
        self.renderer.draw_selected(self.selected_tile)
        self.renderer.draw_pieces(self.state)
        self.renderer.draw_available_moves(self.state, self.available_moves)

    def get_selected_tile(self, mouse_pos):
        x, y = mouse_pos
        x //= TILE_SIZE
        y //= TILE_SIZE
        return y * COLS + x

    def deselect(self):
        self.selected_tile = None
        self.available_moves = []

    def filter_available_moves(self, selected):
        return list(
            filter(
                lambda move: move.dest_tile == selected,
                self.available_moves,
            )
        )

    def handle_user_gameplay(self, event):
        if self.selected_tile is None:
            selected = self.get_selected_tile(event.pos)
            self.selected_tile = selected
            self.state.generate_moves_for_tile(selected, self.available_moves)
            if len(self.available_moves) == 0:
                self.deselect()
        else:
            selected = self.get_selected_tile(event.pos)
            # Try finding the selected move:
            found_moves = self.filter_available_moves(selected)
            # TODO: Give a choice when multiple moves lead to same place...
            if len(found_moves) != 0:
                self.state.do_move(found_moves[0])
                self.state.change_turn_color()
            self.deselect()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Handle window close event
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.handle_user_gameplay(event)
                    # TODO: Add undo mechanism

            self.draw_frame()
            pygame.display.flip()

        pygame.quit()
