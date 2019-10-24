# Pychess
import itertools


class Piece:
    """
    Class for objects that are in the board
    """

    def __init__(self, name=None, color=None, state=None, position=None):
        self.name = name
        self.color = color
        self.state = state
        self.position = position

    def __str__(self):
        if (self.name is not None) and (self.color is not None):
            return self.name + self.color
        else:
            return '  '

    def __repr__(self):
        return " ".join([self.name, self.color, str(self.state), self.position])

    def change_position(self, new_position):
        self.position = new_position


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
        self.board = [["" for _ in range(8)] for __ in range(8)]

        if setup.lower() == 'default':
            # Pawns
            for file in Chess._files:
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

        elif setup.lower() == "simple":
            self.active_white.append(Piece('R', 'w', True, 'a1'))

    def print(self):
        """
        Primitive print of the board to console
        :return:
        """
        all_active = [self.active_white, self.active_black]
        for piece in itertools.chain(*all_active):
            col = ord(piece.position[0]) - ord('a')
            row = int(piece.position[1]) - 1
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

    def move(self, new):
        current_active = []
        if self.current_player == 'w':
            current_active = self.active_white
        elif self.current_player == 'b':
            current_active = self.active_black

        # Paws move

        # Other pieces move
        selected_pieces = []  # Select possible pieces to move
        for piece in current_active:
            if new[0] == piece.name:
                selected_pieces.append(piece)

        if len(selected_pieces) == 1:
            selected_pieces[0].position = new[1:]


c = Chess("simple")
# print(c.board['f']['5'])
c.print()

c.move('Re4')

c.print()
