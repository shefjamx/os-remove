import pygame
import random
from typing import List
from objects.enemy import GenericEnemy
from objects.necromancer import Necromancer
from objects.bringer_of_death import BringerOfDeath
from objects.zone import Zone

class EnemyHandler:

    NUM_SPAWNS = 4

    def __init__(self, initialSpawnRate: float, initialZone: Zone, mainLoop, player, core) -> None:
        self.initialSpawnRate = initialSpawnRate
        self.enemies: list[GenericEnemy] = []
        self.enemies_dying: list[GenericEnemy] = []
        self.enemySpawnPoints = [(591, 718), (812, 267), (1258, 44), (1714, 267), (1931, 720), (1712, 1158), (1267, 1385), (815, 1162)] # there are 8 of these :D
        self.mainLoop = mainLoop
        self.setZone(initialZone)
        self.pathfindingTargets = {
            "necromancer": core,
            "bod": core
        }
        self.ENEMY_LIST = {
            "necromancer": Necromancer,
            "bod": BringerOfDeath
        }
        self.nextSpawn = 0

    def updateSpawnRate(self, mult: float) -> None:
        self.initialSpawnRate *= mult

    def spawnEnemy(self, _type: str, *args) -> None:
        if _type not in self.currentZone.getAllowedEnemies():
            return
        self.enemies.append(self.ENEMY_LIST[_type](*args))

    def spawnRandomEnemy(self, x: float, y: float) -> None:
        toSpawn = random.choice(self.currentZone.getAllowedEnemies())
        self.enemies.append(self.ENEMY_LIST[toSpawn](x, y, self.mainLoop, self.pathfindingTargets[toSpawn]))

    def purgeEnemies(self) -> None:
        for e in self.enemies:
            e.kill()
        self.enemies = []

    def setZone(self, zone: Zone):
        self.currentZone = zone

    def tick(self, currentSongTime: float) -> None:
        if currentSongTime >= self.nextSpawn:
            chosenSpawnPoints = [random.choice(self.enemySpawnPoints) for i in range(self.NUM_SPAWNS)]
            for sp in chosenSpawnPoints:
                self.spawnRandomEnemy(sp[0] + random.randint(0, 30) - 15, sp[1] + random.randint(0, 30) - 15)
            self.nextSpawn += 4e3 * self.currentZone.getSpawnRate()

        toRemove = []
        for enemy in self.enemies:
            if enemy.currentHealth <= 0 and enemy not in self.enemies_dying:
                self.enemies_dying.append(enemy)
                toRemove.append(enemy)
            enemy.tick()
        for enemy in toRemove:
            enemy.kill(lambda: self.deleteEnemy(enemy))

    def deleteEnemy(self, enemy):
        if enemy in self.enemies:
            self.enemies.remove(enemy)
            self.enemies_dying.remove(enemy)

    def draw(self, surface, pX, pY) -> None:
        for enemy in self.enemies:
            enemy.draw(surface, (pX, pY))

    def detect_hit(self, test_rect: pygame.rect.Rect, player_pos) -> List[GenericEnemy]:
        """
        Detects a player hit and returns a list of all enemies in that area.
        If there are no enemies then an empty list is returned x
        """
        enemies_hit = []
        for enemy in self.enemies:
            bounding_box = enemy.getRelativeBoundingBox()
            enemy_pos = (bounding_box.x - player_pos[0], bounding_box.y - player_pos[1])
            enemy_rect = pygame.Rect(enemy_pos[0], enemy_pos[1], bounding_box.w, bounding_box.h)
            if test_rect.colliderect(enemy_rect) and enemy not in self.enemies_dying:
                enemies_hit.append(enemy)
        return enemies_hit
