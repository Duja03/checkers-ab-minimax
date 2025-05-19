import pygame

from piece import *
from utility import *


class Renderer(object):
    def __init__(self, window):
        self.window = window

        self.background_image = pygame.transform.scale(
            pygame.image.load("assets/main menu background.png"),
            (SCREEN_WIDTH, SCREEN_HEIGHT),
        )

        self.header_text = pygame.font.Font(
            "assets/Roboto-Black.ttf", HEADER_FONT_SIZE
        ).render("CHECKERS", True, HEADER_FONT_COLOR)

        self.p_vs_p_text = pygame.font.Font(
            "assets/Roboto-Regular.ttf", BUTTON_FONT_SIZE
        ).render("Player vs. Player", True, BUTTON_FONT_COLOR)

        self.p_vs_c_text = pygame.font.Font(
            "assets/Roboto-Regular.ttf", BUTTON_FONT_SIZE
        ).render("Player vs. AI", True, BUTTON_FONT_COLOR)

        self.play_again_text = pygame.font.Font(
            "assets/Roboto-Regular.ttf", BUTTON_FONT_SIZE
        ).render("Play again", True, BUTTON_FONT_COLOR)

        self.go_draw_text = pygame.font.Font(
            "assets/Roboto-Black.ttf", GAME_OVER_FONT_SIZE
        ).render("Draw!", True, GAME_OVER_FONT_COLOR)
        self.go_light_text = pygame.font.Font(
            "assets/Roboto-Black.ttf", GAME_OVER_FONT_SIZE
        ).render("Light won!", True, GAME_OVER_FONT_COLOR)
        self.go_dark_text = pygame.font.Font(
            "assets/Roboto-Black.ttf", GAME_OVER_FONT_SIZE
        ).render("Dark won!", True, GAME_OVER_FONT_COLOR)

        # Helper rects for easy game mode selection in main menu:
        self.p_vs_p_rect = self.p_vs_p_text.get_rect(
            topleft=(BUTTON_PVP_X, BUTTON_PVP_Y)
        )
        self.p_vs_c_rect = self.p_vs_c_text.get_rect(
            topleft=(BUTTON_PVC_X, BUTTON_PVC_Y)
        )
        self.play_again_rect = self.play_again_text.get_rect(topleft=(AGAIN_X, AGAIN_Y))

    def draw_main_menu(self):
        self.window.blit(self.background_image, (0, 0))
        self.window.blit(self.header_text, (HEADER_X, HEADER_Y))
        self.window.blit(self.p_vs_p_text, (BUTTON_PVP_X, BUTTON_PVP_Y))
        self.window.blit(self.p_vs_c_text, (BUTTON_PVC_X, BUTTON_PVC_Y))

    def draw_game_over(self, state_result):
        assert state_result != StateResult.PLAYING
        self.window.blit(self.background_image, (0, 0))
        if state_result == StateResult.DRAW:
            self.window.blit(self.go_draw_text, (230, 200))
        elif state_result == StateResult.LIGHT_WON:
            self.window.blit(self.go_light_text, (180, 200))
        else:
            self.window.blit(self.go_dark_text, (185, 200))

        self.window.blit(self.play_again_text, (AGAIN_X, AGAIN_Y))

    def draw_tiles(self):
        for tile in range(ROWS * COLS):
            row = tile // ROWS
            col = tile % COLS
            color = LIGHT_TILE_COLOR if (row + col) % 2 == 0 else DARK_TILE_COLOR
            x = col * TILE_SIZE
            y = row * TILE_SIZE
            pygame.draw.rect(self.window, color, (x, y, TILE_SIZE, TILE_SIZE))

    def draw_selected(self, selected_tile):
        if selected_tile is None:
            return
        row = selected_tile // ROWS
        col = selected_tile % COLS
        x = col * TILE_SIZE
        y = row * TILE_SIZE
        pygame.draw.rect(self.window, ACTIVE_TILE_COLOR, (x, y, TILE_SIZE, TILE_SIZE))

    def draw_available_moves(self, state, moves):
        if len(moves) == 0:
            return

        # Gather only unique destination tiles, so it is
        # equally transparent, regardless of number of Moves
        # that lead to that destination:
        dests = set()
        for move in moves:
            dests.add(move.dest)

        # Select starting tile, so we can extract info:
        for tile in dests:
            row = tile // ROWS
            col = tile % COLS
            x = col * TILE_SIZE
            y = row * TILE_SIZE
            surf = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
            self.draw_piece(state.atTile(move.start), surf, row, col, True)
            self.window.blit(surf, (x, y))

    def draw_pieces(self, state):
        for tile in range(ROWS * COLS):
            row = tile // ROWS
            col = tile % COLS
            piece = state.atTile(tile)
            self.draw_piece(piece, self.window, row, col, False)

    def draw_piece(self, piece, surface, row, col, alpha):
        if piece.type == Type.EMPTY:
            return

        color = LIGHT_PIECE_COLOR if piece.is_light() else DARK_PIECE_COLOR
        shadow = LIGHT_PIECE_SHADOW if piece.is_light() else DARK_PIECE_SHADOW

        center_x = (col + 0.5) * TILE_SIZE
        center_y = (row + 0.5) * TILE_SIZE

        if alpha:
            color = color + (128,)
            shadow = shadow + (128,)
            center_x = TILE_SIZE / 2
            center_y = TILE_SIZE / 2
        else:
            center_x = (col + 0.5) * TILE_SIZE
            center_y = (row + 0.5) * TILE_SIZE

        pygame.draw.circle(
            surface,
            shadow,
            (center_x, center_y + PIECE_HEIGHT / 2),
            PIECE_RADIUS,
        )
        pygame.draw.circle(
            surface,
            color,
            (center_x, center_y - PIECE_HEIGHT / 2),
            PIECE_RADIUS,
        )

        if piece.is_queen():
            pygame.draw.circle(
                surface,
                shadow,
                (center_x, center_y - PIECE_HEIGHT / 2),
                QUEEN_RADIUS,
            )
