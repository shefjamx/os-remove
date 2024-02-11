import pygame
from scenes.generic_scene import GenericScene
from objects.player import Player
from objects.level import Level
from objects.beat import BeatHitter

from objects.core import Core

from handlers.enemy import EnemyHandler

from effects.particles.flame.flame_effect import FlameCircle
from effects.particles.particle_themes import ICE

class PlayScene(GenericScene):
    def __init__(self, screen, main_loop, level_string: str) -> None:
        pygame.mixer.init()
        super().__init__(screen, main_loop)
        self.level = Level(level_string)
        self.musicChannel = pygame.mixer.music
        self.musicChannel.load(self.level.getSongPath())
        self.background_image = pygame.image.load("assets/images/main_level_3x.png")
        self.player = Player(main_loop, self)
        self.core = Core(10e3, self.main_loop)
        self.musicChannel.play()
        self.label_font = pygame.font.Font("assets/fonts/Abaddon Bold.ttf", 48)

        self.enemyHandler = EnemyHandler(1.0, self.level.zones[0], self.main_loop, self.player, self.core)
        self.playData = {
            "num-misses": 0,
            "total-score": 0,
            "highest-combo": 0,
            "current-combo": 0
        }

        self.main_loop.add_key_callback(pygame.locals.K_l, self.doPlayerAttack, False)
        self.main_loop.add_key_callback(pygame.locals.K_k, self.doPlayerAttack, False)

        self.flame = FlameCircle(25, 5, [self.player.getX(),self.player.getY()], 1, ICE)
        self.hitTimings = self.level.getHitTimings()
        self.beatHitter = BeatHitter(main_loop, main_loop.screen, self, 80)
        self.pastAttackOffsets = []

    def resetCombo(self) -> None:
        self.playData["highest-combo"] = max(self.playData["highest-combo"], self.playData["current-combo"])
        self.playData["current-combo"] = 0

    def doPlayerAttack(self) -> None:
        self.player.attack()
        if not self.hitTimings:
            return
        currentSongTime = self.musicChannel.get_pos()
        nextTiming = self.hitTimings[0]
        
        nextTimingScore = nextTiming.getScore(currentSongTime)
        # 0 indicates a miss, -1 indicates not hitting
        if nextTimingScore[1] == -1:
            return
        self.pastAttackOffsets.append(nextTimingScore[0])
        if nextTimingScore[1] == 0:
            self.shake()
            self.resetCombo()
        self.hitTimings.remove(nextTiming)
        self.playData["current-combo"] += 1
        print("Removed timing")
        

    def removeHitTimings(self, songPos: float) -> None:
        toRemove = []
        for timing in self.hitTimings:
            if timing.getTiming() < songPos:
                toRemove.append(timing)
            else:
                break
        for timing in toRemove:
            self.hitTimings.remove(timing)

    def tick(self):
        currentSongPos = self.musicChannel.get_pos()
        self.enemyHandler.tick(currentSongPos)
        self.removeHitTimings(currentSongPos)
        # Background
        self.display.blit(self.background_image, (-self.player.x, -self.player.y))
        self.core.draw(self.display, (self.player.x, self.player.y))
        self.core.tick()
        self.player.tick()
        self.enemyHandler.draw(self.display, self.player.x, self.player.y)
        self.display.blit(self.label_font.render(f"x{self.playData['current-combo']}", False, "#FFFFFF"), (0, 0))
        self.beatHitter.draw(self.display)

        self.flame.tick(self.display, self.main_loop.dt)
        return super().tick(self.player)
