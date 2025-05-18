from enum import Enum

import pygame

from computer import Computer
from piece import Color
from renderer import Renderer
from settings import *
from state import State


class GameState(Enum):
    MAIN_MENU = 1
    PLAYING = 2


class Application(object):
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Checkers!")
        self.running = True
        self.renderer = Renderer(self.window)
        self.state = State()
        self.game_state = GameState.PLAYING
        self.ai = Computer(5, 5)

        self.selected_tile = None
        self.available_moves = []

        self.stack_of_moves = []

    def draw_frame(self):
        if self.game_state == GameState.MAIN_MENU:
            pass
        else:
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
                lambda move: move.dest == selected,
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
                self.stack_of_moves.append(found_moves[0])
            self.deselect()

    def handle_undo_gameplay(self):
        if len(self.stack_of_moves) != 0:
            self.deselect()
            move = self.stack_of_moves.pop()
            self.state.undo_move(move)

    def run(self):
        while self.running:

            if self.state.turn_color == Color.DARK:
                move = self.ai.get_next_best_move(self.state, False)
                if move:
                    self.state.do_move(move)
                    self.stack_of_moves.append(move)
                    continue

            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Handle window close event
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.handle_user_gameplay(event)
                    # TODO: Add undo mechanism
                    if event.button == 3:
                        self.handle_undo_gameplay()

            self.draw_frame()
            pygame.display.flip()

        pygame.quit()
