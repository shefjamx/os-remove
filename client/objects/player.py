import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.surf = pygame.Surface((75, 25))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()

    
