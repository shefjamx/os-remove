import pygame

class GenericScene:
    """A Generic Scene class for all other scenes to inherit from"""
    def __init__(self, screen, main_loop) -> None:
        self.screen = screen
        self.main_loop = main_loop

    def tick(self):
        """Re-render the scene"""
        pygame.display.flip()

    def handle_click(self, mouse):
        """
        Handle a click.
        Default implementation is to ignore a click
        """
        pass