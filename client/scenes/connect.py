import pygame
from tweener import *
from scenes.generic_scene import GenericScene
from scenes.play import PlayScene
from objects.menu.input_box import InputBox
from misc.settings import SCREEN_HEIGHT, SCREEN_WIDTH, ADDRESS, PORT
from misc.logger import log
from handlers.level import LevelHandler
from objects.level import Level

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
        self.levelHandler = LevelHandler(self.main_loop, lambda x: self.begin_level(x))
        self.y_tween.start()
        self.input_box = InputBox((SCREEN_WIDTH / 2) - 50, (SCREEN_HEIGHT / 2) - 25, 100,50,32)
        self.buttons = {}
        self.create_button_dict()
        self.main_loop.client.connect()
        self.is_in_party = False
        self.is_joining_party = False
        self.currentLevel = 0
        self.current_screen = 0


    def create_button_dict(self):
        """Create buttons and add them to the dictionary to be later used"""
        self.create_button(390, 320, 500, 60, "CREATE PARTY", 490, 330, lambda: self.create_party())    
        self.create_button(390, 420, 500, 60, "JOIN PARTY", 520, 430, lambda: self.switch_party())
        self.create_button(900, 600, 325, 60, "LEAVE PARTY", 925, 610, lambda: self.leave_party())
        self.create_button(80, 600, 300, 60, "START GAME", 105, 610, lambda: self.begin_level())
        self.create_button((SCREEN_WIDTH / 2) - 105, 470, 250, 60, "JOIN GAME", (SCREEN_WIDTH / 2) - 100, 480, lambda: self.join_party())


    def leave_party(self) -> None:
        self.is_in_party = False
        self.is_joining_party = False
        self.current_screen = 0
        # broadcast back to server 
        self.main_loop.client.leave_party()
        log("Leaving Party")
        pass

    def create_button(self, x, y, w, h, text, tx, ty, callback):
        """
        Add an individual button to the list
        tx, ty => text x and text y
        """
        rect = pygame.Rect(x, y, w, h)
        label = self.label_font.render(text, True, "#1F284D")
        self.buttons[text] = [rect, [label, tx, ty], callback]

    def begin_level(self) -> None:
        #TODO: no idea how to do this can somebody else do it
        log("Telling server to begin level")
        self.main_loop.client.start_game()
        pygame.mixer.music.stop()
        #self.main_loop.client.send_spawn_rate("2.03")

    def render_buttons(self, buttons):
        buttons = buttons or self.buttons
        for button in buttons:
            pygame.draw.rect(self.display, "#BED9E5", self.buttons[button][0])
            self.display.blit(self.buttons[button][1][0], (self.buttons[button][1][1], self.buttons[button][1][2]))

    def handle_click(self, mouse_pos):
        for button in self.buttons:
            if self.buttons[button][0].collidepoint(mouse_pos):
                if self.current_screen == 0:
                    if (button == "CREATE PARTY" or button == "JOIN PARTY"):
                        self.buttons[button][2]()
                elif self.current_screen == 1:
                     if (button == "JOIN GAME") or (button == "LEAVE PARTY"): 
                        self.buttons[button][2]()
                elif self.current_screen == 2:
                    if button == "LEAVE PARTY" or button == "START GAME":
                        self.buttons[button][2]()

    def handle_menu_input(self, event):
        self.input_box.handle_event(event)

    def switch_party(self):
        self.is_joining_party = not self.is_joining_party
        self.current_screen = 1

    def join_party(self):
        # render button
        # on button press, get text from input
        # try send a join party message
        party_code = self.input_box.get_text_value().upper()
        log(f"Joining party {party_code}")
        self.main_loop.client.join_party(party_code)

    def create_party(self):
        print("Create party")
        self.current_screen = 2
        self.main_loop.client.create_party()
        self.is_in_party = True

    def tick(self):
        # Background
        rect = self.background_image.get_rect()
        self.display.blit(self.background_image, rect)

        if self.current_screen == 2:
            party_code = self.font.render(f"Party Code: ", True, "#D6D5D4")
            code = self.font.render(f"{self.main_loop.client.party_code}", False, "#DB2D20")
            x = (self.display.get_width() - (party_code.get_width() + code.get_width())) / 2
            self.display.blit(party_code, (x, 25))
            self.display.blit(code, (x + party_code.get_width(), 25))

            self.levelHandler.draw(self.display)
            self.render_buttons(["LEAVE PARTY", "START GAME"])
        elif self.current_screen == 1:
            # display input and join button
            self.input_box.draw(self.display)
            self.render_buttons(["JOIN GAME", "LEAVE PARTY"])
        elif self.current_screen == 0:
            # If we are not in a party then display the defaults :D
            os = self.font.render("OS, ", True, "#D6D5D4")
            remove = self.font.render("REMOVE", True, "#DB2D20")
            question_mark = self.font.render("?", True, "#D6D5D4")

            self.display.blit(os, (388, self.y_tween.value))
            self.display.blit(remove, (550, self.y_tween.value))
            self.display.blit(question_mark, (850, self.y_tween.value))
            self.render_buttons(["CREATE PARTY", "JOIN PARTY"])

        #self.input_box.draw(self.display)
        self.y_tween.update()
        return super().tick(),
