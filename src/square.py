from collections import namedtuple


class Square(namedtuple("BaseSquare", "x y")):
    """
    Position of a piece with coordinates (x,y) in the range [0,7]
    """

    def __new__(cls, *args, **kwargs):
        def check_values(value):
            assert -1 < value < 8, 'Coordinate value is not within the range [0,7]'

        # check the arguments
        for v in args + tuple(kwargs.values()):
            check_values(v)

        self = super().__new__(Square, *args, **kwargs)
        return self
