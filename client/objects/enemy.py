import pygame
from misc.logger import log
from misc.animator import Tileset

class GenericEnemy:

    sprite_map = {}
    def __init__(self, x: float, y: float, damage: int, health: int, main_loop) -> None:
        self.pos = [x, y]
        self.player_pos = (0, 0)
        self.damage = damage
        self.health = health
        self.tilesets = {}
        self.tile_fps = {}
        self.main_loop = main_loop
        self.time_since_last_tile = 0


    def tick(self):
        """Tick the player class, used to animate the player"""
        self.time_since_last_tile += self.main_loop.dt
        if self.time_since_last_tile >= 1 / self.tile_fps[self.tileset]:
            self.time_since_last_tile = 0
            self.sprite = self.tilesets[self.tileset].increment()

    def kill(self) -> None:
        # death animation ?
        self.health = 0

    def draw(self, surface, playerPos) -> None:
        # draw da enemy
        raise NotImplementedError("Please draw ur monster silly billy")

    def takeDamage(self, damageNum: float) -> bool:
        """
        Returns true if the monster is still alive
        """
        self.health -= damageNum
        return self.health > 0
