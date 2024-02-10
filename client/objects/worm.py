from objects.enemy import GenericEnemy
from misc.logger import log
from misc.animator import Tileset
from objects.ray import Ray
import random
import pygame

class Worm(GenericEnemy):

    def __init__(self, x, y, mainLoop, desireableEntity):
        super().__init__(x, y, 200, 1, mainLoop)
        self.tilesets["idle"] = Tileset("assets\\images\\wum.jpg", (360, 343), 0, 0, 0.25)
        self.tile_fps["idle"] = 1
        self.tileset = "idle"
        self.sprite = self.tilesets[self.tileset].increment()
        self.desireableEntity = desireableEntity
        self.mainLoop = mainLoop
        centerPos = (self.pos[0] + self.sprite.get_width() / 2, self.pos[1] + self.sprite.get_height() / 2)
        rayCast = Ray(centerPos, self.desireableEntity.getRect())
        self.targetPoint = rayCast.cast() # This is a stupid AI that does not change the point it wants to go to
        self.targetPoint = (self.targetPoint[0] + (random.randint(0, 50) - 25), self.targetPoint[1] + (random.randint(0, 100) - 50))

    def tick(self):
        # player pos vector
        centerPos = (self.pos[0] + self.sprite.get_width() / 2, self.pos[1] + self.sprite.get_height() / 2)
        """entityCenter = (self.desireableEntity.getX() + self.desireableEntity.getWidth() / 2 - 100, self.desireableEntity.getY() + self.desireableEntity.getHeight() / 2)
        direction_vector = (centerPos[0] - entityCenter[0], centerPos[1] - entityCenter[1])
        distToEntity = (direction_vector[0] ** 2 + direction_vector[1] ** 2) ** 0.5 """
        directionVector = (centerPos[0] - self.targetPoint[0], centerPos[1] - self.targetPoint[1])
        distToEntity = (directionVector[0] ** 2 + directionVector[1] ** 2) ** 0.5

        # if distToEntity > 2:
        #     self.pos[0] -= (directionVector[0] / distToEntity) * 100 * self.mainLoop.dt
        #     self.pos[1] -= (directionVector[1] / distToEntity) * 100 * self.mainLoop.dt
        # else:
        #     self.attack(self.desireableEntity)
        return super().tick()

    def attack(self, entity) -> None:
        super().attack(entity)
        self.kill()

    def draw(self, surface: pygame.Surface, playerPos) -> None:
        surface.blit(self.sprite, (self.pos[0] - playerPos[0], self.pos[1] - playerPos[1]))
