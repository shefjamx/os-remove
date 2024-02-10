from objects.enemy import GenericEnemy
from misc.logger import log
import random
import pygame

class Worm(GenericEnemy):

    def __init__(self, x, y, desireableEntity):
        super().__init__(x, y, "assets\\images\\wum.jpg", 100, 1)
        self.desireableEntity = desireableEntity

    def update(self):
        # player pos vector
        self.direction_vector = (self.pos[0] - self.desireableEntity.getX(), self.pos[1] - self.desireableEntity.getY())
        self.pos[0] -= self.direction_vector[0]*0.015
        self.pos[1] -= self.direction_vector[1]*0.015

    def draw(self, surface: pygame.Surface, playerPos) -> None:
        surface.blit(self.sprite, (self.pos[0] - playerPos[0], self.pos[1] - playerPos[1]))