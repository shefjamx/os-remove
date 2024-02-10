import pygame
from misc.animator import Tileset
from objects.worm import Worm

class Player(pygame.sprite.Sprite):
    def __init__(self, main_loop, scene) -> None:
        super().__init__()
        self.main_loop = main_loop
        self.scene = scene

        # Tileset
        self.tilesets = {
            "idle": Tileset("assets/images/player/idle.png", (80, 80), 0, 8, upscale=3),
            "run": Tileset("assets/images/player/run.png", (80, 80), 0, 5, upscale=3),
            "attack": Tileset("assets/images/player/attack.png", (80, 80), 0, 11, upscale=3, callback=lambda: self.set_tileset("idle"))
        }
        self.tile_fps = {
            "idle": 8,
            "run": 12,
            "attack": 36
        }
        self.tileset = "idle"
        self.time_since_last_tile = 0

        # Player
        self.surf = self.tilesets[self.tileset].increment()
        self.player_rect = self.surf.get_rect()
        self.x = 500
        self.y = 600
        self.size = (80, 80)

        # Attacking
        self.time_since_last_attack = 0
        self.min_attack_time = 0.1
        self.attack_amount = 100

        # Movement callbacks
        self.speed = 400
        self.flipped = False
        self.last_direction = "right"
        self.main_loop.add_key_callback(pygame.locals.K_s, lambda: self.change_position(0, self.speed, self.last_direction))
        self.main_loop.add_key_callback(pygame.locals.K_w, lambda: self.change_position(0, -self.speed, self.last_direction))
        self.main_loop.add_key_callback(pygame.locals.K_d, lambda: self.change_position(self.speed, 0, "right"))
        self.main_loop.add_key_callback(pygame.locals.K_a, lambda: self.change_position(-self.speed, 0, "left"))
        self.main_loop.add_key_callback(pygame.locals.K_k, lambda: self.attack(), False)
        self.main_loop.add_key_callback(pygame.locals.K_l, lambda: self.attack(), False)
        self.main_loop.add_keys_released_callback((pygame.locals.K_a, pygame.locals.K_d, pygame.locals.K_w, pygame.locals.K_s), lambda: self.set_tileset("idle") if self.tileset != "attack" else None)

    def set_tileset(self, tileset) -> None:
        self.tileset = tileset
        self.speed = 400

    def getRect(self) -> pygame.Rect:
        return self.surf.get_rect()

    def getX(self) -> float:
        return self.x

    def getY(self) -> float:
        return self.y

    def getWidth(self) -> float:
        return self.surf.get_width()

    def getHeight(self) -> float:
        return self.surf.get_height()

    def change_position(self, x_diff, y_diff, direction):
        """
        Increment/Decrement self.x and self.y
        Check that the player isn't about to go over a boundary first (kinda magic numbers honestly sorry)
        """
        # Movement
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

        # Directions and animations
        if self.last_direction != direction:
            self.last_direction = direction
            self.flipped = not self.flipped

        if self.tileset != "run" and self.tileset != "attack":
            self.tileset = "run"

    def attack(self):
        """Run the attack animation to attack and send a message to any enemy in the collision area"""
        if self.time_since_last_attack >= self.min_attack_time:
            self.time_since_last_attack = 0

            # Animations
            if self.tileset == "attack":
                self.tilesets[self.tileset].reset()
            self.tileset = "attack"
            self.speed = 200
            
            # Attempt to attack the enemies
            attack_rect = pygame.rect.Rect(555, 330, 170, 120)
            enemies_hit = self.scene.enemyHandler.detect_hit(attack_rect, (self.x - (self.player_rect.w / 2), self.y - (self.player_rect.h / 2)))
            if len(enemies_hit) >= 1:
                enemies_hit[-1].takeDamage(self.attack_amount)

    def tick(self):
        """Tick the player class, used to animate the player"""
        self.time_since_last_tile += self.main_loop.dt
        self.time_since_last_attack += self.main_loop.dt
        if self.time_since_last_tile >= 1 / self.tile_fps[self.tileset]:
            self.time_since_last_tile = 0
            self.surf = self.tilesets[self.tileset].increment()


