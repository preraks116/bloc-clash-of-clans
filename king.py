import os
import numpy as np
from colorama import init as cinit
from colorama import Fore, Back, Style
from person import Person
from screen import Screen
import random
import time
import sys
from person import Person

movementKeys = {
    'w': (-1, 0),
    'a': (0, -1),
    's': (1, 0),
    'd': (0, 1)
}

class King(Person):
    def __init__(self, x,y):
        super().__init__(x,y,'K',Fore.BLACK)
        self.health = 100
        self.attack = 10
        self.isDead = False
    
    
    def attackBuilding(self, building):
        building.health -= self.attack
        if building.health <= 0:
            building.isBroken = True
    
    def updateMove(self, screen, ch):
        if ch in movementKeys:
            screen.screen[self.x][self.y] = screen.bg
            dx, dy = movementKeys[ch]
            if screen.screen[self.x + dx][self.y + dy] == screen.bg:
                self.x += dx
                self.y += dy
        # if ch == ' ':
            
    # polymorphism example
    def draw(self,screen):
        super().draw(screen)
            