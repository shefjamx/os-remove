import pygame
import sys
from tweener import Tween, Easing, EasingMode

from scenes.generic_scene import GenericScene
from objects.menu.input_box import InputBox
# from scenes.connect import ConnectScene
from scenes.connect import ConnectScene
from scenes.editor import LevelEditor

class HomeScreen(GenericScene):
    def __init__(self, screen, main_loop) -> None:
        super().__init__(screen, main_loop)
        self.font = pygame.font.Font("assets/fonts/Abaddon Bold.ttf", 96)
        self.label_font = pygame.font.Font("assets/fonts/Abaddon Bold.ttf", 48)
        self.background_image = pygame.image.load("assets/images/home_background.png").convert()
        # Create tween
        self.y_tween = Tween(
            begin=140,
            end=160,
            duration=2000,
            easing=Easing.SINE,
            easing_mode=EasingMode.IN_OUT,
            boomerang=True,
            loop=True
        )
        self.y_tween.start()

        # Create buttons
        self.buttons = {}
        self.create_button_dict()

        # start shake
        self.start_shake(1000, 10)

    def create_button_dict(self):
        """Create buttons and add them to the dictionary to be later used"""
        self.create_button(490, 320, 300, 60, "PLAY", 580, 330, lambda: self.main_loop.change_scene(ConnectScene))
        self.create_button(490, 420, 300, 60, "EDIT", 575, 430, lambda: self.main_loop.change_scene(LevelEditor))
        self.create_button(490, 520, 300, 60, "LEAVE", 575, 530, sys.exit)

    def create_button(self, x, y, w, h, text, tx, ty, callback):
        """
        Add an individual button to the list
        tx, ty => text x and text y
        """
        rect = pygame.Rect(x, y, w, h)
        label = self.label_font.render(text, True, "#1F284D")
        self.buttons[text] = [rect, [label, tx, ty], callback]

    def render_buttons(self):
        for button in self.buttons:
            pygame.draw.rect(self.display, "#BED9E5", self.buttons[button][0])
            self.display.blit(self.buttons[button][1][0], (self.buttons[button][1][1], self.buttons[button][1][2]))

    def handle_click(self, mouse_pos):
        for button in self.buttons:
            if self.buttons[button][0].collidepoint(mouse_pos):
                self.buttons[button][2]()

    def tick(self):
        # Background
        rect = self.background_image.get_rect()
        self.display.blit(self.background_image, rect)

        # Header Text
        os = self.font.render("OS, ", True, "#D6D5D4")
        remove = self.font.render("REMOVE", True, "#DB2D20")
        question_mark = self.font.render("?", True, "#D6D5D4")
        self.display.blit(os, (388, self.y_tween.value))
        self.display.blit(remove, (550, self.y_tween.value))
        self.display.blit(question_mark, (850, self.y_tween.value))

        # Move header and render buttons
        self.y_tween.update()
        self.render_buttons()

        return super().tick()
