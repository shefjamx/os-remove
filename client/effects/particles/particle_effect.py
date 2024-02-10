import pygame

# all particle effects inherit these properties
class ParticleEffect():
    def __init__(self, theme: list[pygame.Color]):
        self.colours = theme 
        self.particle_group = pygame.sprite.Group()

    def generate_particles(self):
        """ OVERRIDE FOR CUSTOM EFFECTS """
        return

    def tick(self, display: pygame.Surface, dt: float):
        self.particle_group.draw(display)
        self.particle_group.update(dt)
