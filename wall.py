import os
import numpy as np
from colorama import init as cinit
from colorama import Fore, Back, Style
from screen import Screen
import random
import time
import sys
from building import Building

class Wall(Building):
    def __init__(self, x,y):
        super().__init__(x,y,'#',Fore.BLACK)
        self.health = 100
        self.isBroken = False
    
    def updateWall(self, screen):
        if self.isBroken == False:
            screen.screen[self.x][self.y] = self.ch
        else:
            screen.screen[self.x][self.y] = screen.bg