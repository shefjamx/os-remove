import pygame
from pygame.sprite import _Group

class Particle(pygame.sprite.Sprite):
    def __init__(self,
                groups: pygame.sprite.Group,
                pos: list[int],
                color: pygame.Color,
                direction: pygame.math.Vector2,
                speed: int
                 ):
        super().__init__(groups)
        self.pos = pos
        self.color = color
        self.direction = direction
        self.speed = speed

        self.create_surface()

    def create_surface(self):
        self.image = pygame.Surface((4,4)).convert_alpha()
        self.image.set_colorkey("black") # makes black pixels transparent
        pygame.draw.rect(surface=self.image, color=self.color, width = 2)
        self.rect = self.image.get_rect(center=self.pos)
    
    def move(self, dt):
        # update position based on direction and speed
        self.pos += self.direction * self.speed * dt
        self.rect.center = self.pos

    def update(self, dt):
        self.move(dt)