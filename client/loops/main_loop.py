import pygame
import sys

from pygame.locals import (
    KEYDOWN,
    KEYUP,
    QUIT
)

from misc.logger import log
from scenes.generic_scene import GenericScene
from scenes.home import HomeScreen
# from scenes.level import LevelScene

class MainLoop():
    """Main Loop class, this will handle all keyboard inputs and generic stuff (that i've not figured out yet)"""

    def __init__(self, screen) -> None:
        self.running = False
        self.keyMap: dict = {}
        self.pressedKeys = []
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.current_scene: GenericScene = HomeScreen(screen, self)
        # self.current_scene: GenericScene = LevelScene(screen, self, "ascension-to-heaven")

    def change_scene(self, scene: GenericScene):
        log(f"Changing scenes to: {scene}", type="debug")
        self.current_scene = scene(self.screen, self)
        pygame.display.flip()

    def add_key_callback(self, key: int, callback) -> None:
        """
        Registers a callback to be called when the given keycode is registered as pressed
        If there is already a callback registered then it is removed :D Dont care!!!

        Parameters:
            key[int]: The python.locals keycode used for the key
            callback[callable]: The function to be called
        TODO: Do we want there to be multiple callbacks for one keycode?
        """
        self.keyMap[key] = callback

    def remove_key_callback(self, key: int) -> None:
        """
        Removes a created callback function
        """
        del self.keyMap[key]
    

    def dispatchKeyCallback(self, key: int) -> None:
        if key in self.keyMap:
            # call the button callback
            self.keyMap[key]()

    
    def start(self) -> None:
        """
        Start the main game loop:
        """
        self.running = True
        while self.running:
            # Event loop
            for key in self.pressedKeys:
                self.dispatchKeyCallback(key)
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                    sys.exit()

                # Clicks
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    self.current_scene.handle_click(pos)

                # call held down keys
                # Keydown / up commands
                if event.type == KEYDOWN:
                    self.pressedKeys.append(event.key)
                    self.dispatchKeyCallback(event.key)
                elif event.type == KEYUP:
                    self.pressedKeys.remove(event.key)


            # Re-render the screen
            if self.current_scene is not None:
                self.current_scene.tick()

            # Tick clock at 120fps
            self.clock.tick(60)

        # Game is over
        pygame.quit()
