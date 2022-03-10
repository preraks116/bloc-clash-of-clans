import os
import numpy as np
import sys
from colorama import init as cinit
from colorama import Fore, Back, Style
import random
from time import monotonic as clock, sleep
from king import King
from screen import Screen
from person import Person
from input import *

# \033[0;0H

class Game:
    def __init__(self):
        # change stdout to null
        # sys.stdout = open(os.devnull, 'w')
        self.screen = Screen(50,100)
        self.framerate = 30
        self.game_over = False
        self.king = King(10,10)
        
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
            self.king.draw(self.screen.screen)
            self.screen.print()
            sleep(1/self.framerate)
