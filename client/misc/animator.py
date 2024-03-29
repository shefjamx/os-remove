import pygame
from misc.logger import log

class Tileset:
    def __init__(self, mainLoop, file, size=(64, 64), start=0, stop=0, upscale=1, callback=None, reverse=False, max_repeat=0) -> None:
        """
        Init a tile set
            file: file path relative to client (actual images must be on 1 line)
            size: tuple of size
            start: start of animation, zero indexed
            end: end of animation, zero indexed
            upscale: how much to upscale the image by
        """
        self.mainLoop = mainLoop
        self.file = file
        self.size = size
        self.upscale = (size[0] * upscale, size[1] * upscale)
        self.start = start
        self.stop = stop
        self.callback = callback
        self.reverse = reverse
        self.current_tile_index = start
        self.max_repeat = max_repeat
        self.repeats = 0

        if mainLoop.cachedImages.getImage(file) is None:
            self.image = pygame.image.load(file)
            self.tiles = []
            self.rect = self.image.get_rect()
            self.setup()
        else:
            cachedImage = mainLoop.cachedImages.getImage(file)
            self.image = cachedImage["image"]
            self.tiles = cachedImage["tiles"]
            self.rect = self.image.get_rect()

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

        self.mainLoop.cachedImages.addImage(self.file, {"image": self.image, "tiles": self.tiles})

    def increment(self, poggersEntity=None) -> pygame.Surface:
        """Incrementally go through all tiles. Return the current tile"""
        tile = self.tiles[self.stop - self.current_tile_index] if self.reverse else self.tiles[self.current_tile_index]
        if self.current_tile_index + 1 <= self.stop:
            self.current_tile_index += 1 
        else:
            if self.callback:
                self.callback()
            self.current_tile_index = self.start
            self.repeats += 1
        
        if self.repeats >= self.max_repeat and self.max_repeat > 0:
            log("Hit max repeats", "warning")
            if poggersEntity:
                poggersEntity.forceKill()
        
        return tile
    
    def reset(self):
        """Reset the tileset animation back to the start"""
        self.current_tile_index = self.start

class CachedImages:
    def __init__(self) -> None:
        self.images = {}

    def getImage(self, filename):
        if filename in self.images:
            return self.images[filename]
        return None

    def addImage(self, filename, image):
        if filename not in self.images:
            self.images[filename] = image
