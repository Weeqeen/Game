import pygame
import sys


def reset_game():
    global level
    level = 1
    game_loop(level)


def quit_game():
    pygame.quit()
    sys.exit()
