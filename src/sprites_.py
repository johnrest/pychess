from src import *

def chess_to_screen( x, y, square_size=SQUARE_SIZE):
    """Conversion of chess coordinates to screen coordinates"""
    board_size = 8 * square_size
    xs = SCREEN_WIDTH / 2 - board_size / 2 + square_size / 2 + x * square_size
    ys = SCREEN_HEIGHT / 2 + board_size / 2 - square_size / 2 - y * square_size
    return xs, ys

def screen_to_chess(xs, ys, square_size=SQUARE_SIZE):
    """Conversion from screen coordinates to chess coordinates"""
    board_size = 8 * square_size
    x = round((xs - SCREEN_WIDTH / 2 + board_size / 2 - square_size / 2) / square_size)
    y = round((-ys + SCREEN_HEIGHT / 2 + board_size / 2 - square_size / 2) / square_size)
    return x, y

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

    def __init__(self, x=None, y=None, name=None):
        super(PieceSprite, self).__init__()
        self.surf = pygame.image.load(os.path.join(ASSETS_FOLDER, name + ".png"))
        self.surf.set_colorkey((255, 255, 255), pygame.RLEACCEL)

        self.x, self.y = x, y
        self.rect = []

        self.set_square(x, y)

        self.dragging = False

    def set_square(self, x, y):
        xs, ys = chess_to_screen(x, y, square_size=SQUARE_SIZE)  # real center positions on screen coordinates
        self.x, self.y = x, y
        self.rect = self.surf.get_rect(center=(xs, ys))

    # def set_xy(self, x, y):
    #     self.x, self.y = x, y
    #     self.screen_to_chess(square_size=SQUARE_SIZE)
    #     self.rect = self.surf.get_rect(center=(self.x, self.y))



