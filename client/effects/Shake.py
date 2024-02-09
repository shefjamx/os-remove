import pygame
from itertools import repeat

class Shake():
    def __init__(self, surface: pygame.Surface) -> None:
        self.surface = surface
        self.offset = repeat((0,0))

    def screen_shake(self, intensity: int, amplitude: int):
        s = -1
        for i in range(0,3):
            for x in range (0, amplitude, intensity):
                yield x * s, 0
            for x in range (amplitude, 0, intensity):
                yield x * s, 0
            s *= -1
        while True:
            yield 0,0
