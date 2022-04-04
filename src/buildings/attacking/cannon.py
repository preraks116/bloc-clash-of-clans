import os
import numpy as np
from colorama import init as cinit
from colorama import Fore, Back, Style
from src.game.screen import Screen
import random
import time
import sys
from src.buildings.building import Building

class Cannon(Building):
    def __init__(self, x,y, game):
        super().__init__(x,y,1,1,25,15,5,'C',Back.GREEN, game)
        # self.health = 25
        self.attack = 5
        self.cooldown = 8
        self.range = 5  
        # self.isBroken = False
    
    def inRange(self, person):
        return abs(person.x - self.x) + abs(person.y - self.y) <= self.range
    
    def updateCannons(self):
        # check if king is close to the cannon
        if not self.isBroken and not self.game.king.isDead and self.inRange(self.game.king) and self.game.time % self.cooldown == 0:
            self.game.king.health -= self.attack
            # print("Cannon hit the king: ",self.game.king.health, file=sys.stderr)
            if self.game.king.health <= 0:
                self.game.king.isDead = True
    
        # for loop for attacking all the barbarians, add a break after the first iteration because we only want to attack one
        for barbarian in self.game.barbarians:
            if not barbarian.isDead and not self.isBroken and abs(barbarian.x - self.x) + abs(barbarian.y - self.y) <= self.range and self.game.time % self.cooldown == 0:
                barbarian.health -= self.attack
                # add indication that the barb is getting attacked
                # print("Cannon hit the barbarian: ",barbarian.health, file=sys.stderr)
                if barbarian.health <= 0:
                    barbarian.isDead = True
                break
            
    # def updateWall(self, screen):
    #     if self.isBroken == False:
    #         screen.screen[self.x][self.y] = self.ch
    #     else:
    #         screen.screen[self.x][self.y] = screen.bg