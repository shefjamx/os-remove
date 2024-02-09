import pygame
from scenes.generic_scene import GenericScene
from objects.player import Player
from misc.settings import SCREEN_WIDTH, SCREEN_HEIGHT

class PlayScene(GenericScene):
    def __init__(self, screen, main_loop) -> None:
        super().__init__(screen, main_loop)
        self.background_image = pygame.image.load("assets/images/level_draft.png")
        self.player = Player()

    def tick(self):
        # Background
        rect = self.background_image.get_rect()
        rect.x -= 640
        rect.y -= 360
        self.screen.blit(self.background_image, rect)

        # Player
        self.screen.blit(self.player.surf, (SCREEN_WIDTH/2, SCREEN_HEIGHT/2))

        return super().tick()