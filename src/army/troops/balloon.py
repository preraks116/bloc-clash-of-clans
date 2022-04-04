import os
import numpy as np
from colorama import init as cinit
from colorama import Fore, Back, Style
from src.game.screen import Screen
import random
import time
import sys
from src.army.person import Person

class Balloon(Person):
    def __init__(self, x, y, game):
        super().__init__(x, y, 20, 10, 5, 'O', Back.BLACK, game)
        # self.maxHealth = 20
        # self.health = self.maxHealth
        self.attack = 12
        self.speed = 1
        self.cooldown = 3
        self.isDead = False
        self.nearestBuilding = None
        self.cooldown = 1

    def getDistance(self, building):
        return (abs(self.x - building.x) + abs(self.y - building.y))

    
    def getNearestBuilding(self):
        nearest = None
        maxdist = 99

        for cannon in self.game.cannons:
            if not cannon.isBroken:
                dist = self.getDistance(cannon)
                if dist < maxdist:
                    maxdist = dist
                    nearest = cannon
        for tower in self.game.wizardtowers:
            if not tower.isBroken:
                dist = self.getDistance(tower)
                if dist < maxdist:
                    maxdist = dist
                    nearest = tower
        # wont go beyond this if a cannon is found
        # wizard tower will come above this
        if not nearest is None:
            self.nearestBuilding = nearest
            return

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
    def updateBalloon(self,screen):
        if not self.isDead and self.game.time % self.cooldown == 0:
            if self.nearestBuilding is None:
                self.getNearestBuilding()
                if self.nearestBuilding is None:
                    return
            if not self.checkCollision(self.nearestBuilding):
                screen.screen[self.x][self.y] = screen.bg
                if self.x < self.nearestBuilding.x:
                    self.x += self.speed
                elif self.x > self.nearestBuilding.x:
                    self.x -= self.speed
                elif self.y < self.nearestBuilding.y:
                    self.y += self.speed
                elif self.y > self.nearestBuilding.y:
                    self.y -= self.speed           
            else:
                self.registerHit(self.nearestBuilding)
                # print("hit:", self.nearestBuilding.health,' ', self.nearestBuilding.isBroken, file=sys.stderr)
                if self.nearestBuilding.isBroken:
                    self.nearestBuilding = None
                        
                
                

    

