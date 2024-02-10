import pygame
from scenes.generic_scene import GenericScene
from objects.player import Player

from objects.worm import Worm

class PlayScene(GenericScene):
    def __init__(self, screen, main_loop) -> None:
        super().__init__(screen, main_loop)
        self.background_image = pygame.image.load("assets/images/level_draft.png")
        self.player = Player(main_loop)
        self.enemies = [Worm(100, 100) for x in range(10)]

    def tick(self):
        for e in self.enemies:
            e.update()
        # Background
        rect = self.background_image.get_rect()
        rect.x -= self.player.x
        rect.y -= self.player.y
        self.display.blit(self.background_image, rect)

        return super().tick(self.player)