import pygame
from objects.enemy import GenericEnemy
from misc.animator import Tileset

class Necromancer(GenericEnemy):
    def __init__(self, x, y, entity, main_loop) -> None:
        super().__init__(x, y, 100, 1, main_loop)
        self.dseireableEntity = entity
        self.main_loop = main_loop
        self.tilesets = {
            "idle": Tileset("assets/images/necromancer/idle.png", (128, 128), 0, 7)
        }
        self.tileset = "idle"

        # Sprite
        self.surf = self.tilesets[self.tileset].increment()
        self.player_react = self.surf.get_rect()

    def update(self):
        pass

    def draw(self, surface: pygame.Surface, playerPos) -> None:
        surface.blit(self.surf, (self.pos[0] - self.player_pos[1], self.pos[1] - self.player_pos[1]))