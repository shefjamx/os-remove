import pygame
from misc.settings import SCREEN_HEIGHT

class Particle(pygame.sprite.Sprite):
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
        super().__init__(groups)
        self.pos = pos
        self.color = color
        self.direction = direction
        self.speed = speed
        self.fade_duration = fade_duration
        self.size_multiplier = size
        self.trail = trail
        self.alpha = 255
        self.lifetime = 0 # lifetime in frames, each particle lives max 240 frames or 4 seconds

        self.create_surface()

    def fade(self, dt):
        self.alpha -= self.fade_duration * dt
        self.image.set_alpha(self.alpha)

    def check_life(self):
        """ 
        OVERRIDE for custom particle behaviour
        default behaviour particle dies after fade duration
        """
        if (self.alpha < 1):
            self.kill()
        return

    def create_surface(self):
        self.image = pygame.Surface((4 * self.size_multiplier, 20 * self.size_multiplier)).convert_alpha()
        self.image.set_colorkey("black") # makes black pixels transparent
        self.rect_obj = pygame.Rect(self.size_multiplier, self.size_multiplier, 2 * self.size_multiplier, 2*self.size_multiplier)
        
        # draw a trail
        if (self.trail):
            for i in range (1,5):
                surf = pygame.Surface((4,4))
                pygame.draw.rect(surf, self.color, self.rect_obj)
                surf.set_alpha(self.alpha / i)
                self.image.blit(surf, [0, 4*(5-i)])
            
        pygame.draw.rect(self.image, self.color, self.rect_obj)
        self.image.set_alpha(self.alpha)
        self.rect = self.image.get_rect(center=self.pos)
    
    def move(self, dt):
        """ 
        OVERRIDE for custom behaviour
        default behaviour particle continues in direction at constant speed 
        """ 
        self.pos += self.direction * self.speed * dt
        self.rect.center = self.pos

    def update(self, dt):
        self.move(dt)
        self.fade(dt)    
        self.check_life()