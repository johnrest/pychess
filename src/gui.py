import pygame
from main import *

pygame.init()

from pygame.locals import (
    RLEACCEL,
    MOUSEBUTTONDOWN,
    MOUSEBUTTONUP,
    MOUSEMOTION
)

# Set up the drawing window
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 640
SQUARE_SIZE = 80

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])


def chess_to_screen(file, rank, square_size=SQUARE_SIZE):
    """Conversion of chess coordinates to screen coordinates"""
    board_size = 8 * square_size
    x = SCREEN_WIDTH / 2 - board_size / 2 + square_size / 2 + file * square_size
    y = SCREEN_HEIGHT / 2 + board_size / 2 - square_size / 2 - rank * square_size
    return x, y


def screen_to_chess(x, y, square_size=SQUARE_SIZE):
    """Conversion from screen coordinates to chess coordinates"""
    board_size = 8 * square_size
    file = round((x - SCREEN_WIDTH / 2 + board_size / 2 - square_size / 2) / square_size)
    rank = round((-y + SCREEN_HEIGHT / 2 + board_size / 2 - square_size / 2) / square_size)
    return file, rank


class Board(pygame.sprite.Sprite):
    def __init__(self):
        super(Board, self).__init__()
        self.surf = pygame.image.load("../assets/board.png")
        # self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))


class PieceSprite(pygame.sprite.Sprite):
    def __init__(self, file_image, file, rank):
        super(PieceSprite, self).__init__()
        self.surf = pygame.image.load("../assets/" + file_image + ".png")
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)

        self.file, self.rank = 0, 0
        self.x, self.y = 0, 0
        self.rect = []

        self.set_square(file, rank)

        self.dragging = False

    def set_square(self, file, rank):
        self.file, self.rank = file, rank  # Integer values from [0,7]
        self.x, self.y = chess_to_screen(file, rank, SQUARE_SIZE)  # real center positions on screen coordinates
        self.rect = self.surf.get_rect(center=(self.x, self.y))

    def set_pos(self, x, y):
        self.x, self.y = x, y
        self.rect = self.surf.get_rect(center=(self.x, self.y))


static_sprites = pygame.sprite.Group()
board = Board()
static_sprites.add(board)

piece_sprites = pygame.sprite.Group()

piece_sprites.add(PieceSprite("Nw", 1, 0))
piece_sprites.add(PieceSprite("Qw", 3, 3))

# Compute

# Run until the user asks to quit
running = True
dragging = False

while running:

    # Did the user click the window close button?
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1:  # Is this left click?
                for piece in piece_sprites:
                    if piece.rect.collidepoint(event.pos):
                        # mouse_x, mouse_y = event.pos
                        # offset_x = piece.x - mouse_x
                        # offset_y = piece.y - mouse_y
                        piece.dragging = True
                        dragging = True
                        # current_piece = piece
                        # print(current_piece)

        elif event.type == MOUSEBUTTONUP:
            if event.button == 1:
                dragging = False
                for piece in piece_sprites:
                    if piece.dragging:
                        piece.dragging = False

                # if current_piece is not None:
                #     current_piece.dragging = False
                #     current_piece = None
                #     print("PieceSprite released")

        elif event.type == MOUSEMOTION:
            # if current_piece is not None:
            #     if current_piece.dragging:
            if dragging:
                for piece in piece_sprites:
                    if piece.dragging:
                        # print(offset_x, offset_y)
                        mouse_x, mouse_y = event.pos
                        mouse_file, mouse_rank = screen_to_chess(mouse_x, mouse_y, SQUARE_SIZE)
                        mouse_x, mouse_y = chess_to_screen(mouse_file, mouse_rank, SQUARE_SIZE)
                        piece.set_pos(mouse_x, mouse_y)

    # Fill the background with black
    screen.fill((255, 255, 255))

    # Draw all static sprites
    for entity in static_sprites:
        screen.blit(entity.surf, entity.rect)

    # Draw all piece sprites
    for entity in piece_sprites:
        screen.blit(entity.surf, entity.rect)

    # piece_sprites.draw(screen)

    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()
