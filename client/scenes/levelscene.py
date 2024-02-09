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
        self.__musicChannel = pygame.mixer.music
        self.__levelIsRunning = False
        self.__level = Level(pathToLevel)
        self.__musicChannel.load(self.__level.getSongPath())

        self.__status = self.Status.COUNTDOWN
        self.__countdownStart = time.perf_counter()
        self.font = pygame.font.Font("client\\assets\\fonts\\Abaddon Bold.ttf", 96)
        self.__graphics_attributes = {}
    
    def __render(self):
        self.screen.fill((0, 0, 0))
        if self.__status == self.Status.COUNTDOWN:
            timeTillStart = "{:.2f}".format(self.GRACE_PERIOD - (time.perf_counter() - self.__countdownStart))
            _time = self.font.render(f"{timeTillStart}", False, "#FFFFFF")
            if "time-width" not in self.__graphics_attributes:
                self.__graphics_attributes["time-width"] = _time.get_width() + 10
            _text = self.font.render(f"s to Start", False, "#FFFFFF")
            self.screen.blit(_time,(0, 0))
            self.screen.blit(_text, (self.__graphics_attributes["time-width"], 0))

    def __startLevel(self):
        self.__status = self.Status.PLAYING
        self.__musicChannel.play()
    
    def __doGameLogic(self):
        if self.__status == self.Status.COUNTDOWN:
            timeTillStart = self.GRACE_PERIOD - (time.perf_counter() - self.__countdownStart)
            if timeTillStart <= 0:
                self.__startLevel()
        elif self.__status == self.Status.PLAYING:
            currentSongTime = self.__musicChannel.get_pos()

    
    def tick(self):
        self.__doGameLogic()
        self.__render()
        return super().tick()
