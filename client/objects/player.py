import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, main_loop) -> None:
        super().__init__()
        self.main_loop = main_loop
        self.surf = pygame.Surface((75, 25))
        self.surf.fill((255, 255, 255))
        self.player_rect = self.surf.get_rect()
        self.x = 500
        self.y = 600

        # Movement callbacks
        self.speed = 400
        self.main_loop.add_key_callback(pygame.locals.K_s, lambda: self.change_position(0, self.speed))
        self.main_loop.add_key_callback(pygame.locals.K_w, lambda: self.change_position(0, -self.speed))
        self.main_loop.add_key_callback(pygame.locals.K_d, lambda: self.change_position(self.speed, 0))
        self.main_loop.add_key_callback(pygame.locals.K_a, lambda: self.change_position(-self.speed, 0))

    def change_position(self, x_diff, y_diff):
        """
        Increment/Decrement self.x and self.y
        Check that the player isn't about to go over a boundary first (kinda magic numbers honestly sorry)
        """
        x_diff *= self.main_loop.dt
        y_diff *= self.main_loop.dt

        if self.x >= -600 and x_diff < 0:
            self.x += x_diff
        elif self.x <= 1880 and x_diff > 0:
            self.x += x_diff

        if self.y >= -320 and y_diff < 0:
            self.y += y_diff
        elif self.y <= 1040 and y_diff > 0:
            self.y += y_diff
    
