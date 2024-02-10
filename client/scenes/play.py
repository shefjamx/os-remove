import pygame
from scenes.generic_scene import GenericScene
from objects.player import Player
from objects.level import Level
import random

from misc.logger import log
from objects.worm import Worm

class PlayScene(GenericScene):
    def __init__(self, screen, main_loop, level_string: str) -> None:
        pygame.mixer.init()
        super().__init__(screen, main_loop)
        self.level = Level(level_string)
        self.musicChannel = pygame.mixer.music
        self.musicChannel.load(self.level.getSongPath())
        self.background_image = pygame.image.load("assets/images/level_draft.png")
        self.player = Player(main_loop)
        self.enemies = []
        self.musicChannel.play()
        self.STANDARD_SPAWN_TIMER = 1e3 # in ms
        self.performanceSpawnMultiplier = 1.0
        self.nextEnemySpawn = 0

    def checkSpawnEnemy(self):
        currentPos_ms = self.musicChannel.get_pos()
        if currentPos_ms >= self.nextEnemySpawn:
            self.enemies.append(Worm(self.player.x + (random.randint(0,100) - 50), (self.player.y + random.randint(0, 100)-50)))
            self.nextEnemySpawn = currentPos_ms + self.STANDARD_SPAWN_TIMER

    def tick(self):
        self.checkSpawnEnemy()
        for e in self.enemies:
            e.update()
        # Background
        self.display.blit(self.background_image, (-self.player.x, -self.player.y))
        for e in self.enemies:
            e.resolveMove(self.player.x, self.player.y)
            e.draw(self.display)


        return super().tick(self.player)