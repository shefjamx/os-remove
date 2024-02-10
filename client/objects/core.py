import pygame
from misc.animator import Tileset

class Core:

    def __init__(self, health: int, main_loop):
        self.main_loop = main_loop
        self.maxHealth = health
        self.currentHealth = health
        self.tilesets = {
            "idle": Tileset("assets\\images\\core\\FlyingObelisk_no_lightnings_no_letter.png", (200, 400), 0, 12)
        }
        self.tile_fps = {
            "idle": 12,
            "run": 12,
            "attack": 36
        }
        self.tileset = "idle"
        self.sprite = self.tilesets[self.tileset].increment()
        self.time_since_last_tile = 0

    def dealDamage(self, damage: float) -> None:
        self.currentHealth -= damage

    def getX(self) -> float:
        return 2560 / 2 - self.sprite.get_width() / 2

    def getY(self) -> float:
        return 1440 / 2 - self.sprite.get_height() / 1.5

    def getWidth(self) -> int:
        return self.sprite.get_width()

    def getHeight(self) -> int:
        return self.sprite.get_height()

    def getRect(self) -> pygame.Rect:
        return pygame.Rect(self.getX(), self.getY(), self.getWidth(), self.getHeight())

    def doDamage(self, damage: int) -> None:
        self.health -= damage

    def drawHealthBar(self, surface: pygame.Surface, playerPos) -> None:
        pygame.draw.line(surface, "#333333", (self.getX() + 136 - playerPos[0], self.getY() + 109 - playerPos[1]), (self.getX() + 150 - playerPos[0], self.getY() + 300 - playerPos[1]), 4)
        ratio = min(1 - (self.currentHealth / self.maxHealth), 1)
        startX = self.getX() + 136 - playerPos[0] + 14*ratio
        startY = self.getY() + 109 - playerPos[1] + 191*ratio
        color = "#00FF00" if ratio < 0.25 else "#FFFF00" if ratio < 0.5 else "#FFA500" if ratio < 0.75 else "#AA0000"
        pygame.draw.line(surface, color, (startX, startY), (self.getX() + 150 - playerPos[0], self.getY() + 300 - playerPos[1]), 1)

    def draw(self, surface: pygame.Surface, playerPos):
        posX, posY = self.getX(), self.getY()
        surface.blit(self.sprite, (posX - playerPos[0], posY - playerPos[1]))
        self.drawHealthBar(surface, playerPos)

    def tick(self):
        """Tick the player class, used to animate the player"""
        self.time_since_last_tile += self.main_loop.dt
        if self.time_since_last_tile >= 1 / self.tile_fps[self.tileset]:
            self.time_since_last_tile = 0
            self.sprite = self.tilesets[self.tileset].increment()
