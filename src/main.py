# Pychess

class Piece:
    """
    Class for objects that are in the board
    """

    def __init__(self, name=None, color=None, state=None):
        self.name = name
        self.color = color
        self.state = state

    def __str__(self):
        if (self.name is not None) and (self.color is not None):
            return self.name + self.color
        else:
            return '  '

class Chess:
    """
    Class for all game management
    """
    _columns = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    _rows = ['1', '2', '3', '4', '5', '6', '7', '8']
    _valuations = {'P': 1, 'N': 3, 'B': 3, 'R': 5, 'Q': 9, 'K': 0};

    def __init__(self):
        """
        Initialize the board on the starting setup for chess
        """
        self.board = {}
        self.score = 0

        for col in Chess._columns:
            temp = {}
            for row in Chess._rows:
                temp[row] = Piece()
            self.board[col] = temp

        # Pawns
        for col in Chess._columns:
            self.board[col]['2'] = Piece('P', 'w', True)
            self.board[col]['7'] = Piece('P', 'b', True)

        # Rooks
        self.board['a']['1'] = Piece('R', 'w', True)
        self.board['h']['1'] = Piece('R', 'w', True)
        self.board['a']['8'] = Piece('R', 'b', True)
        self.board['h']['8'] = Piece('R', 'b', True)

        # Knights
        self.board['b']['1'] = Piece('N', 'w', True)
        self.board['g']['1'] = Piece('N', 'w', True)
        self.board['b']['8'] = Piece('N', 'b', True)
        self.board['g']['8'] = Piece('N', 'b', True)

        # Bishops
        self.board['c']['1'] = Piece('B', 'w', True)
        self.board['f']['1'] = Piece('B', 'w', True)
        self.board['c']['8'] = Piece('B', 'b', True)
        self.board['f']['8'] = Piece('B', 'b', True)

        # Queens
        self.board['d']['1'] = Piece('Q', 'w', False)
        self.board['d']['8'] = Piece('Q', 'b', True)

        # Kings
        self.board['e']['1'] = Piece('K', 'w', True)
        self.board['e']['8'] = Piece('K', 'b', True)

    def print(self):
        w = 3
        line = " " + "-- "*8 + "\n"
        board_string = line
        for row in Chess._rows:
            for col in Chess._columns:
                board_string += "|" + str(self.board[col][row])
            board_string += "|\n" + line
        print(board_string)

    def game_score(self):

        for row in Chess._rows:
            for col in Chess._columns:
                piece = self.board[col][row]
                if (piece.name is not None) and (piece.state is True):
                    if piece.color == 'w':
                        self.score += Chess._valuations[piece.name]
                    elif piece.color == 'b':
                        self.score -= Chess._valuations[piece.name]





c = Chess()
# print(c.board['f']['5'])
c.print()
c.game_score()
print(c.score)
