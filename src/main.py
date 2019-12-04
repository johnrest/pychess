from src import *

# Initialize modules from pygame
pygame.init()

if __name__ == '__main__':
    c = Chess()
    c.game()

    print("Exiting game, goodbye")
