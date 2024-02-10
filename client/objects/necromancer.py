from objects.enemy import GenericEnemy
from misc.animator import Tileset
from objects.ray import Ray
import pygame

class Necromancer(GenericEnemy):
    def __init__(self, x, y, mainLoop, desireableEntity):
        super().__init__(x, y, 200, 1, mainLoop)
        self.mainLoop = mainLoop
        self.tilesets = {
            "run": Tileset("assets/images/necromancer/run.png", (160, 128), 0, 5, 2),
            "death": Tileset("assets/images/necromancer/death.png", (160, 128), 0, 8, 2)  # Updated with callback later in code
        }
        self.tile_fps = {
            "run": 12,
            "death": 12
        }
        self.tileset = "run"

        self.sprite = self.tilesets[self.tileset].increment()
        self.desireableEntity = desireableEntity
        
        centerPos = (self.pos[0] + self.sprite.get_width() / 2, self.pos[1] + self.sprite.get_height() / 2)
        rayCast = Ray(centerPos, self.desireableEntity.getRect())
        self.targetPoint = rayCast.cast() # This is a stupid AI that does not change the point it wants to go to
        self.targetPoint = (self.targetPoint[0], self.targetPoint[1])

    def tick(self):
        # player pos vector
        centerPos = (self.pos[0] + self.sprite.get_width() / 2, self.pos[1] + self.sprite.get_height() / 2)
        directionVector = (centerPos[0] - self.targetPoint[0], centerPos[1] - self.targetPoint[1])
        distToEntity = (directionVector[0] ** 2 + directionVector[1] ** 2) ** 0.5

        if distToEntity > 15:
            self.pos[0] -= (directionVector[0] / distToEntity) * 100 * self.mainLoop.dt * self.speed
            self.pos[1] -= (directionVector[1] / distToEntity) * 100 * self.mainLoop.dt * self.speed
        else:
            self.attack(self.desireableEntity)
        return super().tick()

    def attack(self, entity) -> None:
        super().attack(entity)
        self.currentHealth = 0

    def kill(self, callback=None) -> None:
        """Kill the enemy and play the necromancer animation"""
        self.speed = 0
        self.tilesets["death"] = Tileset("assets/images/necromancer/death.png", (160, 128), 0, 8, 2, callback=callback)
        self.tileset = "death"

    def getBoundingBox(self) -> pygame.Rect:
        oldBoundingBox = super().getBoundingBox()
        newBoundingBox = pygame.Rect(oldBoundingBox.x + (oldBoundingBox.width * 3/4)/2, 
                                     oldBoundingBox.y + (oldBoundingBox.height * 0.5), oldBoundingBox.width / 4, oldBoundingBox.height / 2)
        return newBoundingBox
    

    def draw(self, surface: pygame.Surface, playerPos) -> None:
        surface.blit(self.sprite, (self.pos[0] - playerPos[0], self.pos[1] - playerPos[1]))
        super().draw(surface, playerPos)
