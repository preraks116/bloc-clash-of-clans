import os
import numpy as np
from colorama import init as cinit
from colorama import Fore, Back, Style
from src.game.screen import Screen
import random
import time
import sys

class Person:
    def __init__(self, x, y, ch, color, game):
        self.x = x
        self.y = y
        self.color = color
        self.ch = ch
        self.game = game

    def registerHit(self,building):
        building.health -= self.attack
        if building.health <= 0:
            building.isBroken = True 

    def checkCollision(self, building):
        xdiff = self.x - building.x
        ydiff = self.y - building.y
        if not building.isBroken and (xdiff == -1 or xdiff == building.size_x) and self.y in range(building.y, building.y + building.size_y):
            return 1
        if not building.isBroken and (ydiff == -1 or ydiff == building.size_y) and self.x in range(building.x, building.x + building.size_x):
            return 1
        return 0

    def draw(self, screen):
        screen[self.x][self.y] = self.color + self.ch

    
