# Pychess


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
        return " ".join([self.file, self.rank])

    def __eq__(self, other):
        return (self.file == other.file) and (self.rank == other.rank)

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

    def change_position(self, new_square):
        self.square = new_square

    def valid_squares(self):
        """
        Compute all valid squares for the current piece as if it were alone in the board.
        :return: List of Positions objects
        """
        # Rooks
        types = {'R': Piece.valid_rook, 'B': Piece.valid_bishop, 'N': Piece.valid_knight}

        def select_function(function, piece):
            return function(piece)

        squares = select_function(types.get(self.name), self.square)
        return squares

    @staticmethod
    def valid_rook(square):
        horizontal = {file + square.rank for file in FILES}
        vertical = {square.file + rank for rank in RANKS}
        coordinates = sorted(horizontal ^ vertical)  # symmetric difference
        return [Square(coord) for coord in coordinates]

    @staticmethod
    def valid_bishop(square):
        x1, y1 = square.to_int_grid()
        pos_diagonal_num = [(x, x - x1 + y1) for x in range(8) if (-1 < x - x1 + y1 < 8)]
        neg_diagonal_num = [(x, -x + x1 + y1) for x in range(8) if (-1 < -x + x1 + y1 < 8)]

        pos_diagonal = {chr(p[0] + ord(FILES[0])) + chr(p[1] + ord(RANKS[0])) for p in pos_diagonal_num}
        neg_diagonal = {chr(n[0] + ord(FILES[0])) + chr(n[1] + ord(RANKS[0])) for n in neg_diagonal_num}

        coordinates = sorted(pos_diagonal ^ neg_diagonal)  # symmetric difference

        return [Square(coord) for coord in coordinates]

    @staticmethod
    def valid_knight(square):
        x1, y1 = square.to_int_grid()

        # Hard coding of the possible L movements of a knight
        pos_xy = []
        for x, y in zip([2, 2, -2, -2, 1, 1, -1, -1], [1, -1, 1, -1, 2, -2, 2, -2]):
            if (-1 < x1 + x < 8) and (-1 < y1 + y < 8):     # Select for within the board
                pos_xy.append((x1 + x, y1 + y))

        coordinates = [chr(p[0] + ord(FILES[0])) + chr(p[1] + ord(RANKS[0])) for p in pos_xy]

        return [Square(coord) for coord in coordinates]


class Chess:
    """
    Class for all game management
    """
    _valuations = {'P': 1, 'N': 3, 'B': 3, 'R': 5, 'Q': 9, 'K': 0}

    def __init__(self, setup):
        """
        Initialize the board on the starting setup for chess
        """
        self.current_player = 'w'
        self.active_white = []
        self.active_black = []
        self.dead_white = []
        self.dead_black = []
        self.score = 0

        if setup.lower() == 'default':
            # Pawns
            for file in FILES:
                self.active_white.append(Piece('P', 'w', True, Square(file + '2')))
                self.active_black.append(Piece('P', 'b', True, Square(file + '7')))

            # Rooks
            self.active_white.append(Piece('R', 'w', True, Square('a1')))
            self.active_white.append(Piece('R', 'w', True, Square('h1')))
            self.active_black.append(Piece('R', 'b', True, Square('a8')))
            self.active_black.append(Piece('R', 'b', True, Square('h8')))

            # Knights
            self.active_white.append(Piece('N', 'w', True, Square('b1')))
            self.active_white.append(Piece('N', 'w', True, Square('g1')))
            self.active_black.append(Piece('N', 'b', True, Square('b8')))
            self.active_black.append(Piece('N', 'b', True, Square('g8')))

            # Bishops
            self.active_white.append(Piece('B', 'w', True, Square('c1')))
            self.active_white.append(Piece('B', 'w', True, Square('f1')))
            self.active_black.append(Piece('B', 'b', True, Square('c8')))
            self.active_black.append(Piece('B', 'b', True, Square('f8')))

            # Queens
            self.active_white.append(Piece('Q', 'w', True, Square('d1')))
            self.active_black.append(Piece('Q', 'b', True, Square('d8')))

            # Kings
            self.active_white.append(Piece('K', 'w', True, Square('e1')))
            self.active_black.append(Piece('K', 'b', True, Square('e8')))

        elif setup.lower() == "simple":
            self.active_white.append(Piece('N', 'w', True, 'e4'))
            self.active_white, self.dead_white = Chess.check_active(self.active_white, self.dead_white)

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

        for square in selected_piece.valid_squares():
            col = ord(square.file) - ord('a')
            row = int(square.rank) - 1
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

    def set_current_player(self, new_player):
        self.current_player = new_player

    # def parse_move(self, entry):
    #     """
    #     Transform the chess move from regular notation to a tuple having the
    #     initial and last positions. Check for validity of notation.
    #     :param entry: string with move
    #     :return: Tuple with Position objects (old, new)
    #     """
    #
    #     # Detect if move has correct notation
    #     assert(1 < len(entry) < 6, "Move has incorrect length of characters")
    #
    #     # Obtain active player pieces
    #     if self.current_player == 'w':
    #         current_active = self.active_white
    #     else:
    #         current_active = self.active_black
    #
    #     #   Detect what type of piece is moving
    #     if (entry[0] in Chess.FILES) and (len(entry) == 2):        # Simple pawn move
    #         old = Square(entry[0] + chr(ord(entry[1])-1))
    #         new = Square(entry)
    #     elif (entry[0] in Chess._valuations.keys()) and (len(entry) == 3):      #Simple mayor piece move
    #         selected_pieces = [piece for piece in current_active if piece.name == entry[0]]
    #
    #
    #     # Detect location of piece
    #
    #     # Detect if move is legal
    #     # Translate to tuple of Positions
    #
    #     return (old, new)

    # def move(self, entry):
    #     current_active = []
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

    @staticmethod
    def check_active(active, dead):
        new_active = []
        for piece in active:
            if not piece.state:
                dead.append(piece)
            else:
                new_active.append(piece)
        return new_active, dead


c = Chess("simple")
# print(c.board['f']['5'])
c.print()

c.print_valid(Square("e4"))
