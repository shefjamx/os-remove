import pygame
from logic.level import Level
from misc.logger import log
from scenes.generic_scene import GenericScene
import time
import enum


class LevelScene(GenericScene):

    class Status(enum.Enum):
        COUNTDOWN = 0
        PLAYING = 1
        FINISHED = 2

    def __init__(self, screen, pathToLevel: str):
        self.GRACE_PERIOD = 5 #countdown before the song plays in seconds
        super().__init__(screen)
        self.musicChannel = pygame.mixer.music
        self.level = Level(pathToLevel)
        self.musicChannel.load(self.level.getSongPath())

        self.status = self.Status.COUNTDOWN
        self.countdownStart = time.perf_counter()
        self.font = pygame.font.Font("assets\\fonts\\Abaddon Bold.ttf", 96)
        self.graphics_attributes = {}
    
    def render(self):
        self.screen.fill((0, 0, 0))
        if self.status == self.Status.COUNTDOWN:
            # Draw the countdown to the screen
            timeTillStart = "{:.2f}".format(self.GRACE_PERIOD - (time.perf_counter() - self.countdownStart))
            _time = self.font.render(f"{timeTillStart}", False, "#FFFFFF")
            if "time-width" not in self.graphics_attributes:
                self.graphics_attributes["time-width"] = _time.get_width() + 10
            _text = self.font.render(f"s to Start", False, "#FFFFFF")
            self.screen.blit(_time,(0, 0))
            self.screen.blit(_text, (self.graphics_attributes["time-width"], 0))

    def startLevel(self):
        self.status = self.Status.PLAYING
        self.musicChannel.play()
    
    def doGameLogic(self):
        if self.status == self.Status.COUNTDOWN:
            timeTillStart = self.GRACE_PERIOD - (time.perf_counter() - self.countdownStart)
            if timeTillStart <= 0:
                self.startLevel()
        elif self.status == self.Status.PLAYING:
            currentSongTime = self.musicChannel.get_pos()
            # spawn any new enemies
            # update enemy positions
            # calculate enemy attacks
            # check if center is still alive after attacks
            # update player position
            # check player attack based on currentSongTime    
    
    def tick(self):
        self.doGameLogic()
        self.render()
        return super().tick()
