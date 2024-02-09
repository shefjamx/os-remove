import pygame
from tweener import Tween, Easing, EasingMode

from scenes.generic_scene import GenericScene

class HomeScreen(GenericScene):
    def __init__(self, screen) -> None:
        super().__init__(screen)
        self.font = pygame.font.Font("assets/fonts/Abaddon Bold.ttf", 96)
        self.background_image = pygame.image.load("assets/images/home_background.png")
        self.y_tween = Tween(
            begin=130, 
            end=170,
            duration=2000,
            easing=Easing.SINE,
            easing_mode=EasingMode.IN_OUT,
            boomerang=True, 
            loop=True
        )
        self.y_tween.start()

    def tick(self):
        # Background
        rect = self.background_image.get_rect()
        self.screen.blit(self.background_image, rect)

        # Header Text
        os = self.font.render("OS, ", True, "#D6D5D4")
        remove = self.font.render("REMOVE", True, "#DB2D20")
        question_mark = self.font.render("?", True, "#D6D5D4")
        self.screen.blit(os, (388, self.y_tween.value))
        self.screen.blit(remove, (550, self.y_tween.value))
        self.screen.blit(question_mark, (850, self.y_tween.value))

        # Move header and re-render
        self.y_tween.update()
        return super().tick()
    