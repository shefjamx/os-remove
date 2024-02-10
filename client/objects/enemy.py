import pygame
from misc.logger import log

class GenericEnemy:

    sprite_map = {}
    def __init__(self, x: float, y: float, sprite: str, damage: int, health: int) -> None:
        self.pos = [x, y]
        self.player_pos = (0, 0)
        self.sprite = GenericEnemy.getSprite(sprite)
        self.damage = damage
        self.health = health
    
    @staticmethod
    def getSprite(sprite):
        if sprite not in GenericEnemy.sprite_map:
            print("Loaded sprite")
            GenericEnemy.sprite_map[sprite] = pygame.image.load(sprite)
        return GenericEnemy.sprite_map[sprite]

    def update(self) -> None:
        # run ai :D
        raise NotImplementedError("Please add ai to ur monster goofy goober")

    def draw(self, surface, cameraPos) -> None:
        # draw da enemy
        raise NotImplementedError("Please draw ur monster silly billy")
    
    def takeDamage(self, damageNum: float) -> bool:
        """
        Returns true if the monster is still alive
        """
        self.health -= damageNum
        return self.health > 0