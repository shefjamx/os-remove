import pygame
import time
from scenes.generic_scene import GenericScene
from scenes.end import EndScene
from objects.player import Player
from objects.level import Level
from objects.beat import BeatHitter
import math

from objects.core import Core

from handlers.enemy import EnemyHandler
from misc.logger import log

from effects.particles.flame.flame_effect import FlameCircle
from effects.particles.particle_themes import ICE

class PlayScene(GenericScene):
    def __init__(self, screen, main_loop, level_string: str, epochStart: float, debug=True) -> None:
        pygame.mixer.init()
        super().__init__(screen, main_loop)
        self.level = Level(level_string)
        self.startMapAt = epochStart
        self.isDebug = debug
        self.musicChannel = pygame.mixer.music
        self.musicChannel.load(self.level.getSongPath())
        self.background_image = pygame.image.load("assets/images/main_level_3x.png")
        self.player = Player(main_loop, self)
        self.player.min_attack_time = self.level.playerAttackSpeed
        
        self.cores = [Core(10e3, 0, 0, self.main_loop), Core(10e3, 0, 0, self.main_loop)]
        offsetX, coreY = self.background_image.get_width() / 2.5, 2162 / 2 - self.cores[0].sprite.get_height() / 1.5
        self.cores[0].setPos((offsetX, coreY))
        self.cores[1].setPos((self.background_image.get_width() - offsetX - 100, coreY))
        self.cores[0].setCallback(lambda: self.death())
        self.cores[1].setCallback(lambda: self.death())
        
        self.hasStarted = False
        if debug:
            self.musicChannel.play()
        self.label_font = pygame.font.Font("assets/fonts/Abaddon Bold.ttf", 48)

        self.currentZone = 0
        self.enemyHandler = EnemyHandler(1.0, self.level.zones[self.currentZone], self.main_loop, self.player, self.cores)
        self.playData = {
            "num-misses": 0,
            "total-score": 0,
            "highest-combo": 0,
            "current-combo": 0
        }

        self.main_loop.add_key_callback(pygame.locals.K_l, self.doPlayerAttack, False)
        self.main_loop.add_key_callback(pygame.locals.K_k, self.doPlayerAttack, False)

        self.flame = FlameCircle(25, 5, [self.player.getX(),self.player.getY()], 1, ICE)
        self.hitTimings = self.level.getHitTimings().copy()
        self.beatHitter = BeatHitter(main_loop, main_loop.screen, self, self.level.bpm)
        self.pastAttackOffsets = []

    def death(self):
        self.main_loop.client.broadcast_death()

    def endGame(self, value):
        log("Player died", "debug")
        pygame.mixer.music.stop()
        self.cores = []
        self.main_loop.change_scene(EndScene, value)

    def resetCombo(self) -> None:
        self.playData["highest-combo"] = max(self.playData["highest-combo"], self.playData["current-combo"])
        self.playData["current-combo"] = 0
    
    def getNearestTiming(self):
        prevTimingDiff = 99999999999
        for i,timing in enumerate(self.hitTimings):
            timingDiff = abs(timing.getTiming() - self.musicChannel.get_pos())
            if timingDiff > prevTimingDiff:
                return self.hitTimings[i-1]
            prevTimingDiff = timingDiff

    def doPlayerAttack(self) -> None:
        self.player.setAttackAnimation()
        self.beatHitter.deleteNearest()
        if not self.hitTimings:
            self.player.attack(0.25)
            return
        currentSongTime = self.musicChannel.get_pos()
        timingToHit = self.getNearestTiming()

        nextTimingScore = timingToHit.getScore(currentSongTime)
        # 0 indicates a miss, -1 indicates not hitting
        self.player.attack()
        if nextTimingScore[1] == -1:
            return
        self.beatHitter.deleteNearest()
        
        self.pastAttackOffsets.append(nextTimingScore[0])
        if nextTimingScore[1] == 0:
            self.shake()
            self.resetCombo()
        self.hitTimings.remove(timingToHit)
        self.playData["current-combo"] += 1

        self.updateEnemySpawnMultiplier()

    def updateEnemySpawnMultiplier(self):
        NUM_POINTS = min(6, len(self.pastAttackOffsets))
        avgHitTime = sum(self.pastAttackOffsets[-NUM_POINTS:]) / NUM_POINTS
        avgHitTime = 10 - max(min(avgHitTime, 75), 25) / 10
        mult = 1 + 0.05 * math.e ** (0.9*avgHitTime - 4)
        self.main_loop.client.send_spawn_rate(mult)
        print(f"Enemy spawn multiplier: {mult}")

    def removeHitTimings(self, songPos: float) -> None:
        toRemove = []
        for timing in self.hitTimings:
            if (timing.getTiming() + (120/self.level.bpm)*1000) < songPos:
                toRemove.append(timing)
            else:
                break
        for timing in toRemove:
            self.hitTimings.remove(timing)

    def tick(self):
        if not self.isDebug and time.time() < self.startMapAt:
            timeToStart = self.startMapAt - time.time()
            self.display.fill("#000000")
            text = self.label_font.render(f"{timeToStart:.2f}s till start", False, "#FFFFFF")
            self.display.blit(text, (0, 0))
            return super().tick()
        if not self.hasStarted:
            self.musicChannel.play()
            self.hasStarted = True
        currentSongPos = self.musicChannel.get_pos()
        self.enemyHandler.tick(currentSongPos)
        zoneTime = self.level.zones[self.currentZone].getTimings()[1]
        if zoneTime <= currentSongPos and zoneTime != -1:
            self.currentZone = min(self.currentZone + 1, len(self.level.zones))
            self.enemyHandler.setZone(self.level.zones[self.currentZone])
        self.removeHitTimings(currentSongPos)
        # Background
        self.display.blit(self.background_image, (-self.player.x, -self.player.y))
        for c in self.cores:
            c.draw(self.display, (self.player.x, self.player.y))
            c.tick()
        self.player.tick()
        self.enemyHandler.draw(self.display, self.player.x, self.player.y)
        self.display.blit(self.label_font.render(f"x{self.playData['current-combo']}", False, "#FFFFFF"), (0, 0))
        self.beatHitter.draw(self.display)
        self.beatHitter.tick()

        self.flame.tick(self.display, self.main_loop.dt)
        return super().tick(self.player)
