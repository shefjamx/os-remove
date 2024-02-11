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
        self.deadBeats = []

    def draw(self, screen=None):
        screen = self.screen if screen is None else screen
        baseImageRect = self.baseImage.get_rect()
        baseImageCoords = (round(DIMENSIONS[0]/2) - round(baseImageRect.w/2), DIMENSIONS[1] - 100)
        screen.blit(self.baseImage, pygame.Rect(baseImageCoords[0], baseImageCoords[1], baseImageRect.w, baseImageRect.h))

        # Beats
        for beat in self.beats:
            beatTime = beat - pygame.mixer.music.get_pos()
            beatOffset = beatTime / (self.beatsPerBar * self.timePerBeat) * baseImageRect.w
            if beatOffset <= -baseImageRect.w / 2:
                self.beats.remove(beat)
            else:
                screen.blit(self.baseBeatImage, pygame.Rect(baseImageCoords[0] + (baseImageRect.w / 2) - 15 + beatOffset, baseImageCoords[1] - 35, 1, 1))

    def deleteNearest(self):
        closest = 9999999999999999999
        for beat in self.beats:
            if abs(beat) + self.baseImage.get_rect().w / 2 < closest: 
                closest = beat
        if closest is not None and closest in self.beats:
            self.beats.remove(closest)
            self.deadBeats.append(closest)

    def tick(self):
        # Get all beats
        beatsAfter = self.scene.level.getNextHitTimings(pygame.mixer.music.get_pos(), self.timePerBeat * (self.beatsPerBar / 2))
        for x in beatsAfter:
            if x.getTiming() not in self.beats and x.getTiming() not in self.deadBeats:
                self.beats.append(x.getTiming())



