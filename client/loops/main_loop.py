import pygame
import sys

from pygame.locals import (
    K_w,  # Forwards
    K_a,  # Left
    K_s,  # Down
    K_d,  # Right
    K_k,  # Beat button 1
    K_l,  # Beat button 2
    KEYDOWN,
    QUIT
)

from misc.pos import Pos
from scenes.generic_scene import GenericScene
from scenes.home import HomeScreen

class MainLoop():
    """Main Loop class, this will handle all keyboard inputs and generic stuff (that i've not figured out yet)"""

    def __init__(self, screen) -> None:
        self.running = False
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.current_scene: GenericScene = HomeScreen(screen)

    def change_scene(self, scene: GenericScene):
        self.current_scene = scene

    def start(self) -> None:
        """
        Start the main game loop:
        """
        self.running = True
        while self.running:
            # Event loop
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                    sys.exit()

                # Clicks
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    self.current_scene.handle_click(pos)

                # Keydown
                if event.type == KEYDOWN:
                    if event.key == K_w:
                        pass # Move Forwards
                    elif event.key == K_a:
                        pass # Move right
                    elif event.key == K_s:
                        pass # Move right
                    elif event.key == K_d:
                        pass # Move right
                    elif event.key == K_k:
                        pass # Move right
                    elif event.key == K_l:
                        pass # Move right

            # Re-render the screen
            if self.current_scene is not None:
                self.current_scene.tick()

            # Tick clock at 120fps
            self.clock.tick(120)

        # Game is over
        pygame.quit()
