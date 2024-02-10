import pygame
from scenes.generic_scene import GenericScene
from scenes.play import PlayScene

class ConnectScene(GenericScene):
    def __init__(self, screen, main_loop) -> None:
        super().__init__(screen, main_loop)
        self.background_image = pygame.image.load("assets/images/home_background.png")

        self.party_leader = False
        self.font = pygame.font.Font("assets/fonts/Abaddon Bold.ttf", 96)
        #self.main_loop.change_scene(PlayScene, "anybody-can-find-love")
    
    def handle_menu_input(self, event):
        self.input_box.handle_event(event)


    def connect(self, display):
        return

    def create_party(self, display):
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

        return super().tick()