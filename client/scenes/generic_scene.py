import pygame
import time
import random
from misc.settings import DIMENSIONS, MS_PER_FRAME

class GenericScene:
    """A Generic Scene class for all other scenes to inherit from"""
    def __init__(self, screen, main_loop) -> None:
        self.screen = screen
        self.display = pygame.Surface(DIMENSIONS)
        self.shake_offset = [0, 0]
        self.shake_duration = 0
        self.shake_amplitude = 0
        self.main_loop = main_loop
        self.time_difference = 0 

    def tick(self, player = None, particle_effect = None):
        """Re-render the scene"""
        # RENDER EVERYTHING ON self.display

        if self.shake_duration <= 2 and self.shake_amplitude != 0:
            self.stop_shake()
        elif self.shake_duration > 2:
            self.shake()

        self.screen.blit(self.display, self.shake_offset)
        if player:
            self.screen.blit(pygame.transform.flip(player.surf, player.flipped, False), [640 - player.player_rect.w/2, 360 - player.player_rect.h/2])
        if particle_effect:
            particle_effect.tick(self.screen, self.main_loop.dt)
        pygame.display.flip()
    
    def handle_click(self, mouse):
        """
        Handle a click.
        Default implementation is to ignore a click
        """
        pass

    def start_shake(self, intensity: int, amplitude: int):
        """
        Starts the screen shake animation
        intensity: int
            length of screen shake in frames
        amplitude: int
            maximum offset value for the shake
        """
        self.time_difference = time.time()
        self.shake_duration = round(intensity / MS_PER_FRAME) # milliseconds to frames
        self.shake_amplitude = amplitude

    def shake(self):
        """ 
        Shakes the screen 
            amplitude: int
            maximum offset value for the shake
        """
        amplitude_offset = (self.shake_amplitude / 2)
        self.shake_offset[0] = random.randint(0, self.shake_amplitude) - amplitude_offset
        self.shake_offset[1] = random.randint(0, self.shake_amplitude) - amplitude_offset
        self.shake_duration -= 1

    def stop_shake(self):
        """Stops screen shake"""
        self.shake_duration = 0
        self.shake_offset = [0,0]
        self.shake_amplitude = 0
        self.time_difference = time.time() - self.time_difference # ms diff
    
