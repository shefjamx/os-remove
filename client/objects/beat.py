import pygame

class BeatHitter:
    def __init__(self, mainLoop, screen) -> None:
        self.mainLoop = mainLoop
        self.screen = screen
        self.baseImage = pygame.image.load("assets/images/timing_zone.png").convert_alpha()

    def draw(self, screen=None):
        screen = self.screen if screen is None else screen
        screen.blit(self.baseImage, pygame.Rect(0, 0, 100, 100))
        
