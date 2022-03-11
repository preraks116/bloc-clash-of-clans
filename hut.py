import os
import numpy as np
from colorama import init as cinit
from colorama import Fore, Back, Style
from screen import Screen
import random
import time
import sys
from building import Building

class Hut(Building):
    def __init__(self, x,y):
        super().__init__(x,y,2,'H',Back.GREEN)
        self.health = 50
        # self.isBroken = False
    
    # def updateWall(self, screen):
    #     if self.isBroken == False:
    #         screen.screen[self.x][self.y] = self.ch
    #     else:
    #         screen.screen[self.x][self.y] = screen.bg