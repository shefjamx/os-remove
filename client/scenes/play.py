import pygame
from scenes.generic_scene import GenericScene
from objects.player import Player
from objects.level import Level

from objects.worm import Worm

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
        self.enemies = [Worm(500, 500) for x in range(10)]
        self.musicChannel.play()

        self.pulse = PulseEffect(5, 0, 10, 10, 50)

    def tick(self):
        for e in self.enemies:
            e.update()
        # Background
        rect = self.background_image.get_rect()
        rect.x = -self.player.x
        rect.y = -self.player.y
        self.display.blit(self.background_image, rect)
        for e in self.enemies:
            e.resolveMove(self.player.x, self.player.y)
            e.draw(self.display)

        return super().tick(self.player, self.pulse)