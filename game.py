import time
import random
import sys
import os
from src.game.screen import Screen
from src.game.game import Game

game = Game(0)
while True:
    game.screen.clear()
    print("WELCOME TO COC-BLOC! THE TERMINAL BASED VERSION OF CLASH OF CLANS!")
    print("CHOOSE YOUR CHARACTER!")
    print("1. BARBARIAN KING")
    print("2. ARCHER QUEEN")
    choice = int(input("Enter your choice: "))
    if choice != 1 and choice != 2:
        print("Invalid choice!")
        time.sleep(1)
    else:
        break
game = Game(choice)
game.play()
