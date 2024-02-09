import os

class HitTiming:

    def __init__(self, timing: float):
        self.__TIMING_WINDOWS = self.TIMING_WINDOWS = [(50, 5), (150, 2)]
        self.__timing = timing
    
    def getScore(self, timing: float) -> int:
        """
        Returns the score for the given hit timing 
        """
        for window in self.__TIMING_WINDOWS:
            if abs(self.__timing - timing) <= window[0]: return window[1]
        return 0
    
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
    def __init__(self, levelPath: str):
        self.__levelPath = levelPath
        self.songPath = ""
        self.timingPoints = []
        self.zones = []
        # To add an attribute to the file schema, 
        self.__FILE_SCHEMA = {
            "audio-path": ("songPath", lambda x: x),
            "timing-points": ("timingPoints", lambda x: [HitTiming(float(i)) for i in x.strip('][').split(', ')])
        }
        self.__loadFromPath(levelPath)
        
    
    def __loadFromPath(self, path: str) -> None:
        if not os.path.isfile(path):
            raise FileNotFoundError("No Level Exists!")
        with open(path, "r") as f:
            attributes = f.read().split("\n")
            for attribute in attributes:
                name, value = attribute.split("=")
                if name in self.__FILE_SCHEMA:
                    setattr(self, self.__FILE_SCHEMA[name][0], self.__FILE_SCHEMA[name][1](value))
            print(self.songPath)
    

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
                saveString += f"{attribute}: {getattr(self, attrName)}\n"
            f.write(saveString)
    
    def getHitTimings(self) -> list[HitTiming]:
        return self.timingPoints
    
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