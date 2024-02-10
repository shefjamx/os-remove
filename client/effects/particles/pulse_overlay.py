# on beat pulse a random set of particles
import pygame
from tweener import *

from effects.particles.particle import Particle
from random import uniform, randint, choice
from misc.settings import MAX_PARTICLES, SCREEN_HEIGHT, SCREEN_WIDTH

N_PULSE = 20 # pulse 20 particles

class PulseEffect():
    def __init__(self, pulse_duration: int, pulse_intensity: int, N_PARTICLES: int):
        self.alpha = 100 # low opacity
        self.fade_speed = 0
        self.color = pygame.Color(255,255,255) # white is default
        self.particle_group = pygame.sprite.Group()
        self.pulse_duration = pulse_duration
        self.pulse_intensity = pulse_intensity
        self.N_PARTICLES = N_PARTICLES

        self.max_life = pulse_duration / 16.67
        self.speed_multiplier = SCREEN_HEIGHT / self.max_life


        self.generate_particles()


    def generate_particles(self):
        for i in range(self.N_PARTICLES):
            # for the position calculate random point on circle
            direction = pygame.math.Vector2(0, 1)
            direction = direction.normalize()
            pos = [
                randint(0, SCREEN_WIDTH), 
                0 
                ]
            Particle(groups=self.particle_group, 
                    pos=pos, 
                    color=self.color, 
                    direction=direction,
                    speed=self.speed_multiplier, 
                    fade_speed=self.fade_speed, 
                    size_multiplier=1, 
                    should_die=True,
                    max_life=20000
                    )
            
            self.pulse()
        


    def tick(self, display: pygame.Surface, dt):
        self.particle_group.update(dt)
        self.particle_group.draw(display)

    def pulse(self):
        # select random N_PULSE particles
        sprites = self.particle_group.sprites()
        for i in range(N_PULSE):
            sprite = sprites[randint(0, len(sprites) - 1)] 
            # start the tween
            sprite.size_multiplier = 4
            sprite.rect_obj.scale_by(2,2)

            

