from src import *


class Piece:
    """
    Chess piece
    """

    # TODO: verify that color, state and name are valid
    def __init__(self, name=None, is_white=None, state=None, square=None):
        self.name = name
        self.is_white = is_white
        self.state = state
        self.square = square
        self.valid_squares = self.compute_valid_squares()
        self.attack_squares = self.compute_attack_squares()

        color = "w" if is_white else "b"
        self.sprite = PieceSprite(self.square.x, self.square.y, self.name + color)

    def __str__(self):
        if (self.name is not None) and (self.is_white is not None):
            return self.name + ("w" if self.is_white else "b")
        else:
            return '  '

    def __repr__(self):
        color = "w" if self.is_white else "b"
        return " ".join([self.name, color, str(self.state), str(self.square)])

    def change_square(self, new_square):
        self.square = new_square
        self.sprite.set_square(new_square.x, new_square.y)
        self.valid_squares = self.compute_valid_squares()  # Update new valid individual squares
        self.attack_squares = self.compute_valid_squares()  # Update new valid individual squares

    def compute_valid_squares(self):
        """
        Compute all valid squares for the current piece as if it were alone in the board.
        :return: Dictionary with key = directions and values = list of valid squares
        """
        types = {'R': Piece.valid_rook, 'B': Piece.valid_bishop, 'N': Piece.valid_knight,
                 'Q': Piece.valid_queen, 'K': Piece.valid_king, 'P': Piece.valid_pawn}

        def select_function(function, piece):
            return function(piece)

        return select_function(types.get(self.name), self)

    def compute_attack_squares(self):
        """
        Compute squares that one piece can possibly attack to. Note: pawns attack different
        than the way they move
        :return: list of Squares
        """

        if self.name == "P":
            direction = +1 if self.is_white else -1
            x1, y1 = self.square.values()
            s1, s2 = None, None
            if (-1 < x1 - 1 < 8) and (-1 < y1 + direction < 8):
                s1 = Square((x1 - 1, y1 + direction))
            if (-1 < x1 + 1 < 8) and (-1 < y1 + direction < 8):
                s2 = Square((x1 + 1, y1 + direction))

            attack_squares = {(1, direction): [s2], (-1, direction): [s1]}
        else:
            attack_squares = self.compute_valid_squares()

        return attack_squares

    @staticmethod
    def sort_valid_squares(square, valid_squares, valid_squares_sorted):
        """
        Sort the valid squares according to their distance to the piece square.
        The sorting facilitates to filter the valid moves with respect to other pieces,
        yet this is done inside the Chess class.
        :param square: current square
        :param valid_squares: list of all valid squares
        :param valid_squares_sorted: Dictionary with the keys expected to be computed, and empty value lists to populate
                e.g.: For a rook, directions are (1,0), (0,1), (-1,0), (0,-1)
        :return: None
        """

        x1, y1 = square.values()

        for v in valid_squares:
            x, y = v.values()
            dx = int((x - x1) / abs(x - x1)) if abs(x - x1) > 0 else 0
            dy = int((y - y1) / abs(y - y1)) if abs(y - y1) > 0 else 0
            valid_squares_sorted[(dx, dy)].append(v)  # Populate dictionary

        # Sort valid squares with respect to the current square
        for direction, valid in valid_squares_sorted.items():
            if direction[0] < 0:  # "negative directions" have inverse sorting
                reverse = True
            elif (direction[0] == 0) and (direction[1] < 0):  # "negative directions" have inverse sorting
                reverse = True
            else:
                reverse = False

            valid_squares_sorted[direction] = sorted(valid_squares_sorted[direction], reverse=reverse)

    @staticmethod
    def valid_rook(piece):
        current_square = piece.square
        x1, y1 = piece.square.values()

        horizontal = {Square((x, y1)) for x in range(8)}
        vertical = {Square((x1, y)) for y in range(8)}
        valid_squares = sorted(horizontal ^ vertical)  # symmetric difference

        valid_squares_sorted = {(1, 0): [], (0, 1): [], (-1, 0): [], (0, -1): []}

        Piece.sort_valid_squares(current_square, valid_squares, valid_squares_sorted)

        return valid_squares_sorted

    @staticmethod
    def valid_bishop(piece):
        current_square = piece.square

        x1, y1 = current_square.values()
        pos_diagonal = {Square((x, x - x1 + y1)) for x in range(8) if (-1 < x - x1 + y1 < 8)}
        neg_diagonal = {Square((x, -x + x1 + y1)) for x in range(8) if (-1 < -x + x1 + y1 < 8)}

        valid_squares = sorted(pos_diagonal ^ neg_diagonal)  # symmetric difference

        valid_squares_sorted = {(1, 1): [], (-1, 1): [], (-1, -1): [], (1, -1): []}

        Piece.sort_valid_squares(current_square, valid_squares, valid_squares_sorted)

        return valid_squares_sorted

    @staticmethod
    def valid_knight(piece):
        current_square = piece.square
        x1, y1 = current_square.values()

        # Hard coding of the L movements of a knight, i.e. 2+1 or 1+2
        valid_squares = []
        for x, y in zip([2, 2, -2, -2, 1, 1, -1, -1], [1, -1, 1, -1, 2, -2, 2, -2]):
            if (-1 < x1 + x < 8) and (-1 < y1 + y < 8):  # Select for within the board
                valid_squares.append(Square((x1 + x, y1 + y)))

        # No directional information is stored, since Knights can jump over pieces
        valid_squares_sorted = {(0, 0): valid_squares}

        return valid_squares_sorted

    @staticmethod
    def valid_queen(piece):
        return {**Piece.valid_rook(piece), **Piece.valid_bishop(piece)}  # Queen moves as this combination

    @staticmethod
    def valid_king(piece):
        current_square = piece.square
        x1, y1 = current_square.values()

        valid_squares = []
        for x, y in zip([-1, -1, -1, 0, 0, 1, 1, 1], [1, 0, -1, 1, -1, 1, 0, -1]):  # hard code all valid moves
            if (-1 < x1 + x < 8) and (-1 < y1 + y < 8):  # Select for within the board
                valid_squares.append(Square((x1 + x, y1 + y)))

        valid_squares_sorted = {(1, 1): [], (-1, 1): [], (-1, -1): [], (1, -1): [],
                                (1, 0): [], (0, 1): [], (-1, 0): [], (0, -1): []}

        Piece.sort_valid_squares(current_square, valid_squares, valid_squares_sorted)

        return valid_squares_sorted

    @staticmethod
    def valid_pawn(piece):
        current_square = piece.square
        x1, y1 = current_square.values()

        steps = 2 if current_square.y in [1, 6] else 1  # Starting pawns can jump 1 or 2 squares

        direction = +1 if piece.is_white else -1  # Black pawns move downwards, white pawns move upwards

        valid_squares = [Square((x1, y1 + direction * step)) for step in range(1, steps + 1) if
                         (-1 < y1 + direction * step < 8)]

        valid_squares_sorted = {(0, direction): []}

        Piece.sort_valid_squares(current_square, valid_squares, valid_squares_sorted)

        return valid_squares_sorted


if __name__ == "__main__":
    print("piece_ module")
