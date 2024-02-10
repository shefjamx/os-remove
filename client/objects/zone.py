from __future__ import annotations


class Zone:

    """ Defines a sub-section of a level, the spawn rate for said sub-section and the enemies that can spawn
    Uses a start time and an end time to effectively create waves
    """
    def __init__(self):
        self.allowedEnemies = []

    def addAllowedEnemy(self, enemy: str) -> None:
        """ Add a named enemy to the list of enemies that can spawn in this zone
        """
        self.allowedEnemies.append(enemy)

    def setTimingPoints(self, start: float, end: float) -> None:
        """ Set the start and end times for this zone
        """
        self.startTime = start
        self.endTime = end

    def setSpawnRate(self, spawnRate: float) -> None:
        """ Set the spawn rate for this zone
        """
        self.spawnRate = spawnRate

    def getTimings(self) -> (float, float):
        return self.startTime, self.endTime

    def getSpawnRate(self) -> float:
        return self.spawnRate

    def setName(self, name) -> None:
        self.name = name

    def getAllowedEnemies(self) -> list[str]:
        return self.allowedEnemies

    @staticmethod
    def from_string(dat: str) -> Zone:
        """ Load a zone from string representation

        Parameters:
            data[str]: the unpacked data for the zone
        """
        rZone = Zone()
        data = dat.strip(')(').split(" ")
        rZone.setName(data[0].replace('-', ' '))
        rZone.setTimingPoints(float(data[1]), float(data[2]))
        rZone.setSpawnRate(float(data[3]))
        rZone.allowedEnemies = [enemy for enemy in data[4::]]
        return rZone

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        rStr = f"({self.name.replace(' ', '-')} {self.startTime} {self.endTime} {self.spawnRate}"
        for enemy in self.allowedEnemies:
            rStr += f" {enemy}"
        return rStr + ")"

