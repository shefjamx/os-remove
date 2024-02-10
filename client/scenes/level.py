import pygame
from misc.logger import log
from scenes.generic_scene import GenericScene
import time
import enum
import math


class LevelScene(GenericScene):

    class Status(enum.Enum):
        COUNTDOWN = 0
        PLAYING = 1
        FINISHED = 2

    def __init__(self, screen, main_loop, pathToLevel: str):
        super().__init__(screen, main_loop)
        self.GRACE_PERIOD = 5 #countdown before the song plays in seconds
        self.APPROACH_RATE = 0.75
        self.level = Level(pathToLevel)
        self.musicChannel = pygame.mixer.music
        self.musicChannel.load(self.level.getSongPath())

        self.status = self.Status.COUNTDOWN
        self.countdownStart = time.perf_counter()
        self.font = pygame.font.Font("assets\\fonts\\Abaddon Bold.ttf", 96)
        self.graphics_attributes = {}

    def render(self):
        self.display.fill((0, 0, 0)) # TODO: replace with background image as appropriate
        if self.status == self.Status.COUNTDOWN:
            # Draw the countdown to the screen TODO: Replace with nicer code :D
            timeTillStart = f"{math.ceil(self.GRACE_PERIOD - (time.perf_counter() - self.countdownStart))}"
            _time = self.font.render(f"{timeTillStart}", False, "#FFFFFF")
            if "time-width" not in self.graphics_attributes:
                self.graphics_attributes["time-width"] = _time.get_width() + 10
            _text = self.font.render(f"s to Start", False, "#FFFFFF")
            self.display.blit(_time,(0, 0))
            self.display.blit(_text, (self.graphics_attributes["time-width"], 0))

    def startLevel(self):
        """
        Begins playing the level
        """
        self.status = self.Status.PLAYING
        self.musicChannel.play()
    

    def drawHitTimings(self) -> None:
        timingPoint = self.musicChannel.get_pos() / 1e3 # current timing point in seconds
        relevantTimingPoints = self.level.getNextHitTimings(timingPoint, self.APPROACH_RATE) # points that need to be rendered
        for tp in relevantTimingPoints:
            ratio = (tp.getTiming() - timingPoint) / self.APPROACH_RATE # how close are we to the perfect hit
            # TODO: rendering logic for actual hit timing circles here :D
    
    def doGameLogic(self):
        if self.status == self.Status.COUNTDOWN:
            timeTillStart = self.GRACE_PERIOD - (time.perf_counter() - self.countdownStart)
            if timeTillStart <= 0:
                self.startLevel()
        elif self.status == self.Status.PLAYING:
            currentSongTime = self.musicChannel.get_pos() / 1e3 # pos in seconds
            # spawn any new enemies
            # update enemy positions
            # calculate enemy attacks
            # check if center is still alive after attacks
            # update player position
            # check player attack based on currentSongTime
            # draw hit timings
    
    def tick(self):
        self.doGameLogic()
        self.render()
        return super().tick()
