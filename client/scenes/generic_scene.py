import pygame

class GenericScene:
    """A Generic Scene class for all other scenes to inherit from"""
    def __init__(self, screen) -> None:
        self.screen = screen

    def tick(self):
        """Re-render the scene"""
        pygame.display.flip()