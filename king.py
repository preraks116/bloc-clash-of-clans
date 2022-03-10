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
        screen.screen[self.x][self.y] = screen.bg
        if ch == 'w' and screen.screen[self.x - 1][self.y] == screen.bg:          
            self.x -= 1
        if ch == 's' and screen.screen[self.x + 1][self.y] == screen.bg:
            self.x += 1
        if ch == 'a' and screen.screen[self.x][self.y - 1] == screen.bg:
            self.y -= 1
        if ch == 'd' and screen.screen[self.x][self.y + 1] == screen.bg:
            self.y += 1

    # polymorphism example
    def draw(self,screen):
        super().draw(screen)
            