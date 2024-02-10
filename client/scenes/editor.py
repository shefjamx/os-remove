import pygame
from tkinter import filedialog, Tk

from pygame.locals import (
    K_SPACE,
    K_o,
    K_s,
    K_n
)
from scenes.generic_scene import GenericScene
from objects.level import Level, HitTiming

class Timeline:

    def __init__(self, level: Level) -> None:
        self.level = level
        self.duration = pygame.mixer.Sound(level.getSongPath()).get_length()
        self.currentTime = 0
        self.pauseTime = 0
        self.musicChannel = pygame.mixer.music
        self.musicChannel.load(level.getSongPath())
        self.hitSound = pygame.mixer.Sound("assets\\sound\\hitsound.ogg")

        self.previousRelevantHitObjects = self.level.getNextHitTimings(self.currentTime, 0.5)

        self.buttons = [(pygame.image.load("assets\\images\\ui\\player.png").convert(), self.resume),
                        (pygame.image.load("assets\\images\\ui\\pausegers.png").convert(), self.resume),
                        (pygame.image.load("assets\\images\\ui\\back-to-start.png").convert(), self.resetSong)]
        self.graphicsData = {
            "button-offset-y": 600,
            "button-margin-x": 20,
            "button-container-size": 75*3 + 40
        }

        self.isPlaying = False

    def resetSong(self) -> float:
        self.currentTime = 0
        self.pauseTime = 0
        if self.isPlaying:
            self.musicChannel.play()


    def getTrueCurrentTime(self) -> float:
        return -0.5 + self.musicChannel.get_pos() / 1e3 + self.pauseTime

    def resume(self) -> None:
        self.isPlaying = not self.isPlaying
        if self.isPlaying:
            self.musicChannel.play(0, self.pauseTime)
        else:
            self.pauseTime = self.getTrueCurrentTime()
            self.musicChannel.pause()

    def drawButtons(self, surface: pygame.Surface) -> None:
        for i,b in enumerate(self.buttons):
            xPos = 1280 / 2 - self.graphicsData["button-container-size"] / 2 + (95)*i
            surface.blit(b[0], (xPos,self.graphicsData["button-offset-y"]))

    def draw(self, surface: pygame.Surface, scale) -> None:
        width, height = 1000, 10
        pygame.draw.rect(surface, "#FFFFFF", (140, 500, width, height))
        pygame.draw.rect(surface, "#FFFFFF", (140, 450, 2, 100))
        pygame.draw.rect(surface, "#FFFFFF", (1140, 450, 2, 100))

        for point in self.level.getHitTimings():
            ratio = point.getTiming() / self.duration
            pygame.draw.rect(surface, "#FF0000", (140 + 1000*ratio, 475, 1, 50))

        ratio = self.currentTime / self.duration
        pygame.draw.rect(surface, "#00FF00", (140 + 1000*ratio, 475, 2, 50))

        self.drawButtons(surface)

    def tick(self) -> None:
        if self.isPlaying:
            self.currentTime = self.getTrueCurrentTime()

            currentTickTimes = self.level.getNextHitTimings(self.currentTime, 0.5)
            for tick in currentTickTimes:
                if tick not in self.previousRelevantHitObjects:
                    self.hitSound.play()
            self.previousRelevantHitObjects = currentTickTimes

    def click(self, pos) -> None:
        if 475 <= pos[1] <= 525:
            timingPoint = (pos[0] - 140) * self.duration
            print(f"Adding timing point at {timingPoint}")
            self.level.addHitTiming(timingPoint / 1e3)

        if 600 <= pos[1] <= 650:
            for i,button in enumerate(self.buttons):
                xPos = 1280 / 2 - self.graphicsData["button-container-size"] / 2 + (95)*i
                if xPos <= pos[0] <= xPos + 75:
                    button[1]()


class LevelEditor(GenericScene):

    def __init__(self, screen, mainloop, directory: str = "") -> None:
        super().__init__(screen, mainloop)
        self.main_loop.add_key_binding(K_o, self.openDialog)
        self.main_loop.add_key_binding(K_s, self.save)
        if directory:
            self.open(directory)

    def openDialog(self) -> None:
        """Create a Tk file dialog and cleanup when finished"""
        top = Tk()
        top.withdraw()  # hide window
        file_name = filedialog.askdirectory(parent=top)
        top.destroy()
        if not file_name:
            return
        self.open(file_name.split("/")[-1])

    def open(self, directory: str) -> None:
        self.level = Level(directory)
        self.timeline = Timeline(self.level)
        self.main_loop.add_key_callback(K_SPACE, self.timeline.resume, False)


    def save(self) -> None:
        self.level.saveToPath()


    def newMap(self) -> None:
        # get name of map
        # create level object
        # copy audio file and set path
        pass


    def handle_click(self, pos) -> None:
        if self.timeline:
            self.timeline.click(pos)


    def render(self):
        self.display.fill("#000000")
        self.timeline.draw(self.display, 1.0)

    def tick(self):
        if self.timeline:
            self.timeline.tick()
        self.render()
        return super().tick()
