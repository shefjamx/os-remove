import pygame
from tweener import *
from scenes.generic_scene import GenericScene
from objects.menu.input_box import InputBox
from misc.settings import SCREEN_HEIGHT, SCREEN_WIDTH

class ConnectScene(GenericScene):
    def __init__(self, screen, main_loop) -> None:
        super().__init__(screen, main_loop)
        self.background_image = pygame.image.load("assets/images/home_background.png")
        self.label_font = pygame.font.Font("assets/fonts/Abaddon Bold.ttf", 48)
        self.party_leader = False
        self.font = pygame.font.Font("assets/fonts/Abaddon Bold.ttf", 96)
        self.menu_options = []
        self.current_option = 0 
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
        self.input_box = InputBox((SCREEN_WIDTH / 2) - 50, (SCREEN_HEIGHT / 2) - 25, 100,50,32)
        self.buttons = {}
        self.create_button_dict()
        #self.main_loop.change_scene(PlayScene, "anybody-can-find-love")

    def create_button_dict(self):
        """Create buttons and add them to the dictionary to be later used"""
        self.create_button(390, 320, 500, 60, "CREATE PARTY", 490, 330, lambda: self.create_party())
        self.create_button(390, 420, 500, 60, "JOIN PARTY", 520, 430, lambda: self.join_party())

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
    
    def handle_menu_input(self, event):
        self.input_box.handle_event(event)


    def join_party(self):
        # render button
        # on button press, get text from input
        # try send a join party message
        print("Join party")
        return

    def create_party(self):
        print("Create party")
        return

    def tick(self):
        # Background
        rect = self.background_image.get_rect()
        self.display.blit(self.background_image, rect)

        # title 
        os = self.font.render("OS, ", True, "#D6D5D4")
        remove = self.font.render("REMOVE", True, "#DB2D20")
        question_mark = self.font.render("?", True, "#D6D5D4")
        self.display.blit(os, (388, self.y_tween.value))
        self.display.blit(remove, (550, self.y_tween.value))
        self.display.blit(question_mark, (850, self.y_tween.value))

        # two options
        self.render_buttons()

        #self.input_box.draw(self.display)

        return super().tick()