import pygame
from misc.logger import log

class Tileset:
    def __init__(self, file, size=(64, 64), start=0, stop=0, upscale=1) -> None:
        """
        Init a tile set
            file: file path relative to client (actual images must be on 1 line)
            size: tuple of size
            start: start of animation, zero indexed
            end: end of animation, zero indexed
            upscale: how much to upscale the image by
        """
        self.file = file
        self.size = size
        self.upscale = (size[0] * upscale, size[1] * upscale)
        self.image = pygame.image.load(file)
        self.rect = self.image.get_rect()
        self.tiles = []
        self.start = start
        self.stop = stop
        self.current_tile_index = start
        self.setup()

    def setup(self):
        """Import all images into the tileset"""
        log(f"Creating tileset for {self.file}", "debug")
        self.tiles = []
        w, _ = self.rect.size
        dx = self.size[0]

        for x in range(0, w, dx):
            tile = pygame.Surface(self.size, pygame.SRCALPHA, 32)
            tile = tile.convert_alpha()
            tile.blit(self.image, (0, 0), (x, 0, *self.size))
            tile = pygame.transform.scale(tile, self.upscale)
            self.tiles.append(tile)

    def increment(self) -> pygame.Surface:
        """Incrementally go through all tiles. Return the current tile"""
        tile = self.tiles[self.current_tile_index]
        if self.current_tile_index + 1 <= self.stop:
            self.current_tile_index += 1 
        else:
            self.current_tile_index = self.start
        return tile