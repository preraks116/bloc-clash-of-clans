import os
import numpy as np
from colorama import init as cinit
from colorama import Fore, Back, Style
from src.game.screen import Screen
import random
import time
import sys

class Building:
    def __init__(self, x, y, size_x, size_y, health, midhealth, lowhealth, ch, color, game):
        self.x = x
        self.y = y
        # self.size = size
        self.size_x = size_x
        self.size_y = size_y
        self.color = color
        self.ch = ch
        self.isBroken = False
        self.game = game
        self.health = health
        self.midhealth = {'value': midhealth, 'color': Back.YELLOW}
        self.lowhealth = {'value': lowhealth, 'color': Back.RED}

    def updateColors(self):
        if self.health <= self.midhealth['value']:
            self.color = self.midhealth['color']
        if self.health <= self.lowhealth['value']:
            self.color = self.lowhealth['color']

    def draw(self, screen, ch):
        for y in range(self.size_y):
            for x in range(self.size_x):
                screen[self.x + x][self.y + y] = ch
    
    
    
    def updateBuilding(self, screen):
        if self.isBroken == False:
            self.draw(screen.screen, self.color + self.ch + Back.RESET)
        else:
            self.draw(screen.screen, screen.bg)