import os
import numpy as np
import sys
from colorama import init as cinit
from colorama import Fore, Back, Style
import random
from time import monotonic as clock, sleep
from king import King
from screen import Screen
from wall import Wall
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
        self.walls = []
        self.walls += generateLine(20,20,20,1)
        self.walls += generateLine(20,20,20,0)
        self.walls += generateLine(40,20,20,1)
        self.walls += generateLine(20,40,21,0)
        
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
                wall.updateWall(self.screen)
            
            self.king.draw(self.screen.screen)
            self.screen.print()
            sleep(1/self.framerate)
