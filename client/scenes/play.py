import pygame
from scenes.generic_scene import GenericScene

class PlayScene(GenericScene):
    def __init__(self, screen, main_loop) -> None:
        super().__init__(screen, main_loop)
        self.background_image = pygame.image.load("assets/images/home_background.png")

    def tick(self):
        # Background
        # rect = self.background_image.get_rect()
        # self.screen.blit(self.background_image, rect)

        return super().tick()