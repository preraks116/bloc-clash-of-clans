import os
import numpy as np
from colorama import init as cinit
from colorama import Fore, Back, Style
from screen import Screen
import random
import time
import sys
from building import Building

class Cannon(Building):
    def __init__(self, x,y, game):
        super().__init__(x,y,1,1,'C',Back.GREEN, game)
        self.health = 25
        self.attack = 5
        self.cooldown = 8
        # self.isBroken = False
    
    def updateCannons(self):
    # check if king is close to the cannon
        if not self.isBroken and abs(self.game.king.x - self.x) <= 3 and abs(self.game.king.y - self.y) <= 3 and self.game.time % self.cooldown == 0:
            self.game.king.health -= self.attack
            print("Cannon hit the king: ",self.game.king.health, file=sys.stderr)
            if self.game.king.health <= 0:
                self.game.king.isDead = True
    
    # for loop for attacking all the barbarians, add a break after the first iteration because we only want to attack one
            
    # def updateWall(self, screen):
    #     if self.isBroken == False:
    #         screen.screen[self.x][self.y] = self.ch
    #     else:
    #         screen.screen[self.x][self.y] = screen.bg