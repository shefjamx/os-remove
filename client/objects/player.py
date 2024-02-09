import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, main_loop) -> None:
        super().__init__()
        self.main_loop = main_loop
        self.surf = pygame.Surface((75, 25))
        self.surf.fill((255, 255, 255))
        self.player_rect = self.surf.get_rect()
        self.player_rect.x = 500
        self.player_rect.y = 600

        # Movement callbacks
        self.speed = 5
        self.main_loop.add_key_callback(pygame.locals.K_s, lambda: self.player_rect.move_ip(0, self.speed))
        self.main_loop.add_key_callback(pygame.locals.K_w, lambda: self.player_rect.move_ip(0, -self.speed))
        self.main_loop.add_key_callback(pygame.locals.K_d, lambda: self.player_rect.move_ip(self.speed, 0))
        self.main_loop.add_key_callback(pygame.locals.K_a, lambda: self.player_rect.move_ip(-self.speed, 0))
    
