import pygame

class GenericEnemy:

    def __init__(self, x: float, y: float, sprite: str, damage: int, health: int) -> None:
        self.pos = [x, y]
        self.sprite = pygame.image.load(sprite)
        self.damage = damage
        self.health = health

    def update(self) -> None:
        # run ai :D
        raise NotImplementedError("Please add ai to ur monster goofy goober")

    def render(self) -> None:
        # draw da enemy
        raise NotImplementedError("Please draw ur monster silly billy")
    
    def takeDamage(self, damageNum: float) -> bool:
        """
        Returns true if the monster is still alive
        """
        self.health -= damageNum
        return self.health > 0