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
        rect.x -= 640
        rect.y -= 360
        self.screen.blit(self.background_image, rect)

        # Player
        for e in self.enemies:
            e.draw(self.screen)
        self.screen.blit(self.player.surf, self.player.player_rect)

        return super().tick()