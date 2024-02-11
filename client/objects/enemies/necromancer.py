from objects.enemies.enemy import GenericEnemy
from objects.enemies.ray import Ray
from misc.animator import Tileset
import pygame

from effects.particles.flame.flame_effect import FlameCircle
from effects.particles.particle_themes import ICE


class Necromancer(GenericEnemy):
    def __init__(self, x, y, mainLoop, desireableEntity):
        super().__init__(x, y, 400, 100, mainLoop)
        self.enemyName = "necromancer"
        self.pyro = 3
        self.mainLoop = mainLoop
        self.tilesets = {
            "run": Tileset(mainLoop, "assets/images/necromancer/run.png", (160, 128), 0, 5, self.pyro),
            "death": Tileset(mainLoop, "assets/images/necromancer/death.png", (160, 128), 0, 8, self.pyro, max_repeat=2),
            "attack": Tileset(mainLoop, "assets/images/necromancer/attack.png", (160, 128), 0, 12, self.pyro)
        }
        self.tile_fps = {
            "run": 12,
            "death": 12,
            "attack": 12
        }
        self.tileset = "run"

        self.sprite = self.tilesets[self.tileset].increment()
        self.desireableEntity = desireableEntity

        self.isFlipped = False
        
        centerPos = (self.pos[0] + self.sprite.get_width() / 2, self.pos[1] + self.sprite.get_height() / 2)
        rayCast = Ray(centerPos, self.desireableEntity.getRect())
        self.targetPoint = rayCast.cast() # This is a stupid AI that does not change the point it wants to go to
        self.targetPoint = (self.targetPoint[0], self.targetPoint[1])

        self.isFlipped = self.targetPoint[0] < self.pos[0]


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
        bbHeight = 150
        oldBoundingBox = super().getBoundingBox()
        newBoundingBox = pygame.Rect(oldBoundingBox.x + (oldBoundingBox.width - bbWidth)/2, 
                                     oldBoundingBox.y + (oldBoundingBox.height - bbHeight)*0.9,
                                       bbWidth, bbHeight)
        return newBoundingBox
    

    def draw(self, surface: pygame.Surface, playerPos) -> None:
        surface.blit(pygame.transform.flip(self.sprite, self.isFlipped, False), (self.pos[0] - playerPos[0], self.pos[1] - playerPos[1]))
