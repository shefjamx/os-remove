import pygame
from misc.animator import Tileset

class Core:

    def __init__(self, health: int, main_loop):
        self.main_loop = main_loop
        self.health = health
        self.tilesets = {
            "idle": Tileset("assets\\images\\core\\FlyingObelisk_no_lightnings_no_letter.png", (200, 400), 0, 12)
        }
        self.tile_fps = {
            "idle": 12,
            "run": 12,
            "attack": 36
        }
        self.tileset = "idle"

        self.sprite = self.tilesets[self.tileset].increment()
        self.time_since_last_tile = 0
    
    def doDamage(self, damage: int) -> None:
        self.health -= damage

    def draw(self, surface: pygame.Surface, player):
        posX, posY = 2560 / 2 - self.sprite.get_width() / 2, 1440 / 2 - self.sprite.get_height() / 1.5
        surface.blit(self.sprite, (posX - player.x, posY - player.y))

    def tick(self):
        """Tick the player class, used to animate the player"""
        self.time_since_last_tile += self.main_loop.dt
        if self.time_since_last_tile >= 1 / self.tile_fps[self.tileset]:
            self.time_since_last_tile = 0
            self.sprite = self.tilesets[self.tileset].increment()
