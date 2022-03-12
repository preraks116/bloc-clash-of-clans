import os
import numpy as np
import sys
from colorama import init as cinit
from colorama import Fore, Back, Style
import random
from time import monotonic as clock, sleep
from army.barbarian import Barbarian
from buildings.cannon import Cannon
from army.king import King
from buildings.hut import Hut
from game.screen import Screen
from buildings.wall import Wall
from buildings.townhall import Townhall
from buildings.spawnpoint import SpawnPoint
from utils.input import *

# \033[0;0H

cinit(autoreset=True)

class Game:
    def __init__(self):
        # change stdout to null
        # sys.stdout = open(os.devnull, 'w')
        self.screen = Screen(50,100)
        self.framerate = 30
        self.game_over = False

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
        if self.king.health <= 65:
            self.king.color = Back.YELLOW
        if self.king.health <= 25:
            self.king.color = Back.RED
        for barbarian in self.barbarians:
            if barbarian.health <= 10:
                barbarian.color = Back.LIGHTGREEN_EX
            if barbarian.health <= 5:
                barbarian.color = Back.LIGHTBLUE_EX
            if barbarian.health == 0:
                barbarian.color = Back.WHITE

    def check_game_over(self):
        # check here for all barbarians dead as well
        if self.king.isDead:
            self.game_over = True    

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

    
    def play(self):
        input = Get()
        while not self.game_over:
            # self.screen.clear()
            print('\033[0;0H')
            # self.get_input()
            ch = input_to(input)
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
            self.screen.print()
            self.time += 1
            # print(self.time, file=sys.stderr)
            sleep(1/self.framerate)