import os
import numpy as np
from colorama import init as cinit
from colorama import Fore, Back, Style
from src.game.screen import Screen
import random
import time
import sys
from src.army.person import Person

movementKeys = {
    'w': (-1, 0),
    'a': (0, -1),
    's': (1, 0),
    'd': (0, 1)
}

class King(Person):
    def __init__(self, x, y, game):
        super().__init__(x, y, 100, 65, 25,'K', Back.BLACK, game)
        # self.maxHealth = 100
        # self.health = self.maxHealth
        self.attack = 15
        self.speed = 1
        self.isDead = False
        self.cooldown = 2
    
    def updateMove(self, screen, ch):
        ch = ch.lower()
        if not self.isDead and ch in movementKeys and self.game.time % self.cooldown == 0:
            dx, dy = movementKeys[ch]
            # print(screen.screen[self.x + dx][self.y + dy], file=sys.stderr)
            if screen.screen[self.x + dx*self.speed][self.y + dy*self.speed] == screen.bg:
                screen.screen[self.x][self.y] = screen.bg
                self.x += dx*self.speed
                self.y += dy*self.speed
                # print(self.x, " ", self.y, file=sys.stderr)

        if not self.isDead and ch == ' ':

            for building in self.game.walls:
                if not building.isBroken and self.checkCollision(building):
                    self.registerHit(building)

            for building in self.game.cannons:
                if not building.isBroken and self.checkCollision(building):
                    self.registerHit(building)

            if not self.game.townhall.isBroken and self.checkCollision(self.game.townhall):
                # print(self.game.townhall.health, file=sys.stderr)
                self.registerHit(self.game.townhall)

            for building in self.game.huts:
                if not building.isBroken and self.checkCollision(building):
                    self.registerHit(building)
                
            for building in self.game.wizardtowers:
                if not building.isBroken and self.checkCollision(building):
                    self.registerHit(building)

    # polymorphism example
    def draw(self,screen):
        super().draw(screen)
            