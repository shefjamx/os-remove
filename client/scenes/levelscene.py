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
    
    def __render(self):
        pass

    def __startLevel(self):
        self.__status = self.Status.PLAYING
        self.__musicChannel.play()
    
    def __doGameLogic(self):
        if self.__status == self.Status.COUNTDOWN:
            timeTillStart = self.GRACE_PERIOD - (time.perf_counter() - self.__countdownStart)
            if timeTillStart <= 0:
                self.__startLevel()
        else:
            pass

    
    def tick(self):
        self.__doGameLogic()
        self.__render()
        return super().tick()
