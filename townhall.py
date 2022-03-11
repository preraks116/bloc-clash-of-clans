import os
import numpy as np
from colorama import init as cinit
from colorama import Fore, Back, Style
import random
import time
import sys
from building import Building

class Townhall(Building):
    def __init__(self, x,y):
        super().__init__(x,y,4,'T',Back.GREEN)
        self.health = 100
    
