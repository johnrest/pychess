# Pychess
import itertools


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


class Chess:
    """
    Class for all game management
    """
    _files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    _ranks = ['1', '2', '3', '4', '5', '6', '7', '8']
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
        self.board = []

        if setup.lower() == 'default':
            # Pawns
            for file in Chess._files:
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
            self.active_white.append(Piece('P', 'w', True, 'e2'))
            self.active_white.append(Piece('P', 'w', False, 'e2'))
            self.active_white.append(Piece('P', 'w', False, 'e2'))
            self.active_white.append(Piece('P', 'w', False, 'e2'))

    def print(self):
        """
        Primitive print of the board to console
        :return:
        """
        self.board = [["" for _ in range(8)] for __ in range(8)]

        all_active = [self.active_white, self.active_black]
        for piece in itertools.chain(*all_active):
            col = ord(piece.square.file) - ord('a')
            row = int(piece.square.rank) - 1
            self.board[row][col] = piece.name + piece.color

        line = " " + "-- " * 8 + "\n"
        board_string = line
        for r in range(8):
            for c in range(8):
                if self.board[r][c] != "":
                    board_string += "|" + self.board[r][c]
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
        all_active = [self.active_white, self.active_black]
        for piece in itertools.chain(*all_active):
            if piece.state:
                if piece.color == 'w':
                    self.score += Chess._valuations[piece.name]
                elif piece.color == 'b':
                    self.score -= Chess._valuations[piece.name]
        return self.score

    def set_current_player(self, new_player):
        self.current_player = new_player

    def move(self, entry):
        current_active = []
        if self.current_player == 'w':
            current_active = self.active_white
        elif self.current_player == 'b':
            current_active = self.active_black

        # Pawns move
        selected_pieces = []  # Select possible pieces to move
        if len(entry) == 2:
            for piece in current_active:
                if (piece.name == 'P') and (piece.square.file == entry[0]):
                    selected_pieces.append(piece)

        if len(selected_pieces) == 1:
            if selected_pieces[0].square.rank in ['2', '7']:
                if (self.current_player == 'w') and (0 < ord(entry[1]) - ord(selected_pieces[0].square.rank) < 3):
                    selected_pieces[0].square = Square(entry)
                elif (self.current_player == 'b') and (0 < ord(selected_pieces[0].square.rank) - ord(entry[1]) < 3):
                    selected_pieces[0].square = Square(entry)
                else:
                    print("Invalid position")
                    exit()
            else:
                if (self.current_player == 'w') and (ord(entry[1]) - ord(selected_pieces[0].square.rank) == 1):
                    selected_pieces[0].square = Square(entry)
                elif (self.current_player == 'b') and (ord(selected_pieces[0].square.rank) - ord(entry[1]) == 1):
                    selected_pieces[0].square = Square(entry)
                else:
                    print("Invalid position")
                    exit()

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

    # @staticmethod
    # def check_active(active, dead):
    #     for itr, piece in enumerate(active):
    #         if not piece.state:
    #             dead.append(active.pop(itr))
    #     return dead


c = Chess("simple")
# print(c.board['f']['5'])
c.print()

c.move('e4')

c.print()
