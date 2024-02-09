import pygame
from scenes.generic_scene import GenericScene

class HomeScreen(GenericScene):
    def __init__(self, screen) -> None:
        super().__init__(screen)
        self.font = pygame.font.Font("assets/fonts/Abaddon Bold.ttf", 96)
        self.background_image = pygame.image.load("assets/images/home_background.png")

    def tick(self):
        # Background
        rect = self.background_image.get_rect()
        self.screen.blit(self.background_image, rect)

        # Header Text
        os = self.font.render("OS, ", True, "#D6D5D4")
        remove = self.font.render("REMOVE", True, "#DB2D20")
        question_mark = self.font.render("?", True, "#D6D5D4")
        self.screen.blit(os, (388, 148))
        self.screen.blit(remove, (550, 148))
        self.screen.blit(question_mark, (850, 148))
        return super().tick()