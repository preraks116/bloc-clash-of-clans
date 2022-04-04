import os
import numpy as np
from colorama import init as cinit
from colorama import Fore, Back, Style
from src.game.screen import Screen
import random
import time
import sys
from src.buildings.building import Building

class Hut(Building):
    def __init__(self, x,y, game):
        super().__init__(x,y,1,1,50,25,15,'H',Back.GREEN, game)
        # self.health = 50
        # self.isBroken = False
    
    # def updateWall(self, screen):
    #     if self.isBroken == False:
    #         screen.screen[self.x][self.y] = self.ch
    #     else:
    #         screen.screen[self.x][self.y] = screen.bg