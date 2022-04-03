import os
import numpy as np
from colorama import init as cinit
from colorama import Fore, Back, Style
from src.game.screen import Screen
import random
import time
import sys
from src.army.person import Person

class Barbarian(Person):
    def __init__(self, x, y, game):
        super().__init__(x, y, 'B', Back.BLACK, game)
        self.maxHealth = 20
        self.health = self.maxHealth
        self.attack = 5
        self.speed = 1
        self.cooldown = 3
        self.isDead = False
        self.nearestBuilding = None
        self.cooldown = 2

    def getDistance(self, building):
        return (abs(self.x - building.x) + abs(self.y - building.y))

    
    def getNearestBuilding(self):
        nearest = None
        maxdist = 99
        for hut in self.game.huts:
            if not hut.isBroken:
                dist = self.getDistance(hut)
                if dist < maxdist:
                    maxdist = dist
                    nearest = hut

        dist = self.getDistance(self.game.townhall)
        if not self.game.townhall.isBroken and dist < maxdist:
            maxdist = dist
            nearest = self.game.townhall
        
        for cannon in self.game.cannons:
            if not cannon.isBroken:
                dist = self.getDistance(cannon)
                if dist < maxdist:
                    maxdist = dist
                    nearest = cannon
        
        self.nearestBuilding = nearest
    
    def getNearestWall(self):
        nearest = None
        maxdist = 99

        for wall in self.game.walls:
            dist = self.getDistance(wall)
            if dist < maxdist:
                maxdist = dist
                nearest = wall
            
        return nearest
    ##?? add feature where barbarian starts looking for next building if the building breaks while he is walking to it 
    def updateBarb(self,screen):
        if not self.isDead and self.game.time % self.cooldown == 0:
            if self.nearestBuilding is None:
                self.getNearestBuilding()
                if self.nearestBuilding is None:
                    return
            if not self.checkCollision(self.nearestBuilding):
                hasStopped = 1
                screen.screen[self.x][self.y] = screen.bg
                if self.x < self.nearestBuilding.x and (screen.screen[self.x + 1][self.y] == screen.bg or screen.screen[self.x + 1][self.y][5] == self.ch):
                    self.x += self.speed
                    hasStopped = 0
                elif self.x > self.nearestBuilding.x and (screen.screen[self.x - 1][self.y] == screen.bg or screen.screen[self.x - 1][self.y][5] == self.ch):
                    self.x -= self.speed
                    hasStopped = 0
                elif self.y < self.nearestBuilding.y and (screen.screen[self.x][self.y + 1] == screen.bg or screen.screen[self.x][self.y + 1][5] == self.ch):
                    self.y += self.speed
                    hasStopped = 0
                elif self.y > self.nearestBuilding.y and (screen.screen[self.x][self.y - 1] == screen.bg or screen.screen[self.x][self.y - 1][5] == self.ch):
                    self.y -= self.speed
                    hasStopped = 0
                
                if hasStopped:
                    # print("wall detected", file=sys.stderr)
                    wall = self.getNearestWall()
                    if wall is not None:
                        # print(self.getDistance(wall),file=sys.stderr)
                        if self.getDistance(wall) == 1:
                            self.registerHit(wall)
                        else:
                            self.getNearestBuilding()                
            else:
                self.registerHit(self.nearestBuilding)
                # print("hit:", self.nearestBuilding.health,' ', self.nearestBuilding.isBroken, file=sys.stderr)
                if self.nearestBuilding.isBroken:
                    self.nearestBuilding = None
                        
                
                

    

