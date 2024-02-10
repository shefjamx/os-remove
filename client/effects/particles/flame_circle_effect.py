import pygame
from misc.settings import MAX_PARTICLES
from random import uniform, randint, choice
from particles.particle import Particle


class FlameCirle():
    def __init__(self, speed: int, initial_pos: list[int]):
        self.speed = speed # multiplier of the speed
        self.initial_pos = initial_pos
        self.particle_group = pygame.sprite.Group()
        self.colours = [
            pygame.Color(255,0,0),
            pygame.Color(255,90,0),
            pygame.Color(255,154,0),
            pygame.Color(255,206,0),
            pygame.Color(255,232,8)
            ]
        
    def generate_particles(self):
        for i in range(MAX_PARTICLES):
            direction = pygame.math.Vector2(uniform(-1,1), uniform(-1, 1))
            direction = direction.normalize()
            speed = randint(50, speed)
            Particle(self.particle_group, self.initial_pos, choice(self.colours), direction, speed)

    def tick(self, display: pygame.Surface, dt):
        self.particle_group.draw(display)
        self.particle_group.update(dt)