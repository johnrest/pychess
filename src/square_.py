from src import *


class Square:
    """
    Simple class to store the position of a piece with chess notation
    """

    def __init__(self, data):
        self.x, self.y = None, None
        self.file, self.rank = None, None

        if isinstance(data, str):
            data = data.lower()
            assert len(data) == 2, "Input string must be length 2"

            self.x = ord(data[0]) - ord('a')
            self.y = ord(data[1]) - ord('1')

            self.file = data[0]
            self.rank = data[1]

        elif isinstance(data, tuple):
            self.x = data[0]
            self.y = data[1]

            self.file = chr(97 + self.x)
            self.rank = chr(49 + self.y)

        else:
            raise ValueError("Wrong initialization of square, provide a tuple or a string")

        assert -1 < self.x < 8, 'Coordinate value is not within the range [0,7]'
        assert -1 < self.y < 8, 'Coordinate value is not within the range [0,7]'

    def __str__(self):
        return self.file + self.rank

    def __repr__(self):
        return "".join([self.file, self.rank])

    def __eq__(self, other):
        return (self.x == other.x) and (self.y == other.y)

    def __hash__(self):
        return hash(repr(self))

    def __lt__(self, other):
        return self.x < other.x and self.y < other.y

    def values(self):
        return self.x, self.y

# class Square(namedtuple("BaseSquare", "x y")):
#     """
#     Position of a piece with coordinates (x,y) in the range [0,7]
#     """
#
#     def __new__(cls, *args, **kwargs):
#         def check_values(value):
#             assert -1 < value < 8, 'Coordinate value is not within the range [0,7]'
#
#         # check the arguments
#         for v in args + tuple(kwargs.values()):
#             check_values(v)
#
#         self = super().__new__(Square, *args, **kwargs)
#         return self
#
#     def __repr__(self):
#         """
#         Overload to print as chess notation
#         :return:
#         """
#         return "".join([chr(97 + self.x), chr(49 + self.y)])
