from objects.level import Level
import pygame

class LevelHandler:

    def __init__(self, mainLoop, callbackFunc):
        self.allLevels = sorted(Level.allLevels(), key=lambda x: x.name)
        self.mainLoop = mainLoop
        self.callbackFunc = callbackFunc
        self.mainLoop.add_key_callback(pygame.locals.K_RIGHT, lambda: self.incrementSelection(1), False)
        self.mainLoop.add_key_callback(pygame.locals.K_LEFT, lambda: self.incrementSelection(-1), False)
        self.mainLoop.add_key_callback(pygame.locals.K_RETURN, lambda: self.dispatchCallback(), False)
        self.label_font = pygame.font.Font("assets/fonts/Abaddon Bold.ttf", 48)

        self.currentLevel = 0

    def incrementSelection(self, amt) -> None:
        self.currentLevel += amt
        self.currentLevel = self.currentLevel % len(self.allLevels)
        pygame.mixer.music.load(self.allLevels[self.currentLevel].getSongPath())
        pygame.mixer.music.play()

    def dispatchCallback(self) -> None:
        print("Doing thing")
        self.callbackFunc(self.allLevels[self.currentLevel])

    def createLevelRect(self, level, i) -> pygame.Rect:
        LEVEL_WIDTH = 500
        LEVEL_HEIGHT = 100
        LEVEL_MARGIN = 10
        return pygame.Rect((self.mainLoop.screen.get_width() - LEVEL_WIDTH ) / 2, 200 + (LEVEL_HEIGHT + LEVEL_MARGIN)*i, LEVEL_WIDTH, LEVEL_HEIGHT)

    def draw(self, surface):
        for i,level in enumerate(self.allLevels):
            rect = self.createLevelRect(level, i)
            color = "#FF0000" if not self.currentLevel == i else "#00FF00"
            pygame.draw.rect(surface, color, rect)
            title = self.label_font.render(level.name, False, "#FFFFFF")
            surface.blit(title, (rect.x + (rect.w - title.get_width()) / 2, rect.y + 10))
