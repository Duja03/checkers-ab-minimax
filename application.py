from enum import Enum

import pygame

from computer import Computer
from piece import Color
from renderer import Renderer
from state import State
from utility import *


class Application(object):
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Checkers!")

        self.window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.renderer = Renderer(self.window)
        self.ai = Computer(1, 10)
        self.state = State()

        self.running = True
        self.game_state = GameState.MAIN_MENU
        self.game_mode = GameMode.PLAYER_VS_COMPUTER

        self.selected_tile = None
        self.available_moves = []
        self.stack_of_moves = []

    def reset(self):
        self.state = State()
        self.stack_of_moves = []
        self.deselect()

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

    def gameplay_game_over(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                break
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.renderer.play_again_rect.collidepoint(event.pos):
                        self.game_state = GameState.MAIN_MENU

    def gameplay_main_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                break
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.renderer.p_vs_p_rect.collidepoint(event.pos):
                        self.game_mode = GameMode.PLAYER_VS_PLAYER
                        self.game_state = GameState.PLAYING
                        self.reset()
                    elif self.renderer.p_vs_c_rect.collidepoint(event.pos):
                        self.game_mode = GameMode.PLAYER_VS_COMPUTER
                        self.game_state = GameState.PLAYING
                        self.reset()

    def gameplay_player_vs_player(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                break
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.user_selection_gameplay(event)
                elif event.button == 3:
                    self.user_undo_mechanism()

    def gameplay_player_vs_computer(self):
        # Let computer calculate his move:
        if self.state.turn_color == Color.DARK:
            move = self.ai.get_next_best_move(self.state)

            if move:
                self.state.do_move(move)
                self.stack_of_moves.append(move)

                if self.state.is_terminal():
                    self.game_state = GameState.GAME_OVER
                    return

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                break
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.user_selection_gameplay(event)
                elif event.button == 3:
                    # Undo twice so we end up move before computer started thinking:
                    self.user_undo_mechanism()
                    self.user_undo_mechanism()

    def user_selection_gameplay(self, event):
        # Selecting a move is a two step process,
        # first being selecting brand new tile:
        if self.selected_tile is None:
            selected = get_selected_tile(event.pos)
            self.selected_tile = selected

            # Calculating all valid moves that start in selected tile,
            # accumulating them in self.available_moves:
            self.state.generate_moves_for_tile(selected, self.available_moves)

            # If there are no valid moves deselct,
            # and next selection starts from the beginning:
            if len(self.available_moves) == 0:
                self.deselect()
        else:
            # Second part of selecting a move consists of
            # selecting one of the valid ending tiles:
            selected = get_selected_tile(event.pos)

            # So we filter all found moves so that we get a list
            # of only those that end in the selected tile:
            found_moves = self.filter_available_moves(selected)

            # TODO: Give a choice when multiple moves lead to same place...

            # If such move exists we use it:
            if len(found_moves) != 0:
                self.state.do_move(found_moves[0])
                self.stack_of_moves.append(found_moves[0])

                if self.state.is_terminal():
                    self.game_state = GameState.GAME_OVER

            self.deselect()

    def user_undo_mechanism(self):
        # Check if we made enough moves for undo operation:
        if len(self.stack_of_moves) == 0:
            return

        self.deselect()
        move = self.stack_of_moves.pop()
        self.state.undo_move(move)

    def run(self):
        while self.running:
            if self.game_state == GameState.MAIN_MENU:
                self.gameplay_main_menu()
                self.renderer.draw_main_menu()

            elif self.game_state == GameState.PLAYING:
                if self.game_mode == GameMode.PLAYER_VS_PLAYER:
                    self.gameplay_player_vs_player()
                elif self.game_mode == GameMode.PLAYER_VS_COMPUTER:
                    self.gameplay_player_vs_computer()

                # Drawing when game state is PLAYING:
                self.renderer.draw_tiles()
                self.renderer.draw_selected(self.selected_tile)
                self.renderer.draw_pieces(self.state)
                self.renderer.draw_available_moves(self.state, self.available_moves)

            else:
                self.gameplay_game_over()
                game_result = self.state.state_result()
                self.renderer.draw_game_over(game_result)

            pygame.display.flip()

        pygame.quit()
