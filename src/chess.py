from src import *
from itertools import chain
from collections import Counter
import sys
import pygame

from src import *


class Chess:
    """
    Class for all game management
    """
    _valuations = {'P': 1, 'N': 3, 'B': 3, 'R': 5, 'Q': 9, 'K': 0}

    def __init__(self, current_player="w", setup=""):
        """
        Initialize the board on the starting setup for chess
        """
        self.current_player = current_player
        self.active_white = []
        self.active_black = []
        self.dead_white = []
        self.dead_black = []
        self.score = 0

        if setup.lower() == 'default':  # Full chess game
            pass
            # TODO: rewrite full chess initial setup

    def add_piece(self, piece):
        """
        Add a piece to the board
        :param piece: Piece object
        :return: None
        """
        if piece.is_white:
            self.active_white.append(piece)
        else:
            self.active_black.append(piece)

        self.active_white, self.dead_white = Chess.check_active(self.active_white, self.dead_white)
        self.active_black, self.dead_black = Chess.check_active(self.active_black, self.dead_black)

        assert self._test_active(), "Invalid pieces"

    def print(self):
        """
        Primitive print of the board to console
        :return:
        """
        board = [["" for _ in range(8)] for __ in range(8)]

        all_active = self.active_white + self.active_black
        for piece in all_active:
            col, row = piece.square
            board[row][col] = piece.name + ("w" if piece.is_white else "b")

        line = " " + "-- " * 8 + "\n"
        board_string = line
        for r in range(8):
            for c in range(8):
                if board[r][c] != "":
                    board_string += "|" + board[r][c]
                else:
                    board_string += "|" + "  "
            board_string += "|\n" + line

        print(board_string)


    def print_valid(self, square):
        """
        Print valid positions for a piece in the specified square
        :param square:
        :return: None
        """
        all_active = self.active_white + self.active_black

        selected_piece = None
        for piece in all_active:
            if piece.square == square:
                selected_piece = piece

        assert selected_piece is not None, "No valid piece in the selected square"

        # Update valid squares considering all pieces in the board
        self.update_all_valid_squares()

        board = [["" for _ in range(8)] for __ in range(8)]

        for piece in all_active:
            col = ord(piece.square.file) - ord('a')
            row = int(piece.square.rank) - 1
            board[row][col] = piece.name + piece.color

        for sq in list(chain(*selected_piece.valid_squares.values())):
            col, row = sq.to_int_grid()
            # col = ord(sq.file) - ord('a')
            # row = int(sq.rank) - 1
            board[row][col] = "++"

        line = " " + "-- " * 8 + "\n"
        board_string = line
        for r in range(8):
            for c in range(8):
                if board[r][c] != "":
                    board_string += "|" + board[r][c]
                else:
                    board_string += "|" + "  "
            board_string += "|\n" + line

        print(board_string)
        # TODO: correctly print updated valid moves

    def game_score(self):
        """
        Compute game score with 1/3/3/5/9/0 scoring
        :return:
        score: signed integer
        """
        all_active = self.active_white + self.active_black
        for piece in all_active:
            if piece.state:
                if piece.color == 'w':
                    self.score += Chess._valuations[piece.name]
                elif piece.color == 'b':
                    self.score -= Chess._valuations[piece.name]
        return self.score

    def switch_current_player(self):
        if self.current_player == "w":
            self.current_player = "b"
            return
        elif self.current_player == "b":
            self.current_player = "w"
            return

    def parse_move(self, entry):
        """
        Transform the chess move from notation "Pa4->a5" to a tuple having the
        initial and last positions. Check for validity of notation.
        :param entry: string with move
        :return: Tuple with Square objects (current, future)
        """

        # Detect if move has correct notation
        assert len(entry) == 7, "Move has incorrect length of characters"

        name = entry[0]
        current_square = Square(entry[1:3])  # Relevant part of the string
        future_square = Square(entry[5:7])  # Relevant part of the string

        # Obtain active player pieces
        active = self.get_active(self.current_player)

        # Evaluate if piece exists on the current square
        flag = False
        for piece in active:
            if (piece.square == current_square) and (piece.name == name):
                flag = True  # Found one correct piece

        assert flag, "Move is invalid. No active pieces match the entry"

        return current_square, future_square

    def move(self, entry):
        """
        Move a piece for the current player according to a user entry
        :param entry: string with the designed format
        :return: None
        """
        current_square, future_square = self.parse_move(entry)

        # Obtain active player pieces
        active = self.get_active(self.current_player)

        # This works as only one active piece can be in a square at the same time
        [current_piece] = [piece for piece in active if piece.square == current_square]

        # Update valid squares considering all pieces in the board
        self.update_all_valid_squares()

        if future_square in list(chain(*current_piece.valid_squares.values())):
            current_piece.change_square(future_square)
        else:
            assert False, "Move is invalid!"

        self.active_white, self.dead_white = Chess.check_active(self.active_white, self.dead_white)
        self.active_black, self.dead_black = Chess.check_active(self.active_black, self.dead_black)

        assert self._test_active(), "Invalid pieces"

        self.switch_current_player()  # change square of moved piece and compute new valid moves
        self.update_all_valid_squares()  # Update valid moves with new board positions

    def update_all_valid_squares(self):
        """
        Update all active pieces valid squares, update the member Piece.valid_pieces dictionary
        :return: None
        """

        all_active = self.active_white + self.active_black

        occupied_squares = [piece.square for piece in all_active]

        for current_piece in all_active:  # Update to all pieces

            # Compute individual valid pieces
            current_piece.compute_valid_squares()

            # Create new dictionary to populate with updated squares
            updated_valid_squares = {direction: [] for direction in current_piece.valid_squares.keys()}

            for direction, squares in current_piece.valid_squares.items():
                for square in squares:
                    if square in occupied_squares:
                        if current_piece.name in ["K", "N"]:  # Kings and Knights do not have obstructed trajectories
                            pass
                        elif current_piece.name in ["Q", "B", "R", "P"]:  # Cut trajectories for other pieces
                            break  # stop appending after finding a blocking piece
                    else:
                        updated_valid_squares[direction].append(square)

            current_piece.valid_squares = updated_valid_squares

    def _test_active(self):
        """
        Test that no two valid pieces have the same square
        :return: True or False
        """
        all_active = self.active_white + self.active_black
        all_squares = [piece.square for piece in all_active]

        counts = Counter(all_squares)

        flag = True

        for key, val in counts.items():
            if val > 1:
                print("ERROR: Square {} is occupied more than once".format(key), file=sys.stderr)
                flag = False
        return flag

    def get_active(self, color):
        if color == "w":
            active = self.active_white
        else:
            active = self.active_black
        return active

    @staticmethod
    def check_active(active, dead):
        new_active = []
        for piece in active:
            if not piece.state:
                dead.append(piece)
            else:
                new_active.append(piece)
        return new_active, dead

    def game(self):
        """
        Method to start the game
        :return: None
        """

        screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

        static_sprites = pygame.sprite.Group()
        board = BoardSprite()
        static_sprites.add(board)

        self.add_piece(Piece("R", True, True, Square(0,0)))
        self.add_piece(Piece("R", False, True, Square(1,1)))

        piece_sprites = pygame.sprite.Group()
        all_active = self.active_white + self.active_black

        for piece in all_active:
            piece_sprites.add(piece.sprite)

        running = True

        while running:
            # Did the user click the window close button?
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    running = False

            # Draw all static sprites
            for sprite in static_sprites:
                screen.blit(sprite.surf, sprite.rect)

            # Draw all piece sprites
            for sprite in piece_sprites:
                screen.blit(sprite.surf, sprite.rect)

            # Flip the display
            pygame.display.flip()

        # Done! Time to quit.
        pygame.quit()
