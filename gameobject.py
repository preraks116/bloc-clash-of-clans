import os
import numpy as np
from colorama import init as cinit
from colorama import Fore, Back, Style
from screen import Screen
import random
import time
import sys

class GameObject:
    def __init__(self, x, y, ch, color):
        self.x = x
        self.y = y
        self.color = color
        self.ch = ch

    def draw(self, screen):
        screen[self.x][self.y] = self.ch