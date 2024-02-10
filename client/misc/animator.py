import pygame
from misc.logger import log

class Tileset:
    def __init__(self, file, size=(64, 64), start=0, stop=0, upscale=1, callback=None) -> None:
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
        self.start = start
        self.stop = stop
        self.callback = callback

        self.image = pygame.image.load(file)
        self.rect = self.image.get_rect()
        self.tiles = []
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
            if self.callback:
                self.callback()
            self.current_tile_index = self.start
        return tile
    
    def reset(self):
        """Reset the tileset animation back to the start"""
        self.current_tile_index = self.start

class CachedTiles:
    def __init__(self) -> None:
        self.tiles = {}

    def getTile(self, entityName, animationName):
        """Returns a tile if one was found"""
        if entityName in self.tiles:
            if animationName in self.tiles[entityName]:
                return self.tiles[entityName][animationName]
        return None
    
    def addTile(self, entityName, animationName, override=False, *TilesetAttributes):
        if entityName in self.tiles:
            if animationName not in self.tiles[entityName] or override:
                self.tiles[entityName][animationName] = Tileset(*TilesetAttributes)
        else:
            self.tiles[entityName] = {animationName: Tileset(*TilesetAttributes)}