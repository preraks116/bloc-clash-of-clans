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
    def __init__(self, x, y, game):
        super().__init__(x, y, 'K', Back.BLACK, game)
        self.health = 100
        self.attack = 10
        self.speed = 1
        self.isDead = False
    
    def checkCollision(self, building):
        xdiff = self.x - building.x
        ydiff = self.y - building.y
        if xdiff == building.size_x or xdiff == -1:
            return 1
        if ydiff == building.size_y or ydiff == -1:
            return 1
        return 0
    
    def registerHit(self,building):
        building.health -= self.attack
        if building.health <= 0:
            building.isBroken = True 

    def updateMove(self, screen, ch):
        if ch in movementKeys:
            dx, dy = movementKeys[ch]
            # print(screen.screen[self.x + dx][self.y + dy], file=sys.stderr)
            if screen.screen[self.x + dx][self.y + dy] == screen.bg:
                screen.screen[self.x][self.y] = screen.bg
                self.x += dx*self.speed
                self.y += dy*self.speed
            # print(self.x, self.y, file=sys.stderr)
        # if ch in ['w', 'a', 's', 'd']:
        #     screen.screen[self.x][self.y] = screen.bg
        #     if ch == 'w' and screen.screen[self.x -1][self.y] == screen.bg:
        #         self.x -= 1
        #     if ch == 's' and screen.screen[self.x + 1][self.y] == screen.bg:
        #         self.x += 1
        #     if ch == 'a' and screen.screen[self.x][self.y - 1] == screen.bg:
        #         self.y -= 1
        #     if ch == 'd' and screen.screen[self.x][self.y + 1] == screen.bg:
        #         self.y += 1
        if ch == ' ':
            for building in self.game.walls:
                # check if building is close to king
                if abs(building.x - self.x) <= 1 and abs(building.y - self.y) <= 1:
                    building.health -= self.attack
                    if building.health <= 0:
                        building.isBroken = True
            
            for building in self.game.cannons:
                # check if building is close to king
                if abs(building.x - self.x) <= 1 and abs(building.y - self.y) <= 1:
                    building.health -= self.attack
                    if building.health <= 0:
                        building.isBroken = True

            if not self.game.townhall.isBroken and self.checkCollision(self.game.townhall):
                print(self.game.townhall.health, file=sys.stderr)
                self.registerHit(self.game.townhall)

            for building in self.game.huts:
                # check if building is close to king
                if abs(building.x - self.x) <= 1 and abs(building.y - self.y) <= 1:
                    building.health -= self.attack
                    # print(building.health, file=sys.stderr)
                    if building.health <= 0:
                        building.isBroken = True
    

    # polymorphism example
    def draw(self,screen):
        super().draw(screen)
            