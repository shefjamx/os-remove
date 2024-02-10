from effects.particles.particle import Particle
from tweener import *
from random import randint
import pygame

class FlameParticle(Particle):
    def __init__(self,
                groups: pygame.sprite.Group,
                pos: list[int],
                color: pygame.Color,
                direction: pygame.math.Vector2,
                speed: int,
                fade_duration: int,
                size: int,
                trail: bool
                ):
        super().__init__(groups, pos, color, direction, speed, fade_duration, size, trail)
        self.init_speed = round(self.speed / 4)
        self.max_speed = self.speed
        self.tween_speed = Tween(
            begin=self.init_speed,
            end=self.max_speed,
            duration=randint(700, 1200), # random life 
            easing=Easing.EXPO,
            easing_mode=EasingMode.IN_OUT,
            boomerang=False,
            loop=False
        )
        self.tween_speed.start()


    def move(self, dt):
        # custom movement
        # gradually increase speed till reaces max
        self.tween_speed.update()
        self.pos += self.direction * self.tween_speed.value
        self.rect.center = self.pos
