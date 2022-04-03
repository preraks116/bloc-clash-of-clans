import os
import numpy as np
from colorama import init as cinit
from colorama import Fore, Back, Style
from src.game.screen import Screen
import random
import time
import sys

class Text:
    def __init__(self,x,y,size_x,size_y,bgcolor,game,text):
        self.x = x
        self.y = y
        self.size_x = size_x
        self.size_y = size_y
        self.bgcolor = bgcolor
        self.game = game
        self.text = text

    def draw(self,screen):
        # for y in range(self.size_y):
        #     flag = 0
        #     for x in range(self.size_x):
        #         if 
        #         screen.screen[self.x + x][self.y + y] = self.bgcolor + self.text[y*self.size_x+x] + Back.RESET
        x = self.x
        y = self.y
        for i in range(len(self.text)):
            screen.screen[x][y] = self.bgcolor + self.text[i] + Back.RESET
            if screen.screen[x][y] == '\n':
                x += 1
                y = self.y
            y += 1
