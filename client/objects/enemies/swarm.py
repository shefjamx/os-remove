from objects.enemies.enemy import GenericEnemy
import random


class IndividualSwarmEnemy:

    def __init__(self, swarmX, swarmY):

        self.velocity = [0, 0]
        self.pos = [swarmX + random.randint(0, 10) - 5, swarmY + random.randint(0, 10) - 5]

    
    def adjustVelForCohesion(self, averagePos: tuple[float, float]) -> None:
        pass



class Swarm(GenericEnemy):

    def __init__(self):
        self.NUM_SWARM_ENTITES = 40
        self.swarmEntities = [IndividualSwarmEnemy() for i in range(self.NUM_SWARM_ENTITES)]

    def tick(self):
        avg = []
        print(avg)

