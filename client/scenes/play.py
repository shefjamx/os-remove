import pygame
from scenes.generic_scene import GenericScene
from objects.player import Player

from effects.particles.flame_circle_effect import FlameCirle

class PlayScene(GenericScene):
    def __init__(self, screen, main_loop) -> None:
        super().__init__(screen, main_loop)
        self.background_image = pygame.image.load("assets/images/level_draft.png")
        self.player = Player(main_loop)

        #spawn in particles cause fuck it
        self.flame_effect = FlameCirle(10, 5,[100, 100], 5)

    def tick(self):
        # Background
        rect = self.background_image.get_rect()
        rect.x = -self.player.x
        rect.y = -self.player.y
        self.display.blit(self.background_image, rect)

        self.flame_effect.tick(self.display, self.main_loop.dt)

        return super().tick(self.player)