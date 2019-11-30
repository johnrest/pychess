# Pychess
import os
from itertools import chain
from collections import Counter, namedtuple
import sys
import pygame

from src import *
# TODO: safely handle imports, remove all import *

# Initialize modules from pygame
pygame.init()

if __name__ == '__main__':
    c = Chess()
    # c.add_piece(Piece("K", True, True, Square(0, 0)))
    # c.print()
    c.game()

    # c.game()

    # c = Chess(setup = "default")
    # c = Chess()
    # c.add_piece(Piece("R", "w", True, 'd1'))
    # c.add_piece(Piece("N", "b", True, 'd6'))
    # c.add_piece(Piece("P", "w", True, 'c2'))
    #
    # c.print()
    # c.move("Rd1->c1")  # w
    # c.move("Nd6->e4")  # b
    # c.move("Pc2->c4")  # w
    # c.move("Ne4->d2")  # b
    # c.print_valid(Square("c1"))
    # print(c.active_white[0].valid_squares)
    print("Done, goodbye")
