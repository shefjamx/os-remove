import pygame

class Core:

    def __init__(self, health: int):
        self.health = health
        self.sprite = pygame.image.load("assets\\images\\core_draft.png").convert()
    
    def doDamage(self, damage: int) -> None:
        self.health -= damage

    def draw(self, surface: pygame.Surface, pos, player):
        posX, posY = (pos[0] + self.sprite.get_width()) / 2, (pos[1] + self.sprite.get_height()) / 2
        posX -= player.x
        posY -= player.y
        surface.blit(self.sprite, (posX, posY))