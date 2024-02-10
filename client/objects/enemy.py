import pygame
from misc.logger import log
from misc.animator import Tileset

class GenericEnemy:
    sprite_map = {}
    def __init__(self, x: float, y: float, damage: int, health: int, main_loop) -> None:
        self.pos = [x, y]
        self.player_pos = (0, 0)
        self.damage = damage
        self.maxHealth = health
        self.currentHealth = self.maxHealth
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
        self.currentHealth = 0

    def draw(self, surface, playerPos) -> None:
        # draw da enemy
        movedBox = self.getBoundingBox()
        movedBox.x -= playerPos[0]
        movedBox.y -= playerPos[1]
        pygame.draw.rect(surface, "#FF0000", movedBox, 1)

    def takeDamage(self, damageNum: float) -> bool:
        """
        Returns true if the monster is still alive
        """
        self.currentHealth -= damageNum
        if self.currentHealth <= 0:
            self.kill()
            return False
        return True
    
    def getBoundingBox(self) -> pygame.Rect:
        rect = self.sprite.get_rect()
        rect.x = self.pos[0]
        rect.y = self.pos[1]
        return rect

    def attack(self, entity) -> None:
        entity.dealDamage(self.damage)
        #TODO: play anims
