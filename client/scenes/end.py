import pygame
import sys
from scenes.generic_scene import GenericScene

class EndScene(GenericScene):
    def __init__(self, screen, main_loop, won=False) -> None:
        super().__init__(screen, main_loop)
        self.won = won
        self.font = pygame.font.Font("assets/fonts/Abaddon Bold.ttf", 96)
        self.label_font = pygame.font.Font("assets/fonts/Abaddon Bold.ttf", 48)
        self.background_image = pygame.image.load("assets/images/home_background.png").convert()

        # Create buttons
        self.buttons = {}
        self.create_button_dict()

    def create_button_dict(self):
        """Create buttons and add them to the dictionary to be later used"""
        self.create_button(490, 370, 300, 60, "LEAVE", 575, 380, sys.exit)

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
        if self.won:
            you = self.font.render("YOU", True, "#D6D5D4")
            survived = self.font.render("SURVIVED", True, "#DB2D20")
            self.display.blit(you, (352, 150))
            self.display.blit(survived, (556, 150))
        else:
            noMore = self.font.render("NO MORE", True, "#D6D5D4")
            files = self.font.render("FILES", True, "#DB2D20")
            self.display.blit(noMore, (348, 150))
            self.display.blit(files, (736, 150))

        self.render_buttons()
        return super().tick()