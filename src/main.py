# Pychess
from collections import Counter
import sys

# Global variables
FILES = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
RANKS = ['1', '2', '3', '4', '5', '6', '7', '8']


class Square:
    """
    Simple class to store the position of a piece with chess notation
    """

    def __init__(self, sq="  "):
        # TODO: verify that position has correct values
        self.rank = sq[1]
        self.file = sq[0]

    def __str__(self):
        return self.file + self.rank

    def __repr__(self):
        return "".join([self.file, self.rank])

    def __eq__(self, other):
        return (self.file == other.file) and (self.rank == other.rank)

    def __hash__(self):
        return hash(repr(self))

    def __lt__(self, other):
        return self.file + self.rank < other.file + other.rank

    def to_int_grid(self):
        """
        Translate the square to a grid of integers with the lower corner as (0,0)
        :return: tuple (x, y)
        """
        x = ord(self.file) - ord(FILES[0])
        y = ord(self.rank) - ord(RANKS[0])
        return x, y


class Piece:
    """
    Class for objects that are in the board
    """

    # TODO: verify that color, state and name are valid
    def __init__(self, name=None, color=None, state=None, square=None):
        self.name = name
        self.color = color
        self.state = state
        self.square = Square(square)

    def __str__(self):
        if (self.name is not None) and (self.color is not None):
            return self.name + self.color
        else:
            return '  '

    def __repr__(self):
        return " ".join([self.name, self.color, str(self.state), str(self.square)])

    def change_square(self, new_square):
        self.square = new_square

    def valid_squares(self):
        """
        Compute all valid squares for the current piece as if it were alone in the board.
        :return: List of Positions objects
        """
        types = {'R': Piece.valid_rook, 'B': Piece.valid_bishop, 'N': Piece.valid_knight,
                 'Q': Piece.valid_queen, 'K': Piece.valid_king, 'P': Piece.valid_pawn}

        def select_function(function, piece):
            return function(piece)

        squares = select_function(types.get(self.name), self)
        return squares

    @staticmethod
    def sort_valid_squares(square, valid, valid_sorted):
        """
        Sort the valid squares according to their distance to the piece square.
        The sorting facilitates to filter the valid moves with respect to other pieces,
        yet this is done inside the Chess class.
        :param square: current square
        :param valid: list of all valid squares
        :param valid_sorted: Dictionary with the keys expected to be computed, and empty value lists to populate
                e.g.: For a rook, directions are (1,0), (0,1), (-1,0), (0,-1)
        :return: Dictionary with keys describing the direction of the valid squares,
                and values as correspondingly sorted lists
        """

        x1, y1 = square.to_int_grid()
        for v in valid:
            x, y = v.to_int_grid()
            dx = int((x - x1) / abs(x - x1)) if abs(x - x1) > 0 else 0
            dy = int((y - y1) / abs(y - y1)) if abs(y - y1) > 0 else 0
            valid_sorted[(dx, dy)].append(v)                    # Populate dictionary

        # Sort valid squares with respect to the current square
        for direction, valid in valid_sorted.items():
            if direction[0] < 0:                                # "negative directions" have inverse sorting
                reverse = True
            elif (direction[0] == 0) and (direction[1] < 0):    # "negative directions" have inverse sorting
                reverse = True
            else:
                reverse = False

            valid_sorted[direction] = sorted(valid_sorted[direction], reverse=reverse)


    @staticmethod
    def valid_rook(piece):
        square = piece.square
        horizontal = {file + square.rank for file in FILES}
        vertical = {square.file + rank for rank in RANKS}
        coordinates = sorted(horizontal ^ vertical)  # symmetric difference
        valid = [Square(coord) for coord in coordinates]

        valid_sorted = {(1, 0): [], (0, 1): [], (-1, 0): [], (0, -1): []}

        Piece.sort_valid_squares(square, valid, valid_sorted)

        return valid_sorted

    @staticmethod
    def valid_bishop(piece):
        square = piece.square
        x1, y1 = square.to_int_grid()
        pos_diagonal_num = [(x, x - x1 + y1) for x in range(8) if (-1 < x - x1 + y1 < 8)]
        neg_diagonal_num = [(x, -x + x1 + y1) for x in range(8) if (-1 < -x + x1 + y1 < 8)]

        pos_diagonal = {chr(p[0] + ord(FILES[0])) + chr(p[1] + ord(RANKS[0])) for p in pos_diagonal_num}
        neg_diagonal = {chr(n[0] + ord(FILES[0])) + chr(n[1] + ord(RANKS[0])) for n in neg_diagonal_num}

        coordinates = sorted(pos_diagonal ^ neg_diagonal)  # symmetric difference

        valid = [Square(coord) for coord in coordinates]

        valid_sorted = {(1, 1): [], (-1, 1): [], (-1, -1): [], (1, -1): []}

        Piece.sort_valid_squares(square, valid, valid_sorted)

        return valid_sorted

    @staticmethod
    def valid_knight(piece):
        square = piece.square
        x1, y1 = square.to_int_grid()

        # Hard coding of the possible L movements of a knight
        pos_xy = []
        for x, y in zip([2, 2, -2, -2, 1, 1, -1, -1], [1, -1, 1, -1, 2, -2, 2, -2]):
            if (-1 < x1 + x < 8) and (-1 < y1 + y < 8):  # Select for within the board
                pos_xy.append((x1 + x, y1 + y))

        coordinates = [chr(p[0] + ord(FILES[0])) + chr(p[1] + ord(RANKS[0])) for p in pos_xy]

        valid = [Square(coord) for coord in coordinates]

        valid_sorted = {(0, 0): valid}               # Knight moves are not sorted

        return valid_sorted

    @staticmethod
    def valid_queen(piece):
        return {**Piece.valid_rook(piece), **Piece.valid_bishop(piece)}

    @staticmethod
    def valid_king(piece):
        square = piece.square
        x1, y1 = square.to_int_grid()

        pos_xy = []
        for x, y in zip([-1, -1, -1, 0, 0, 1, 1, 1], [1, 0, -1, 1, -1, 1, 0, -1]):  # hard code all valid moves
            if (-1 < x1 + x < 8) and (-1 < y1 + y < 8):  # Select for within the board
                pos_xy.append((x1 + x, y1 + y))

        coordinates = [chr(p[0] + ord(FILES[0])) + chr(p[1] + ord(RANKS[0])) for p in pos_xy]

        valid = [Square(coord) for coord in coordinates]

        valid_sorted = {(1, 1): [], (-1, 1): [], (-1, -1): [], (1, -1): [],
                        (1, 0): [], (0, 1): [], (-1, 0): [], (0, -1): []}

        Piece.sort_valid_squares(square, valid, valid_sorted)

        return valid_sorted

    @staticmethod
    def valid_pawn(piece):
        square = piece.square
        color = piece.color
        x1, y1 = square.to_int_grid()

        steps = 2 if square.rank in ['2', '7'] else 1  # Starting pawns can jump 1 or 2 squares

        direction = +1 if color == 'w' else -1  # Black pawns move downwards, white pawns move upwards

        pos_y = [y1 + direction * (step + 1) for step in range(steps) if (-1 < y1 + direction * (step + 1) < 8)]

        coordinates = [square.file + chr(p + ord(RANKS[0])) for p in pos_y]

        valid = [Square(coord) for coord in coordinates]

        valid_sorted = {(0, direction): []}

        Piece.sort_valid_squares(square, valid, valid_sorted)

        return valid_sorted


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
            # Pawns
            for file in FILES:
                self.active_white.append(Piece('P', 'w', True, file + '2'))
                self.active_black.append(Piece('P', 'b', True, file + '7'))

            # Rooks
            self.active_white.append(Piece('R', 'w', True, 'a1'))
            self.active_white.append(Piece('R', 'w', True, 'h1'))
            self.active_black.append(Piece('R', 'b', True, 'a8'))
            self.active_black.append(Piece('R', 'b', True, 'h8'))

            # Knights
            self.active_white.append(Piece('N', 'w', True, 'b1'))
            self.active_white.append(Piece('N', 'w', True, 'g1'))
            self.active_black.append(Piece('N', 'b', True, 'b8'))
            self.active_black.append(Piece('N', 'b', True, 'g8'))

            # Bishops
            self.active_white.append(Piece('B', 'w', True, 'c1'))
            self.active_white.append(Piece('B', 'w', True, 'f1'))
            self.active_black.append(Piece('B', 'b', True, 'c8'))
            self.active_black.append(Piece('B', 'b', True, 'f8'))

            # Queens
            self.active_white.append(Piece('Q', 'w', True, 'd1'))
            self.active_black.append(Piece('Q', 'b', True, 'd8'))

            # Kings
            self.active_white.append(Piece('K', 'w', True, 'e1'))
            self.active_black.append(Piece('K', 'b', True, 'e8'))

    def add_piece(self, piece):
        """
        Add a piece to the board
        :param piece: Piece object
        :return: None
        """
        if piece.color == "w":
            self.active_white.append(piece)
        else:
            self.active_black.append(piece)

        self.active_white, self.dead_white = Chess.check_active(self.active_white, self.dead_white)
        self.active_black, self.dead_black = Chess.check_active(self.active_black, self.dead_black)

        assert self._test_valid_active(), "Invalid pieces"

    def print(self):
        """
        Primitive print of the board to console
        :return:
        """
        board = [["" for _ in range(8)] for __ in range(8)]

        all_active = self.active_white + self.active_black
        for piece in all_active:
            col = ord(piece.square.file) - ord('a')
            row = int(piece.square.rank) - 1
            board[row][col] = piece.name + piece.color

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

        if selected_piece is None:
            print("No piece in the selected square")
            exit()

        board = [["" for _ in range(8)] for __ in range(8)]

        for piece in all_active:
            col = ord(piece.square.file) - ord('a')
            row = int(piece.square.rank) - 1
            board[row][col] = piece.name + piece.color

        for _, valid in selected_piece.valid_squares().items():
            for sq in valid:
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

        current_square, future_square = self.parse_move(entry)

        # Obtain active player pieces
        active = self.get_active(self.current_player)

        [current_piece] = [piece for piece in active if piece.square == current_square]

        valid = current_piece.valid_squares()

        if future_square in valid:
            current_piece.change_square(future_square)
        else:
            print("Move is invalid!")

        self.active_white, self.dead_white = Chess.check_active(self.active_white, self.dead_white)
        self.active_black, self.dead_black = Chess.check_active(self.active_black, self.dead_black)

        assert self._test_valid_active(), "Invalid pieces"

        self.switch_current_player()

    # def move(self, entry):
    #
    # current_active = []
    #     if self.current_player == 'w':
    #         current_active = self.active_white
    #     elif self.current_player == 'b':
    #         current_active = self.active_black
    #
    #     # Pawns move
    #     selected_pieces = []  # Select possible pieces to move
    #     if len(entry) == 2:
    #         for piece in current_active:
    #             if (piece.name == 'P') and (piece.square.file == entry[0]):
    #                 selected_pieces.append(piece)
    #
    #     if len(selected_pieces) == 1:
    #         if selected_pieces[0].square.rank in ['2', '7']:
    #             if (self.current_player == 'w') and (0 < ord(entry[1]) - ord(selected_pieces[0].square.rank) < 3):
    #                 selected_pieces[0].square = Square(entry)
    #             elif (self.current_player == 'b') and (0 < ord(selected_pieces[0].square.rank) - ord(entry[1]) < 3):
    #                 selected_pieces[0].square = Square(entry)
    #             else:
    #                 print("Invalid position")
    #                 exit()
    #         else:
    #             if (self.current_player == 'w') and (ord(entry[1]) - ord(selected_pieces[0].square.rank) == 1):
    #                 selected_pieces[0].square = Square(entry)
    #             elif (self.current_player == 'b') and (ord(selected_pieces[0].square.rank) - ord(entry[1]) == 1):
    #                 selected_pieces[0].square = Square(entry)
    #             else:
    #                 print("Invalid position")
    #                 exit()

    #
    # selected_pieces = []  # Select possible pieces to move
    # for piece in current_active:
    #     if entry[0] == piece.name:
    #         selected_pieces.append(piece)
    #
    # new_position = entry[1:]
    # if len(selected_pieces) == 1:
    # Rooks
    # if (selected_pieces[0].position[0] == new_position[0]) or (
    #         selected_pieces[0].position[1] == new_position[1]):
    #     selected_pieces[0].position = new_position
    # else:
    #     print("Invalid position!")
    #     exit()

    # Bishops
    # if abs(ord(selected_pieces[0].position[0]) - ord(new_position[0])) == abs(
    #         ord(selected_pieces[0].position[1]) - ord(new_position[1])):
    #     selected_pieces[0].position = new_position
    # else:
    #     print("Invalid position!")
    #     exit()

    # Knights
    # if (abs(ord(selected_pieces[0].position[0]) - ord(new_position[0])) == 2) and (abs(ord(selected_pieces[0].position[1]) - ord(new_position[1])) == 1):
    #     selected_pieces[0].position = new_position
    # elif (abs(ord(selected_pieces[0].position[0]) - ord(new_position[0])) == 1) and (abs(ord(selected_pieces[0].position[1]) - ord(new_position[1])) == 2):
    #     selected_pieces[0].position = new_position
    # else:
    #     print("Invalid position")
    #     exit()

    # Queens
    # if (selected_pieces[0].position[0] == new_position[0]) or (
    #         selected_pieces[0].position[1] == new_position[1]) or (
    #         abs(ord(selected_pieces[0].position[0]) - ord(new_position[0])) == abs(
    #         ord(selected_pieces[0].position[1]) - ord(new_position[1]))):
    #     selected_pieces[0].position = new_position
    # else:
    #     print("Invalid position!")
    #     exit()

    def _test_valid_active(self):
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


# c = Chess(setup = "default")
c = Chess()
c.add_piece(Piece("K", "w", True, 'e4'))
print(c.active_white[0].valid_squares())
c.print_valid(Square("e4"))
# c.print_valid(Square('f1'))
# c.add_piece(Piece("Q", "b", True, 'd8'))
# c.add_piece(Piece("P", "w", True, 'a2'))
# c.print()
# c.move("Ne5->d3")
# c.move("Qd8->d1")
# c.move("Nd3->c5")
# c.move("Qd1->d3")
# c.move("Pa2->a4")
# c.print()
