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
from scenes.level import LevelScene

class MainLoop():
    """Main Loop class, this will handle all keyboard inputs and generic stuff (that i've not figured out yet)"""

    def __init__(self, screen) -> None:
        self.running = False
        self.keyMap: dict = {}
        self.screen = screen
        self.clock = pygame.time.Clock()
        #self.current_scene: GenericScene = HomeScreen(screen, self)
        self.current_scene: GenericScene = LevelScene(screen, self, "ascension-to-heaven")

    def change_scene(self, scene: GenericScene):
        self.current_scene = scene(self.screen, self)

    def addKeyCallback(self, key: int, callback) -> None:
        """
        Registers a callback to be called when the given keycode is registered as pressed
        If there is already a callback registered then it is removed :D Dont care!!!

        Parameters:
            key[int]: The python.locals keycode used for the key
            callback[callable]: The function to be called
        TODO: Do we want there to be multiple callbacks for one keycode? Also add support for held keys!
        """
        self.keyMap[key] = callback

    def removeKeyCallback(self, key: int) -> None:
        """
        Removes a created callback function
        """
        del self.keyMap[key]


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
                    if event.key in self.keyMap:
                        # call the button callback
                        self.keyMap[event.key]()

            # Re-render the screen
            if self.current_scene is not None:
                self.current_scene.tick()

            # Tick clock at 120fps
            self.clock.tick(120)

        # Game is over
        pygame.quit()
