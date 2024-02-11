import pygame
import sys

from pygame.locals import (
    KEYDOWN,
    KEYUP,
    QUIT,
    K_LCTRL
)

from misc.logger import log
from misc.settings import FPS
from misc.animator import CachedImages
from scenes.generic_scene import GenericScene
from scenes.home import HomeScreen
from scenes.editor import LevelEditor
from scenes.play import PlayScene
from scenes.connect import ConnectScene
from misc.settings import ADDRESS, PORT
import time

from network.client import Client

class MainLoop():
    """Main Loop class, this will handle all keyboard inputs and generic stuff (that i've not figured out yet)"""

    def __init__(self, screen) -> None:
        self.running = False
        self.keyMap: dict = {}
        self.keyBindingMap: dict = {}
        self.pressedKeys = []
        self.monitoredKeys = {}
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.cachedImages: CachedImages = CachedImages()

        self.current_scene: GenericScene = HomeScreen(screen, self)
        #self.current_scene: GenericScene = PlayScene(screen, self, "ascension-to-heaven", time.time() + 5, debug=True)
        #self.current_scene: GenericScene = PlayScene(screen, self, "cover-femboy-friday", time.time() + 5, debug=True)
        #self.current_scene: GenericScene = LevelEditor(screen, self, "anybody-can-find-love")
        self.dt = 0

        log("Creating client")
        self.client = Client(ADDRESS, PORT, self)
        log("Created client")

    def change_scene(self, scene: GenericScene, *args):
        log(f"Changing scenes to: {scene}", type="debug")
        print(args)
        self.current_scene = scene(self.screen, self, *args)
        pygame.display.flip()

    def add_key_binding(self, key: int, callback) -> None:
        self.keyBindingMap[key] = callback

    def add_key_callback(self, key: int, callback, onHold=True) -> None:
        """
        Registers a callback to be called when the given keycode is registered as pressed
        If there is already a callback registered then it is removed :D Dont care!!!

        Parameters:
            key[int]: The python.locals keycode used for the key
            callback[callable]: The function to be called
        TODO: Do we want there to be multiple callbacks for one keycode?
        """
        self.keyMap[key] = (callback, onHold)

    def remove_key_callback(self, key: int) -> None:
        """
        Removes a created callback function
        """
        del self.keyMap[key]


    def add_keys_released_callback(self, keys: tuple[int], callback) -> None:
        self.monitoredKeys[keys] = callback


    def dispatchKeyCallback(self, key: int) -> None:
        if key in self.keyMap:
            # call the button callback
            self.keyMap[key][0]()


    def start(self) -> None:
        """
        Start the main game loop:
        """
        self.running = True
        while self.running:
            # Tick clock at 60 fps
            self.dt = self.clock.tick(FPS) / 1000

            # Event loop
            for key in self.pressedKeys:
                self.dispatchKeyCallback(key)
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                    sys.exit()

                # input boxes handle events differently
                if isinstance(self.current_scene, ConnectScene):
                    self.current_scene.handle_menu_input(event)

                # Clicks
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    self.current_scene.handle_click(pos)

                # call held down keys
                # Keydown / up commands
                if event.type == KEYDOWN:
                    self.dispatchKeyCallback(event.key)
                    if event.key in self.keyMap and self.keyMap[event.key][1]:
                        self.pressedKeys.append(event.key)
                elif event.type == KEYUP:
                    if event.key in self.keyMap and self.keyMap[event.key][1]:
                        self.pressedKeys.remove(event.key)
                    for keyCollection in self.monitoredKeys:
                        if event.key in keyCollection and not any(key in self.pressedKeys for key in keyCollection):
                            self.monitoredKeys[keyCollection]()
                    if pygame.key.get_mods() & K_LCTRL and event.key in self.keyBindingMap:
                        self.keyBindingMap[event.key]()


            # Re-render the screen
            if self.current_scene is not None:
                self.current_scene.tick()

        # Game is over
        pygame.quit()
