from objects.enemies.enemy import GenericEnemy
from objects.enemies.ray import Ray
from misc.animator import Tileset
import pygame

class BringerOfDeath(GenericEnemy):
    def __init__(self, x: float, y: float, mainLoop, desireableEntity) -> None:
        super().__init__(x, y, 1000, 150, mainLoop)
        self.pyro = 2
        self.mainLoop = mainLoop
        self.tilesets = {
            "run": Tileset(mainLoop, "assets/images/bod/walk.png", (140, 93), 0, 7, self.pyro),
            "death": Tileset(mainLoop, "assets/images/bod/death.png", (140, 93), 1, 7, self.pyro, reverse=True, max_repeat=2),
            "attack": Tileset(mainLoop, "assets/images/bod/attack.png", (140, 93), 0, 7, self.pyro)
        }
        self.tile_fps = {
            "run": 12,
            "death": 12,
            "attack": 12
        }
        self.tileset = "run"
        self.speed = 0.9

        self.sprite = self.tilesets[self.tileset].increment()
        self.desireableEntity = desireableEntity
        
        centerPos = (self.pos[0] + self.sprite.get_width() / 2, self.pos[1] + self.sprite.get_height() / 2)
        rayCast = Ray(centerPos, self.desireableEntity.getRect())
        self.targetPoint = rayCast.cast() # This is a stupid AI that does not change the point it wants to go to
        self.targetPoint = (self.targetPoint[0], self.targetPoint[1])
        self.isFlipped = self.targetPoint[0] <= self.pos[0]

    def tick(self):
        centerPos = (self.pos[0] + self.sprite.get_width() / 2, self.pos[1] + self.sprite.get_height() / 2)
        directionVector = (centerPos[0] - self.targetPoint[0], centerPos[1] - self.targetPoint[1])
        distToEntity = (directionVector[0] ** 2 + directionVector[1] ** 2) ** 0.5

        if distToEntity > 8:
            self.pos[0] -= (directionVector[0] / distToEntity) * 100 * self.mainLoop.dt * self.speed
            self.pos[1] -= (directionVector[1] / distToEntity) * 100 * self.mainLoop.dt * self.speed
        else:
            self.attack(self.desireableEntity)

        return super().tick()
    
    def setHealth(self, health):
        self.currentHealth = health

    def attack(self, entity) -> None:
        if not self.has_attacked:
            self.speed = 0
            self.tilesets["attack"].callback = lambda: self.setHealth(0)
            self.tileset = "attack"
        super().attack(entity)

    def kill(self, callback=None) -> None:
        """Kill the enemy and play the necromancer animation"""
        self.speed = 0
        self.tilesets["death"].callback = callback
        self.tileset = "death"

    def getBoundingBox(self) -> pygame.Rect:
        bbWidth = 80
        bbHeight = 125
        oldBoundingBox = super().getBoundingBox()
        newBoundingBox = pygame.Rect(oldBoundingBox.x + bbWidth*0.25, 
                                     oldBoundingBox.y + (oldBoundingBox.height - bbHeight),
                                       bbWidth, bbHeight)
        return newBoundingBox

    def draw(self, surface: pygame.Surface, playerPos) -> None:
        surface.blit(pygame.transform.flip(self.sprite, self.isFlipped, False), (self.pos[0] - playerPos[0], self.pos[1] - playerPos[1]))