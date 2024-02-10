import pygame
from objects.enemy import GenericEnemy

class Necromancer(GenericEnemy):
    def __init__(self, x: float, y: float, sprite: str, damage: int, health: int) -> None:
        super().__init__(x, y, sprite, damage, health)

    def update(self):
        pass

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.sprite, (self.pos[0] - self.player_pos[1], self.pos[1] - self.player_pos[1]))