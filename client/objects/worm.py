from objects.enemy import GenericEnemy
import random
import pygame

class Worm(GenericEnemy):

    def __init__(self, x, y):
        super().__init__(x, y, "assets\\images\\wum.jpg", 100, 1)

    def update(self):
        self.pos[0] += (random.randint(0, 20) - 10)
        self.pos[1] += (random.randint(0, 20) - 10)

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.sprite, self.pos)