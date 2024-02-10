from objects.enemy import GenericEnemy
from objects.worm import Worm
from objects.necromancer import Necromancer
from objects.zone import Zone


class EnemyHandler:

    def __init__(self, initialSpawnRate: float, initialZone: Zone, mainLoop) -> None:
        self.initialSpawnRate = initialSpawnRate
        self.enemies: list[GenericEnemy] = []
        self.mainLoop = mainLoop
        self.setZone(initialZone)
        self.ENEMY_LIST = {
            "worm": Worm,
            "necromancer": Necromancer
        }

    def updateSpawnRate(self, mult: float) -> None:
        self.initialSpawnRate*=mult

    def addEnemy(self, _type: str, x: float, y: float, damage: float, health: float, *args) -> None:
        self.enemies.append(_type(x, y, damage, health, self.mainLoop, *args))

    def purgeEnemies(self) -> None:
        for e in self.enemies:
            e.kill()
        self.enemies = []

    def setZone(self, zone: Zone):
        self.currentZone = zone
