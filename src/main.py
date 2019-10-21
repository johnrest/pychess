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

    def __init__(self):
        """
        Initialize the board on the starting setup for chess
        """
        self.board = {}

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
        self.board['d']['1'] = Piece('Q', 'w', True)
        self.board['d']['8'] = Piece('Q', 'b', True)

        # Kings
        self.board['e']['1'] = Piece('K', 'w', True)
        self.board['e']['8'] = Piece('K', 'b', True)

    def print(self):

        for row in Chess._rows:
            for col in Chess._columns:
                print(self.board[col][row], end=" ")
            print(" ")


c = Chess()
# print(c.board['f']['5'])
c.print()
