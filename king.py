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
    
    def attack(self, enemy):
        enemy.health -= self.attack
        if enemy.health <= 0:
            enemy.isDead = True
    
    def updateMove(self, screen, ch):
        screen.screen[self.x][self.y] = screen.bg
        if ch == 'w':          
            self.x -= 1
        if ch == 's':
            self.x += 1
        if ch == 'a':
            self.y -= 1
        if ch == 'd':
            self.y += 1

    # polymorphism example
    def draw(self,screen):
        super().draw(screen)
            