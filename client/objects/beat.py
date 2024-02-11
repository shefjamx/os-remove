import pygame
from misc.settings import DIMENSIONS

class BeatHitter:
    def __init__(self, mainLoop, screen, scene, bpm) -> None:
        self.mainLoop = mainLoop
        self.screen = screen
        self.scene = scene
        self.bpm = bpm
        self.baseImage = pygame.image.load("assets/images/timing_zone.png").convert_alpha()
        self.beatsPerBar = 4
        self.beatsPerGreen = 1
        self.beatsPerOrange = 0.5
        self.beatsPerRed = 0.25

    def draw(self, screen=None):
        screen = self.screen if screen is None else screen
        baseImageRect = self.baseImage.get_rect()
        screen.blit(self.baseImage, pygame.Rect(round(DIMENSIONS[0]/2) - round(baseImageRect.w/2), DIMENSIONS[1] - 100, baseImageRect.w, baseImageRect.h))

    def tick(self):
        # Get all beats
        hitTimings = self.scene.level.getNextHitTimings()
        print(hitTimings)

        
