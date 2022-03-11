import os
import numpy as np
from colorama import init as cinit
from colorama import Fore, Back, Style
from screen import Screen
import random
import time
import sys

class Person:
    def __init__(self, x, y, ch, color, game):
        self.x = x
        self.y = y
        self.color = color
        self.ch = ch
        self.game = game

    def draw(self, screen):
        screen[self.x][self.y] = self.color + self.ch

    
