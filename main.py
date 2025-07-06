import pygame
import os
import sys
from src.game import Game

def get_base_path():
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    return os.path.abspath(".")

BASE_PATH = get_base_path()

pygame.init()

SCREEN_WIDTH = 960
SCREEN_HEIGHT = 540
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("PIX Invader")

game = Game(screen)
game.run()

pygame.quit()