from typing import Optional
import pygame

class Ray:

    def __init__(self, initialPoint, rect: pygame.Rect) -> None:
        self.point = initialPoint
        self.rect = rect

    def cast(self) -> Optional[tuple[float, float]]:
        newline = self.rect.clipline(self.point[0], self.point[1], self.rect.centerx, self.rect.centery)
        if not newline:
            return None
        if self.point[0] <= self.rect.centerx:
            return newline[0]
        else:
            return newline[1]
