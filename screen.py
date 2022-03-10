import os
import numpy as np
from colorama import init as cinit
from colorama import Fore, Back, Style
import random
import time
import sys

class Screen:
    def __init__(self,height,width):
        self.height = height
        self.width = width
        self.screen = np.array([[Back.GREEN + ' ' + Style.RESET_ALL for i in range(self.width)] for j in range(self.height)])
    
    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print(self):
        str = ""
        for i in range(self.height):
            for j in range(self.width):
                str += self.screen[i][j]
            str += '\n'
        str += '\0'
        # print str using sys
        sys.stdout.write(str)