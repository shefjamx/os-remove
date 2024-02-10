import pygame
from scenes.generic_scene import GenericScene
from objects.player import Player
from objects.level import Level
import random

from misc.logger import log
from objects.worm import Worm
from objects.core import Core

from handlers.enemy import EnemyHandler

from effects.particles.flame_circle_effect import FlameCirle
from effects.particles.pulse_overlay import PulseEffect

class PlayScene(GenericScene):
    def __init__(self, screen, main_loop, level_string: str) -> None:
        pygame.mixer.init()
        super().__init__(screen, main_loop)
        self.level = Level(level_string)
        self.musicChannel = pygame.mixer.music
        self.musicChannel.load(self.level.getSongPath())
        self.background_image = pygame.image.load("assets/images/level_draft.png")
        self.player = Player(main_loop)
        self.core = Core(10e3, self.main_loop)
        self.musicChannel.play()

        self.enemyHandler = EnemyHandler(1.0, self.level.zones[0], self.main_loop, self.player, self.core)

        self.pulse = PulseEffect(10, 10, 100)

    def checkSpawnEnemy(self):
        currentPos_ms = self.musicChannel.get_pos()
        if currentPos_ms >= self.nextEnemySpawn:
            self.enemies.append(Worm(self.player.x + (random.randint(0,100) - 50), (self.player.y + random.randint(0, 100)-50), self.core, self.main_loop))
            self.nextEnemySpawn = currentPos_ms + self.STANDARD_SPAWN_TIMER

    def tick(self):
        self.enemyHandler.tick(self.musicChannel.get_pos())
        # Background
        self.display.blit(self.background_image, (-self.player.x, -self.player.y))
        self.enemyHandler.draw(self.display, self.player.x, self.player.y)
        self.core.draw(self.display, self.player)
        self.core.tick()
        self.player.tick()
        return super().tick(self.player, self.pulse)
