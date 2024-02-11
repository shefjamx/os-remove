import pygame
from misc.settings import DIMENSIONS

class BeatHitter:
    def __init__(self, mainLoop, screen, scene, bpm) -> None:
        self.mainLoop = mainLoop
        self.screen = screen
        self.scene = scene
        self.bpm = bpm
        self.baseImage = pygame.image.load("assets/images/timing_zone.png").convert_alpha()
        self.baseBeatImage = pygame.image.load("assets/images/beat.png").convert_alpha()

        self.beatsPerBar = 4
        self.beatsPerGreen = 1
        self.beatsPerOrange = 0.5
        self.beatsPerRed = 0.25
        self.timePerBeat = 60/bpm*1000
        self.beats = []

    def draw(self, screen=None):
        screen = self.screen if screen is None else screen
        baseImageRect = self.baseImage.get_rect()
        baseImageCoords = (round(DIMENSIONS[0]/2) - round(baseImageRect.w/2), DIMENSIONS[1] - 100)
        screen.blit(self.baseImage, pygame.Rect(baseImageCoords[0], baseImageCoords[1], baseImageRect.w, baseImageRect.h))

        # Beats
        for beat in self.beats:
            beatTime = beat - pygame.mixer.music.get_pos()
            beatOffset = beatTime / (self.beatsPerBar * self.timePerBeat) * baseImageRect.w
            screen.blit(self.baseBeatImage, pygame.Rect(baseImageCoords[0] + (baseImageRect.w / 2) - 15 + beatOffset, baseImageCoords[1] - 35, 1, 1))


    def tick(self):
        # Get all beats
        beatsPassed = self.scene.level.getNextHitTimings(pygame.mixer.music.get_pos() - self.timePerBeat * (self.beatsPerBar / 2), self.timePerBeat * (self.beatsPerBar / 2))
        beatsAfter = self.scene.level.getNextHitTimings(pygame.mixer.music.get_pos(), self.timePerBeat * (self.beatsPerBar / 2))
        # Let joe know his function doesnt work for beats before

        self.beats = [x.getTiming() for x in beatsAfter]



