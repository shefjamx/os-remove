import pygame
import sys

class MainLoop():
    """Main Loop class, this will handle all keyboard inputs and generic stuff (that i've not figured out yet)"""

    def __init__(self, screen) -> None:
        self.running = False
        self.screen = screen

    def start(self) -> None:
        """
        Start the main game loop:
        """
        self.running = True
        while self.running:
            # Event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    sys.exit()  # Stops the full python file - may fuck up stuff in future

            # Draw some stuff
            self.screen.fill((255, 255, 255))
            
        # Game is over
        pygame.quit()
