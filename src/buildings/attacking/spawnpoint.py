import os
import numpy as np
from colorama import init as cinit
from colorama import Fore, Back, Style
from src.game.screen import Screen
import random
import time
import sys
from src.buildings.building import Building
from src.army.troops.barbarian import Barbarian
from src.army.troops.archer import Archer
from src.army.troops.balloon import Balloon

class SpawnPoint(Building):
    def __init__(self, x,y, game):
        super().__init__(x,y,1,1,10,10,10,'S',Back.BLACK, game)
        
    def updateBuilding(self, screen):
        self.draw(screen.screen, self.color + self.ch + Back.RESET)
        # self.isBroken = False
    
    def spawnBarb(self, barbarians):
        barbarian = Barbarian(self.x-1,self.y,self.game)
        barbarians.append(barbarian)
    
    def spawnArch(self, archers):
        archer = Archer(self.x-1,self.y,self.game)
        archers.append(archer)
    
    def spawnBalloon(self, balloons):
        balloon = Balloon(self.x-1,self.y,self.game)
        balloons.append(balloon)
    # def updateWall(self, screen):
    #     if self.isBroken == False:
    #         screen.screen[self.x][self.y] = self.ch
    #     else:
    #         screen.screen[self.x][self.y] = screen.bg