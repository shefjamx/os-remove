import math
import pygame
import numpy as np
from misc.settings import MAX_PARTICLES
from random import uniform, randint, choice, random
from effects.particles.particle import Particle



class FlameCirle():
    def __init__(self, speed: int, fade_speed: int, initial_pos: list[int], radius: int):
        self.speed_multiplier = speed # multiplier of the speed
        self.fade_speed = fade_speed
        self.initial_pos = initial_pos
        self.particle_group = pygame.sprite.Group()
        self.colours = [
            pygame.Color(255,0,0),
            pygame.Color(255,90,0),
            pygame.Color(255,154,0),
            pygame.Color(255,206,0),
            pygame.Color(255,232,8)
            ]
        self.radius = radius
        self.generate_particles()
        
    def generate_particles(self):
        for i in range(MAX_PARTICLES):
            # for the position calculate random point on circle
            direction = pygame.math.Vector2(uniform(-1,1), uniform(-1, 1))
            direction = direction.normalize()
            pos = self.initial_pos + (direction * self.radius)
            speed = randint(10 * self.speed_multiplier, 50 * self.speed_multiplier)
            Particle(groups=self.particle_group, pos=pos, color=choice(self.colours), direction=direction, speed=speed, fade_speed=self.fade_speed)

    def tick(self, display: pygame.Surface, dt):
        self.particle_group.update(dt)
        self.particle_group.draw(display)