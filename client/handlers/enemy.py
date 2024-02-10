import random
from objects.enemy import GenericEnemy
from objects.worm import Worm
from objects.necromancer import Necromancer
from objects.zone import Zone



class EnemyHandler:

    NUM_SPAWNS = 4

    def __init__(self, initialSpawnRate: float, initialZone: Zone, mainLoop, player, core) -> None:
        self.initialSpawnRate = initialSpawnRate
        self.enemies: list[GenericEnemy] = []
        self.enemySpawnPoints = [(591, 718), (812, 267), (1258, 44), (1714, 267), (1931, 720), (1712, 1158), (1267, 1385), (815, 1162)] # there are 8 of these :D
        self.mainLoop = mainLoop
        self.setZone(initialZone)
        self.pathfindingTargets = {
            "worm": core,
            "necromancer": core
        }
        self.ENEMY_LIST = {
            "worm": Worm,
            "necromancer": Necromancer
        }
        self.nextSpawn = 0

    def updateSpawnRate(self, mult: float) -> None:
        self.initialSpawnRate*=mult

    def spawnEnemy(self, _type: str, *args) -> None:
        if _type not in self.currentZone.getAllowedEnemies():
            return
        self.enemies.append(self.ENEMY_LIST[_type](*args))

    def spawnRandomEnemy(self, x: float, y: float) -> None:
        """"""
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
                self.spawnRandomEnemy(sp[0], sp[1])
            self.nextSpawn += 4e3 * self.currentZone.getSpawnRate()

        toRemove = []
        for enemy in self.enemies:
            if enemy.currentHealth <= 0:
                toRemove.append(enemy)
            enemy.tick()
        for enemy in toRemove:
            self.enemies.remove(enemy)


    def draw(self, surface, pX, pY) -> None:
        for enemy in self.enemies:
            enemy.draw(surface, (pX, pY))
