from __future__ import annotations
import os
import pathlib
import pygame

from misc.logger import log
from objects.zone import Zone

class HitTiming:
    def __init__(self, timing: float):
        self.__timing = timing

    def setup(self, bpm):
        self.timePerBeat = 60/bpm*1000
        self.__TIMING_WINDOWS = self.TIMING_WINDOWS = [(self.timePerBeat*0.25, 5), (self.timePerBeat*0.5, 2), (self.timePerBeat*1, 0)]

    def getScore(self, timing: float) -> tuple[float, int]:
        """
        Returns the score for the given hit timing
        """
        difference = abs(timing - self.__timing)
        for window in self.__TIMING_WINDOWS:
            if difference <= window[0]:
                return difference, window[1]
        return difference, -1

    def getTiming(self) -> float:
        return self.__timing

    def __repr__(self) -> str:
        return str(self)
    def __str__(self) -> str:
        return f"{float(self.__timing)}"

class Level:
    """
    Encapsulates the level object and the reading / writing to file
    """
    def __init__(self, level_string: str):
        self.__levelPath = f"levels\\{level_string}\\level.dat"
        self.songPath = ""
        self.timingPoints = []
        self.zones = []
        self.bpm = 0
        self.playerAttackSpeed = 0.0
        # To add an attribute to the file schema,
        self.__FILE_SCHEMA = {
            "bpm": ("bpm", int),
            "audio-path": ("songPath", str),
            "timing-points": ("timingPoints", self.timingPointsFromString),
            "zones": ("zones", lambda x: [Zone.from_string(dat) for dat in x.strip('][').split(', ')]),
            "player-attack-timing": ("playerAttackSpeed", float)
        }
        self.__loadFromPath(self.__levelPath)
        for timingPoint in self.timingPoints:
            timingPoint.setup(self.bpm)

    def timingPointsFromString(self, data) -> list[HitTiming]:
        timings = data.strip('][').split(', ')
        if '' in timings:
            timings.remove('')
        return [HitTiming(float(i)) for i in timings]

    def __loadFromPath(self, path: str) -> None:
        if not os.path.isfile(path):
            log(f"File {path} not found!", "ERROR")
            raise FileNotFoundError("No Level Exists!")
        with open(path, "r") as f:
            attributes = f.read().split("\n")
            for attribute in attributes:
                name, value = attribute.split("=")
                if name in self.__FILE_SCHEMA:
                    setattr(self, self.__FILE_SCHEMA[name][0], self.__FILE_SCHEMA[name][1](value))
            print(self.zones)


    @staticmethod
    def allLevels(self) -> list[Level]:
        return os.walk("levels")

    @staticmethod
    def newLevel(directory: str, audioFile: str) -> Level:
        with open(f"{directory}\\level.dat", "w+") as f:
            f.write(f"audio-path={audioFile}\n")
            f.write("timing-points=[]\n")
            f.write(f"zones=[(default 0 {pygame.mixer.Sound(audioFile).get_length()*1e3} 1.0)]\n")
            f.write("bpm=120")
            f.write("player-attack-timing=0.1")
        return Level(directory.split("/")[-1])

    def saveToPath(self, path: str = "") -> None:
        """
        Saves this level so that it can be used in the future
        Attributes:
            path[str]: The path to save the level to (if this is empty then the path the level was loaded from will be used)

        Returns:
            None
        """
        path = path or self.__levelPath
        with open(path, "w+") as f:
            saveString = ""
            for attribute in self.__FILE_SCHEMA:
                attrName = self.__FILE_SCHEMA[attribute][0]
                saveString += f"{attribute}={getattr(self, attrName)}\n"
            saveString = saveString.strip("\n")
            f.write(saveString)

    def getHitTimings(self) -> list[HitTiming]:
        return self.timingPoints

    def getNextHitTimings(self, currentTime: float, numTime: float) -> list[HitTiming]:
        """
        Gets the hit timings in between currentTime and currentTime + numTime

        Parameters:
            currentTime[float]: the time to start at in seconds
            numTime[float]: the time to move forward by in seconds

        Returns:
            list of hit timings that fall within the desired range
        """
        return list(filter(lambda x: currentTime <= x.getTiming() < currentTime + numTime, self.timingPoints))

    def addHitTiming(self, float) -> None:
        self.timingPoints.append(HitTiming(float))
        self.timingPoints.sort(key=lambda x: x.getTiming())

    def getSongPath(self) -> str:
        return self.songPath



if __name__ == "__main__":
    path = "C:\\Users\\joant\\Desktop\\test.txt"
    b = Level(path)
    b.addHitTiming(3.5)
    b.saveToPath()
