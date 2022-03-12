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

class Barbarian(Person):
    def __init__(self, x, y, game):
        super().__init__(x, y, 'B', Back.BLACK, game)
        self.health = 50
        self.attack = 2
        self.speed = 1
        self.cooldown = 3
        self.isDead = False
        self.nearestBuilding = None

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
    
    def updateBarb(self,screen):
        if not self.isDead:
            if self.nearestBuilding is None:
                self.getNearestBuilding()
                print(self.nearestBuilding.x, self.nearestBuilding.y, file=sys.stderr)
            if not self.checkCollision(self.nearestBuilding):
                flag = 0
                screen.screen[self.x][self.y] = screen.bg
                if self.x < self.nearestBuilding.x and screen.screen[self.x + 1][self.y] == screen.bg:
                    self.x += self.speed
                    flag = 1
                elif self.x > self.nearestBuilding.x and screen.screen[self.x - 1][self.y] == screen.bg:
                    self.x -= self.speed
                    flag = 1
                elif self.y < self.nearestBuilding.y and screen.screen[self.x][self.y + 1] == screen.bg:
                    self.y += self.speed
                    flag = 1
                elif self.y > self.nearestBuilding.y and screen.screen[self.x][self.y - 1] == screen.bg:
                    self.y -= self.speed
                    flag = 1
                
                if not flag:
                    # print("wall detected", file=sys.stderr)
                    wall = self.getNearestWall()
                    if wall is not None:
                        self.registerHit(wall)
                
            else:
                self.registerHit(self.nearestBuilding)
                print("hit:", self.nearestBuilding.health,' ', self.nearestBuilding.isBroken, file=sys.stderr)
                if self.nearestBuilding.isBroken:
                    self.nearestBuilding = None
                        
                
                

    

