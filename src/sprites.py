import os
import pygame
from src import *


class BoardSprite(pygame.sprite.Sprite):
    """
    Class to handle the board an all background objects in the game
    """

    def __init__(self):
        super(BoardSprite, self).__init__()
        self.surf = pygame.image.load(BOARD_FILE)
        self.rect = self.surf.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))


class PieceSprite(pygame.sprite.Sprite):
    """
    Sprite for game pieces
    """

    def __init__(self, file=None, rank=None, name=None):
        super(PieceSprite, self).__init__()
        self.surf = pygame.image.load(os.path.join(ASSETS_FOLDER, name + ".png"))
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)

        self.file, self.rank = 0, 0
        self.x, self.y = 0, 0
        self.rect = []

        self.set_square(file, rank)

        self.dragging = False

    def set_square(self, file, rank):
        self.file, self.rank = file, rank  # Integer values from [0,7]
        self.chess_to_screen(square_size=SQUARE_SIZE)  # real center positions on screen coordinates
        self.rect = self.surf.get_rect(center=(self.x, self.y))

    def set_xy(self, x, y):
        self.x, self.y = x, y
        self.screen_to_chess(square_size=SQUARE_SIZE)
        self.rect = self.surf.get_rect(center=(self.x, self.y))

    def chess_to_screen(self, square_size=SQUARE_SIZE):
        """Conversion of chess coordinates to screen coordinates"""
        board_size = 8 * square_size
        self.x = SCREEN_WIDTH / 2 - board_size / 2 + square_size / 2 + self.file * square_size
        self.y = SCREEN_HEIGHT / 2 + board_size / 2 - square_size / 2 - self.rank * square_size

    def screen_to_chess(self, square_size=SQUARE_SIZE):
        """Conversion from screen coordinates to chess coordinates"""
        board_size = 8 * square_size
        self.file = round((self.x - SCREEN_WIDTH / 2 + board_size / 2 - square_size / 2) / square_size)
        self.rank = round((-self.y + SCREEN_HEIGHT / 2 + board_size / 2 - square_size / 2) / square_size)
