import os
import numpy as np
from colorama import init as cinit
from colorama import Fore, Back, Style
from src.game.screen import Screen
import random
import time
import sys
from src.buildings.building import Building

class WizardTower(Building):
    def __init__(self, x,y, game):
        super().__init__(x,y,2,2,25,15,5,'W',Back.GREEN, game)
        # self.health = 25
        self.attack = 5
        self.cooldown = 3
        self.range = 3  
        # self.isBroken = False
    
    # manhattan distance
    def inRange(self, person, thing, range):
        return abs(person.x - thing.x) + abs(person.y - thing.y) <= range
    
    # just checks if the building is next to target
    def isNextTo(self, target, origin):
        return abs(origin.x - target.x) <= 1 and abs(origin.y - target.y) <= 1
    
    def registerAOE(self, troops, origin):
        for troop in troops:
            if not troop.isDead and not origin.isDead and self.isNextTo(troop, origin):
                # print("AOE registered: ",troop.health, file=sys.stderr)
                troop.health -= self.attack
                if troop.health <= 0:
                    troop.isDead = True
                    # print("AOE hit a troop: ",troop.health, file=sys.stderr)
    
    def attackTroop(self, troops):
        for troop in troops:
            if not troop.isDead and not self.isBroken and self.inRange(troop, self, self.range) and self.game.time % self.cooldown == 0:
                troop.health -= self.attack
                # add indication that the barb is getting attacked
                # print("Cannon hit the troop: ",troop.health, file=sys.stderr)
                if troop.health <= 0:
                    troop.isDead = True
                self.registerAOE(self.game.barbarians, troop)
                self.registerAOE(self.game.archers, troop)
                self.registerAOE(self.game.balloons, troop)
                break
    
    def updateTowers(self):
        # check if king is close to the cannon
        if not self.isBroken and not self.game.king.isDead and self.inRange(self.game.king, self, self.range) and self.game.time % self.cooldown == 0:
            self.game.king.health -= self.attack
            # print("Cannon hit the king: ",self.game.king.health, file=sys.stderr)
            if self.game.king.health <= 0:
                self.game.king.isDead = True
    
        self.attackTroop(self.game.barbarians)
        self.attackTroop(self.game.archers)
        self.attackTroop(self.game.balloons)

    # def updateWall(self, screen):
    #     if self.isBroken == False:
    #         screen.screen[self.x][self.y] = self.ch
    #     else:
    #         screen.screen[self.x][self.y] = screen.bg