from effects.particles.particle_effect import ParticleEffect
import pygame
from misc.settings import MAX_PARTICLES
from random import uniform, choice, randint

from effects.particles.flame.flame_particle import FlameParticle
class FlameCircle(ParticleEffect):
    def __init__(self, max_speed: int, fade_duration: int, initial_pos: list[int], radius: int, theme: list[pygame.Color]):
        super().__init__(theme)
        self.max_speed = max_speed
        self.fade_duration = fade_duration
        self.initial_pos = initial_pos
        self.radius = radius
        
        self.generate_particles()

        
    def generate_particles(self):
        for i in range(MAX_PARTICLES):
            # for the position calculate random point on circle
            direction = pygame.math.Vector2(uniform(-1,1), uniform(-1, 1))
            direction = direction.normalize()
            pos = self.initial_pos + (direction * self.radius)
            FlameParticle(
                groups=self.particle_group,
                pos=pos,
                color=choice(self.colours),
                direction=direction,
                speed=self.max_speed,
                fade_duration=randint(round(self.fade_duration / 1.5), self.fade_duration),
                size=1,
                trail=False
            )