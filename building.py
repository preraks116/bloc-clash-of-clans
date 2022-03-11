import os
import numpy as np
from colorama import init as cinit
from colorama import Fore, Back, Style
from screen import Screen
import random
import time
import sys

class Building:
    def __init__(self, x, y, size, ch, color):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.ch = ch
        self.isBroken = False

    def draw(self, screen, ch):
        for y in range(self.size):
            for x in range(self.size):
                screen[self.x + x][self.y + y] = ch
    
    def updateBuilding(self, screen):
        if self.isBroken == False:
            # screen.screen[self.x][self.y] = self.ch
            self.draw(screen.screen, self.color + self.ch + Fore.RESET)
        else:
            # screen.screen[self.x][self.y] = screen.bg
            self.draw(screen.screen, screen.bg)