import os
import numpy as np
import sys
from colorama import init as cinit
from colorama import Fore, Back, Style
import random
from time import monotonic as clock, sleep
from king import King
from hut import Hut
from screen import Screen
from wall import Wall
from townhall import Townhall
from input import *

# \033[0;0H
def generateLine(x,y,L,m):
    p = []
    for i in range(L):
        if m == 1:
            p.append(Wall(x,y+i))
        elif m == 0:
            p.append(Wall(x+i,y))
    
    return p


class Game:
    def __init__(self):
        # change stdout to null
        # sys.stdout = open(os.devnull, 'w')
        self.screen = Screen(50,100)
        self.framerate = 30
        self.game_over = False
        self.king = King(10,10,self)
        self.townhall = Townhall(30,30)
        self.walls = []
        self.walls += generateLine(20,20,20,1)
        self.walls += generateLine(20,20,20,0)
        self.walls += generateLine(40,20,20,1)
        self.walls += generateLine(20,40,21,0)

        self.huts = []
        for i in range(5):
            self.huts.append(Hut(random.randint(0,20),random.randint(0,20)))
        for i in range(3):
            self.huts.append(Hut(random.randint(35,45),random.randint(35,80)))
    
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
        if self.townhall.health <= 25:
            self.townhall.color = Back.YELLOW
        if self.townhall.health <= 15:
            self.townhall.color = Back.RED
        
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
                else:
                    self.king.updateMove(self.screen, ch)
            
            # self.wall.updateWall(self.screen)
            for wall in self.walls:
                wall.updateBuilding(self.screen)
            for hut in self.huts:
                hut.updateBuilding(self.screen)
            self.townhall.updateBuilding(self.screen)
            self.king.draw(self.screen.screen)
            self.updateColors()
            self.screen.print()
            sleep(1/self.framerate)
