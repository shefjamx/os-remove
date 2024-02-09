import pygame
from scenes.generic_scene import GenericScene
from logic.level import Level


class LevelScene(GenericScene):

    def __init__(self, pathToLevel: str):
        super().__init__()
        self.__levelIsRunning = False
        self.__level = Level(pathToLevel)
    
    def __render(self):
        rect = self.background_image.get_rect()
    
    def tick(self):
        # Game logic
        if self.__levelIsRunning:
            self.doGameLogic()
        self.__render()
        return super().tick()
    
    def start(self):
        """
        Starts the level. This should be called in response to the server telling the game to start!!
        """