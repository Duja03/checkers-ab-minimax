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

        print(self.state)

    def draw_frame(self):
        self.renderer.draw_tiles()
        self.renderer.draw_pieces(self.state)

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Handle window close event
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    """selected_tile = self._get_selected_tile(event.pos)

                    if event.button == 1:
                        self._handle_piece_selection(selected_tile)
                    elif event.button == 3:
                        if len(self._move_stack) != 0:
                            self._undo_the_move()"""

            self.draw_frame()
            pygame.display.flip()

        pygame.quit()
