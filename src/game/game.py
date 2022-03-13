import os
import numpy as np
import sys
import copy
import pickle
from colorama import init as cinit
from colorama import Fore, Back, Style
import random
from time import monotonic as clock, sleep
from src.army.barbarian import Barbarian
from src.buildings.cannon import Cannon
from src.army.king import King
from src.buildings.hut import Hut
from src.game.screen import Screen
from src.buildings.wall import Wall
from src.buildings.townhall import Townhall
from src.buildings.spawnpoint import SpawnPoint
from src.utils.input import *

# \033[0;0H

cinit(autoreset=True)

class Game:
    def __init__(self):
        # change stdout to null
        # sys.stdout = open(os.devnull, 'w')
        self.screen = Screen(50,100)
        self.framerate = 30
        self.game_over = False
        self.gamelost = False
        self.gamewon  = False
        self.screens = []

        self.rageSpell = 1
        self.healSpell = 1

        self.king = King(10,10,self)

        self.townhall = Townhall(30,30,self)
        self.time = 0
        self.walls = []
        self.walls += self.generateLine(20,20,20,1)
        self.walls += self.generateLine(20,20,20,0)
        self.walls += self.generateLine(40,20,20,1)
        self.walls += self.generateLine(20,40,21,0)

        self.hutscoords = [[15,15],[10,15],[15,80],[10,80],[15,45],[40,45],[45,10],[40,80]]
        self.huts = []
        for i in range(len(self.hutscoords)):
            self.huts.append(Hut(self.hutscoords[i][0],self.hutscoords[i][1],self))

        self.cannoncoords = [[23,25],[23,30],[43,25],[43,30],[33,25],[35,30]]
        self.cannons = []
        for i in range(len(self.cannoncoords)):
            self.cannons.append(Cannon(self.cannoncoords[i][0],self.cannoncoords[i][1],self))

        # self.barbcoords = [[35,41]]
        self.barbarians = []
        # for i in range(len(self.barbcoords)):
        #     self.barbarians.append(Barbarian(self.barbcoords[i][0],self.barbcoords[i][1],self))
        
        self.spawnPoints = []
        self.spawncoords = [[48,50], [48,40], [48,30]]
        for i in range(len(self.spawncoords)):
            self.spawnPoints.append(SpawnPoint(self.spawncoords[i][0],self.spawncoords[i][1],self))

    def generateLine(self,x,y,L,m):
        p = []  
        for i in range(L):
            if m == 1:
                p.append(Wall(x,y+i,self))
            elif m == 0:
                p.append(Wall(x+i,y,self))
        
        return p

    def updateColors(self):
        for wall in self.walls:
            if wall.health <= 25:
                wall.color = Back.YELLOW
            if wall.health <= 15:
                wall.color = Back.RED

        for hut in self.huts:
            if hut.health <= 25:
                hut.color = Back.YELLOW
            if hut.health <= 15:
                hut.color = Back.RED

        for cannon in self.cannons:
            if cannon.health <= 15:
                cannon.color = Back.YELLOW
            if cannon.health <= 5:
                cannon.color = Back.RED

        if self.townhall.health <= 65:
            self.townhall.color = Back.YELLOW
        if self.townhall.health <= 25:
            self.townhall.color = Back.RED

        if self.king.health <= self.king.maxHealth:
            self.king.color = Back.BLACK
        if self.king.health <= 65:
            self.king.color = Back.LIGHTMAGENTA_EX
        if self.king.health <= 25:
            self.king.color = Back.LIGHTYELLOW_EX
        if self.king.health <= 0:
            self.king.color = Back.WHITE

        for barbarian in self.barbarians:
            if barbarian.health <= barbarian.maxHealth:
                barbarian.color = Back.BLACK
            if barbarian.health <= 10:
                barbarian.color = Back.LIGHTMAGENTA_EX
            if barbarian.health <= 5:
                barbarian.color = Back.LIGHTYELLOW_EX
            if barbarian.health <= 0:
                barbarian.color = Back.WHITE

    def check_game_over(self):
        # check here for all barbarians dead as well
        if not self.king.isDead:
            return
        for barbarian in self.barbarians:
            if not barbarian.isDead:
                return
        self.game_over = True    
        self.gamelost = True
        print("GAME OVER")

    def check_game_win(self):
        # check if all buildings are destroyed 
        for hut in self.huts:
            if not hut.isBroken:
                return
        for cannon in self.cannons:
            if not cannon.isBroken:
                return
        if not self.townhall.isBroken:
            return
        self.game_over = True
        self.gamewon = True

    def updateHUD(self):
        # using kings health to print a health bar 
        boxes = int(self.king.health/10)
        # print(boxes,file=sys.stderr)
        bar = ""
        for i in range(10):
            if i < boxes:
                bar += Fore.GREEN + "█ " + Style.RESET_ALL
            else:
                bar += Fore.RED + "█ " + Style.RESET_ALL
        print("King's health: " , bar)
        print("Heal Spells Left: ", self.healSpell)
        print("Rage Spells Left: ", self.rageSpell)
    
    def play(self):
        input__ = Get()
        while not self.game_over:
            # self.screen.clear()
            print('\033[0;0H')
            # self.get_input()
            ch = input_to(input__)
            # ch = input_to(input)
            if ch is not None:
                if ch == 'q':
                    self.game_over = True
                elif ch == '1':
                    self.spawnPoints[0].spawnBarb(self.barbarians)
                elif ch == '2':
                    self.spawnPoints[1].spawnBarb(self.barbarians)
                elif ch == '3':
                    self.spawnPoints[2].spawnBarb(self.barbarians)
                elif ch == 'r':
                    if self.rageSpell:
                        self.rageSpell = 0
                        self.king.attack *= 2
                        self.king.cooldown /= 2
                        for barbarian in self.barbarians:
                            barbarian.attack *= 2
                            barbarian.cooldown /= 2
                elif ch == 'h':
                    if self.healSpell:
                        self.healSpell = 0
                        self.king.health *= 1.5
                        if self.king.health > self.king.maxHealth:
                            self.king.health = self.king.maxHealth
                        for barbarian in self.barbarians:
                            barbarian.health *= 1.5
                            if barbarian.health > barbarian.maxHealth:
                                barbarian.health = barbarian.maxHealth
                else:
                    self.king.updateMove(self.screen, ch)
            
            # self.wall.updateWall(self.screen)
            self.check_game_over()
            self.check_game_win()
            for wall in self.walls:
                wall.updateBuilding(self.screen)
            for hut in self.huts:
                hut.updateBuilding(self.screen)
            for cannon in self.cannons:
                cannon.updateBuilding(self.screen)
                cannon.updateCannons()
            self.townhall.updateBuilding(self.screen)
            for barbarian in self.barbarians:
                barbarian.updateBarb(self.screen)
                barbarian.draw(self.screen.screen)
            for spawnPoint in self.spawnPoints:
                spawnPoint.updateBuilding(self.screen)
            self.updateColors()
            self.king.draw(self.screen.screen)
            self.screens.append(copy.deepcopy(self.screen.screen))
            self.screen.print()
            self.updateHUD()
            self.time += 1
            # print(self.time, file=sys.stderr)
            sleep(1/self.framerate)
        if self.gamewon:
            print("You Win!")
        elif self.gamelost:
            print("You Lose!")
        name = input("Enter file name: ")
        with open('replays/' + name, 'wb') as f:
            pickle.dump(self.screens,f)
    