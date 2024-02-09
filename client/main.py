import pygame

from misc.logger import log
from misc.settings import SCREEN_WIDTH, SCREEN_HEIGHT

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("OS, Remove?")

if __name__ == "__main__":
    log("Loading game...", type="info")
    log(f"Screen size: {SCREEN_WIDTH}x{SCREEN_HEIGHT}")
