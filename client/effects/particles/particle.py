import pygame
from misc.settings import SCREEN_HEIGHT, SCREEN_WIDTH

class Particle(pygame.sprite.Sprite):
    def __init__(self,
                groups: pygame.sprite.Group,
                pos: list[int],
                color: pygame.Color,
                direction: pygame.math.Vector2,
                speed: int,
                fade_speed: int
                 ):
        super().__init__(groups)
        self.pos = pos
        self.color = color
        self.direction = direction
        self.speed = speed
        self.fade_speed = fade_speed
        self.alpha = 255
        self.lifetime = 0 # lifetime in frames, each particle lives max 240 frames or 4 seconds

        self.create_surface()


    def fade(self, dt):
        self.alpha -= self.fade_speed * dt
        self.image.set_alpha(self.alpha)

    def check_life(self):
        if self.lifetime > 240:
            self.kill()

    def create_surface(self):
        self.image = pygame.Surface((4,4)).convert_alpha()
        self.image.set_colorkey("black") # makes black pixels transparent
        pygame.draw.rect(self.image, self.color, pygame.Rect(1,1, 2,2))
        self.rect = self.image.get_rect(center=self.pos)
    
    def move(self, dt):
        # update position based on direction and speed
        self.pos += self.direction * self.speed * dt
        self.rect.center = self.pos
        self.lifetime += 1

    def update(self, dt):
        self.move(dt)
        self.fade(dt)
        self.check_life()