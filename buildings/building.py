import os
import numpy as np
from colorama import init as cinit
from colorama import Fore, Back, Style
from game.screen import Screen
import random
import time
import sys

class Building:
    def __init__(self, x, y, size_x, size_y, ch, color, game):
        self.x = x
        self.y = y
        # self.size = size
        self.size_x = size_x
        self.size_y = size_y
        self.color = color
        self.ch = ch
        self.isBroken = False
        self.game = game

    def draw(self, screen, ch):
        for y in range(self.size_y):
            for x in range(self.size_x):
                screen[self.x + x][self.y + y] = ch
    
    def updateBuilding(self, screen):
        if self.isBroken == False:
            self.draw(screen.screen, self.color + self.ch + Back.RESET)
        else:
            self.draw(screen.screen, screen.bg)