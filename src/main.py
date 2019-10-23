# Pychess

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
        return [self.name, self.color, self.state, self.position]


class Chess:
    """
    Class for all game management
    """
    _files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    _ranks = ['1', '2', '3', '4', '5', '6', '7', '8']
    _valuations = {'P': 1, 'N': 3, 'B': 3, 'R': 5, 'Q': 9, 'K': 0}

    def __init__(self):
        """
        Initialize the board on the starting setup for chess
        """
        self.active = []
        self.dead = []
        self.score = 0
        self.board = [["" for _ in range(8)] for __ in range(8)]

        # Pawns
        for file in Chess._files:
            self.active.append(Piece('P', 'w', True, file + '2'))
            self.active.append(Piece('P', 'b', True, file + '7'))

        # Rooks
        self.active.append(Piece('R', 'w', True, 'a1'))
        self.active.append(Piece('R', 'w', True, 'h1'))
        self.active.append(Piece('R', 'b', True, 'a8'))
        self.active.append(Piece('R', 'b', True, 'h8'))

        # Knights
        self.active.append(Piece('N', 'w', True, 'b1'))
        self.active.append(Piece('N', 'w', True, 'g1'))
        self.active.append(Piece('N', 'b', True, 'b8'))
        self.active.append(Piece('N', 'b', True, 'g8'))

        # Bishops
        self.active.append(Piece('B', 'w', True, 'c1'))
        self.active.append(Piece('B', 'w', True, 'f1'))
        self.active.append(Piece('B', 'b', True, 'c8'))
        self.active.append(Piece('B', 'b', True, 'f8'))

        # Queens
        self.active.append(Piece('Q', 'w', True, 'd1'))
        self.active.append(Piece('Q', 'b', True, 'd8'))

        # Kings
        self.active.append(Piece('K', 'w', True, 'e1'))
        self.active.append(Piece('K', 'b', True, 'e8'))

    def print(self):
        """
        Primitive print of the board to console
        :return:
        """
        for piece in self.active:
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
        for piece in self.active:
            if piece.state:
                if piece.color == 'w':
                    self.score += Chess._valuations[piece.name]
                elif piece.color == 'b':
                    self.score -= Chess._valuations[piece.name]
        return self.score

    # def move(self, entry=None):
    #     # Rooks
    #     if entry[0] == 'R':
    #         if len(entry) == 2:


c = Chess()
# print(c.board['f']['5'])
c.print()
print(c.game_score())
