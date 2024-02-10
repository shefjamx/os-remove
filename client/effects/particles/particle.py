import pygame
from misc.settings import SCREEN_HEIGHT, SCREEN_WIDTH

class Particle(pygame.sprite.Sprite):
    def __init__(self,
                groups: pygame.sprite.Group,
                pos: list[int],
                color: pygame.Color,
                direction: pygame.math.Vector2,
                speed: int,
                fade_speed: int,
                size_multiplier: int,
                should_die: bool,
                max_life: int
                 ):
        super().__init__(groups)
        self.pos = pos
        self.color = color
        self.direction = direction
        self.speed = speed
        self.fade_speed = fade_speed
        self.size_multiplier = size_multiplier
        self.should_die = should_die
        self.alpha = 255
        self.max_life = max_life
        self.lifetime = 0 # lifetime in frames, each particle lives max 240 frames or 4 seconds

        self.create_surface()

    def fade(self, dt):
        self.alpha -= self.fade_speed * dt
        self.image.set_alpha(self.alpha)

    def check_life(self):
        if self.should_die:
            if self.lifetime > self.max_life:
                self.kill()
        else:
            # reset back to top
            if (self.pos[1] > SCREEN_HEIGHT):
                self.pos[1] = 0

    def create_surface(self):
        self.image = pygame.Surface((16,16)).convert_alpha()
        self.image.set_colorkey("black") # makes black pixels transparent
        self.rect_obj = pygame.Rect(self.size_multiplier, self.size_multiplier, 2 * self.size_multiplier, 2*self.size_multiplier)
        pygame.draw.rect(self.image, self.color, self.rect_obj)
        self.image.set_alpha(self.alpha)
        self.rect = self.image.get_rect(center=self.pos)
    
    def move(self, dt):
        # update position based on direction and speed
        self.pos += self.direction * self.speed * dt
        self.rect.center = self.pos
        if self.image.get_height() > 4:
            print(self.image.get_height())

    def update(self, dt):
        self.move(dt)
        self.fade(dt)    
        self.lifetime += 1
        self.check_life()