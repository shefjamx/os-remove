import pygame
import os
from tkinter import filedialog, Tk
import shutil
import enum

from pygame.locals import (
    K_SPACE,
    K_o,
    K_s,
    K_n,
    K_RIGHT,
    K_LEFT
)
from scenes.generic_scene import GenericScene
from objects.level import Level, HitTiming

class Timeline:

    class EditingMode(enum.Enum):
        E_NORMAL = 1,
        E_ZONES = 2,
        E_PARTICLES = 3,
        E_DATA = 4

    def __init__(self, level: Level) -> None:
        self.level = level
        self.duration = pygame.mixer.Sound(level.getSongPath()).get_length() * 1e3
        self.currentTime = 0
        self.pauseTime = 0
        self.musicChannel = pygame.mixer.music
        self.musicChannel.load(level.getSongPath())
        self.hitSound = pygame.mixer.Sound("assets\\sound\\hitsound.ogg")

        self.previousRelevantHitObjects = self.level.getNextHitTimings(self.currentTime, 0.5)
        self.editingMode = self.EditingMode.E_NORMAL

        self.currentZone = None

        self.label_font = pygame.font.Font("assets/fonts/Abaddon Bold.ttf", 12)
        self.title_font = pygame.font.Font("assets/fonts/Abaddon Bold.ttf", 48)
        self.subtitle_font = pygame.font.Font("assets/fonts/Abaddon Bold.ttf", 30)
        self.audioButtons = [(pygame.image.load("assets\\images\\ui\\zone-selection.png").convert(), lambda: self.toggleZoneMode()),
                        (pygame.image.load("assets\\images\\ui\\player.png").convert(), self.resume),
                        (pygame.image.load("assets\\images\\ui\\pausegers.png").convert(), self.resume),
                        (pygame.image.load("assets\\images\\ui\\back-to-start.png").convert(), self.resetSong),
                        (pygame.image.load("assets\\images\\ui\\zoom-in-timeline.png").convert(), lambda: self.zoom(1.1)),
                        (pygame.image.load("assets\\images\\ui\\zoom-out-timeline.png").convert(), lambda: self.zoom(0.9))]


        self.entitySprites = {
            "necromancer": pygame.image.load("assets\\images\\thumbnails\\necromancer.png").convert(),
            "bod": pygame.image.load("assets\\images\\thumbnails\\bod.png").convert()
        }

        self.graphicsData = {
            "button-offset-y": 600,
            "button-margin-x": 20,
            "button-container-size": 75*3 + 40
        }

        self.isPlaying = False
        self.currentScale = 1.0
    
    def toggleZoneMode(self) -> None:
        if self.editingMode == self.EditingMode.E_ZONES:
            self.editingMode = self.EditingMode.E_NORMAL
        else:
            print("Toggled")
            self.editingMode = self.EditingMode.E_ZONES

    def zoom(self, amt: float) -> None:
        self.currentScale*=amt

    def resetSong(self) -> float:
        self.currentTime = 0
        self.pauseTime = 0
        if self.isPlaying:
            self.musicChannel.play()


    def getTrueCurrentTime(self) -> float:
        return self.musicChannel.get_pos() + self.pauseTime

    def resume(self) -> None:
        self.isPlaying = not self.isPlaying
        if self.isPlaying:
            print(self.pauseTime)
            self.musicChannel.play(0, self.pauseTime/1e3)
        else:
            self.pauseTime = self.getTrueCurrentTime()
            self.musicChannel.pause()
    
    def incrementSong(self, amt) -> None:
        if self.isPlaying:
            return
        self.pauseTime += amt

    def drawButtons(self, surface: pygame.Surface) -> None:
        for i,b in enumerate(self.audioButtons):
            xPos = 1280 / 2 - self.graphicsData["button-container-size"] / 2 + (95)*i
            surface.blit(b[0], (xPos,self.graphicsData["button-offset-y"]))
    
    def getZoneRect(self, startX, startY, zone) -> pygame.Rect:
        start, end = zone.getTimings()
        if int(end) == -1:
            end = self.duration
        start, end = (start / self.duration) * self.width, (end/self.duration) * self.width
        return pygame.Rect(startX + start, startY, end-start, 60)
    
    def drawCurrentZone(self, surface) -> None:
        title = self.title_font.render(f"Zone: {self.currentZone.name}", False, "#FFFFFF")
        surface.blit(title, ((surface.get_width() - title.get_width()) / 2, 0))

        subtitle = self.subtitle_font.render(f"Included Entities", False, "#FFFFFF")
        surface.blit(subtitle, (50, 100))
        for i,entity in enumerate(self.entitySprites.keys()):
            size,margin = 100, 10
            x = 50 + (size+margin)*i
            y = 160 + (size+margin)*(i//6)
            text = self.label_font.render(entity, False, "#FFFFFF")
            color = "#00FF00" if entity in self.currentZone.getAllowedEnemies() else "#FF0000"
            pygame.draw.rect(surface, color, (x, y, 100, 100))
            pygame.draw.rect(surface, "#FFFFFF", (x, y, 100, 100), width=1)
            surface.blit(self.entitySprites[entity], (x,y))
            surface.blit(text, (x,y+105))



    def draw(self, surface: pygame.Surface, scale) -> None:

        if self.editingMode == self.EditingMode.E_ZONES and self.currentZone:
            self.drawCurrentZone(surface)
        scale = self.currentScale
        self.width, self.height = 1000*scale, 10

        x, y = 1280 / 2, 450
        cursorX = self.width * (self.getTrueCurrentTime() / self.duration)
        x -= cursorX
        if self.editingMode == self.EditingMode.E_ZONES:
            for zone in self.level.zones:
                rect = self.getZoneRect(x, y+20, zone)
                pygame.draw.rect(surface, "#66A000", rect)
                pygame.draw.rect(surface, "#FFFFFF", rect, width=1)
                if self.editingMode == self.EditingMode.E_ZONES:
                    text = self.label_font.render(zone.name, False, "#FFFFFF")
                    surface.blit(text, (rect.left + (rect.width - text.get_width()) / 2, y + 20 - text.get_height()))
        
        pygame.draw.rect(surface, "#FFFFFF", (x, y + 50, self.width, self.height))
        pygame.draw.rect(surface, "#FFFFFF", (x, y, 2, 100))
        pygame.draw.rect(surface, "#FFFFFF", (x + self.width, y, 2, 100))

        for point in self.level.getHitTimings():
            ratio = point.getTiming() / self.duration
            pygame.draw.rect(surface, "#FF0000", (x + ratio*self.width, y+25, 1, 50))


        ratio = self.currentTime / self.duration
        pygame.draw.rect(surface, "#00FF00", (1280/2, y + 25, 2, 50))

        self.drawButtons(surface)

    def tick(self) -> None:
        if self.isPlaying:
            self.currentTime = self.getTrueCurrentTime()
            currentTickTimes = self.level.getNextHitTimings(self.currentTime, 500)
            for tick in self.previousRelevantHitObjects:
                if tick not in currentTickTimes:
                    print(self.musicChannel.get_pos())
                    self.hitSound.play()
            self.previousRelevantHitObjects = currentTickTimes

    def click(self, pos) -> None:
        x = 1280 / 2 - self.width * (self.currentTime / self.duration)
        if self.editingMode == self.EditingMode.E_NORMAL:
            if 475 <= pos[1] <= 525:
                timingPoint = (pos[0] - x) * self.duration / self.width
                self.level.addHitTiming(timingPoint)
        elif self.editingMode == self.EditingMode.E_ZONES:
            for zone in self.level.zones:
                if self.getZoneRect(x, 470, zone).collidepoint(pos[0], pos[1]):
                    print("zoned bitch")
                    self.currentZone = zone
            if self.currentZone:
                for i,entity in enumerate(self.entitySprites.keys()):
                    rect = pygame.Rect(50 + (110)*i, 160 + (110)*(i//6), 100, 100)
                    if rect.collidepoint(pos[0], pos[1]):
                        print("Epic epic carpal tunner")
                        print(entity)
                        if entity in self.currentZone.allowedEnemies:
                            self.currentZone.allowedEnemies.remove(entity)
                        else:
                            self.currentZone.allowedEnemies.append(entity)


        if 600 <= pos[1] <= 650:
            for i,button in enumerate(self.audioButtons):
                xPos = 1280 / 2 - self.graphicsData["button-container-size"] / 2 + (95)*i
                if xPos <= pos[0] <= xPos + 75:
                    button[1]()


class LevelEditor(GenericScene):

    def __init__(self, screen, mainloop, directory: str = "") -> None:
        super().__init__(screen, mainloop)
        self.main_loop.add_key_binding(K_o, self.openDialog)
        self.main_loop.add_key_binding(K_s, self.save)
        self.main_loop.add_key_binding(K_n, self.newMap)
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
        self.main_loop.add_key_callback(K_RIGHT, lambda: self.timeline.incrementSong(100))
        self.main_loop.add_key_callback(K_LEFT, lambda: self.timeline.incrementSong(-100))


    def save(self) -> None:
        self.level.saveToPath()


    def newMap(self) -> None:
        # get name of map
        name = "test-new-map"
        _dir = f"levels/{name}"
        # copy audio file and set path
        top = Tk()
        top.withdraw()  # hide window
        file_name = filedialog.askopenfile(filetypes=[("Audio Files", ".mp3 .ogg .wav")], parent=top).name
        print(file_name)
        top.destroy()
        newAudio = f"{_dir}\\{file_name.split('/')[-1]}"
        shutil.copy(file_name, _dir)
        # create level object
        self.level = Level.newLevel(_dir, newAudio)
        self.timeline = Timeline(self.level)
        self.main_loop.add_key_callback(K_SPACE, self.timeline.resume, False)
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
