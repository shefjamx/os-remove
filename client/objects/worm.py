from objects.enemy import GenericEnemy
from misc.logger import log
from misc.animator import Tileset
import random
import pygame

class Worm(GenericEnemy):

    def __init__(self, x, y, desireableEntity, mainLoop):
        super().__init__(x, y, 100, 1, mainLoop)
        self.tilesets["idle"] = Tileset("assets\\images\\wum.jpg", (360, 343), 0, 0, 0.5)
        self.tile_fps["idle"] = 1
        self.tileset = "idle"
        self.sprite = self.tilesets[self.tileset].increment()
        self.desireableEntity = desireableEntity
        self.mainLoop = mainLoop

    def tick(self):
        # player pos vector
        centerPos = (self.pos[0] + self.sprite.get_width() / 2, self.pos[1] + self.sprite.get_height() / 2)
        entityCenter = (self.desireableEntity.getX() + self.desireableEntity.getWidth() / 2 - 100, self.desireableEntity.getY() + self.desireableEntity.getHeight() / 2)
        direction_vector = (centerPos[0] - entityCenter[0], centerPos[1] - entityCenter[1])
        distToEntity = (direction_vector[0] ** 2 + direction_vector[1] ** 2) ** 0.5

        self.pos[0] -= (direction_vector[0] / distToEntity) * 100 * self.mainLoop.dt
        self.pos[1] -= (direction_vector[1] / distToEntity) * 100 * self.mainLoop.dt
        return super().tick()

    def draw(self, surface: pygame.Surface, playerPos) -> None:
        surface.blit(self.sprite, (self.pos[0] - playerPos[0], self.pos[1] - playerPos[1]))