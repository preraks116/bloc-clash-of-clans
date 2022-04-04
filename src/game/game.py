import os
import numpy as np
import sys
import copy
import pickle
import json
from colorama import init as cinit
from colorama import Fore, Back, Style
import random
from time import monotonic as clock, sleep
from src.army.barbarian import Barbarian
from src.buildings.cannon import Cannon
from src.army.king import King
from src.army.queen import Queen
from src.buildings.hut import Hut
from src.game.screen import Screen
from src.buildings.wall import Wall
from src.buildings.townhall import Townhall
from src.buildings.spawnpoint import SpawnPoint
from src.utils.input import *

# \033[0;0H

cinit(autoreset=True)

class Game:
    def __init__(self, choice):
        # change stdout to null
        # sys.stdout = open(os.devnull, 'w')
        self.screen = Screen(50,100)
        self.framerate = 30
        self.game_over = False
        self.gamelost = False
        self.gamestate = 1
        self.gamewon  = False
        self.screens = []
        self.character = choice
        self.time = 0
        self.load_level(self.gamestate)

    def load_level(self, lvlno):
        self.screen.clear_screen()
        if lvlno == 1:
            filename = 'src/game/levels/one.json'
        elif lvlno == 2:
            filename = 'src/game/levels/two.json'
        elif lvlno == 3:
            filename = 'src/game/levels/three.json'
        with open(filename, 'r') as f:
            self.level = json.load(f)
        

        self.rageSpell = self.level['game']['spells']['rageSpell']
        self.healSpell = self.level['game']['spells']['healSpell']
        if self.character == 1:
            self.king = King(self.level['person']['king']['x'],self.level['person']['king']['y'],self)
        elif self.character == 2:
            self.king = Queen(self.level['person']['king']['x'],self.level['person']['king']['y'],self)

        self.townhall = Townhall(self.level['building']['townhall']['x'],self.level['building']['townhall']['y'],self)

        self.walls = []
        for i in range (0,len(self.level['building']['walls'])):
            self.walls += self.generateLine(self.level['building']['walls'][i]['x'],self.level['building']['walls'][i]['y'],self.level['building']['walls'][i]['length'],self.level['building']['walls'][i]['orientation'])
        
        self.huts = []
        for i in range (0,len(self.level['building']['huts'])):
            self.huts.append(Hut(self.level['building']['huts'][i]['x'],self.level['building']['huts'][i]['y'],self))
        
        self.cannons = []
        for i in range (0,len(self.level['building']['cannons'])):
            self.cannons.append(Cannon(self.level['building']['cannons'][i]['x'],self.level['building']['cannons'][i]['y'],self))

        self.barbarians = []
        self.spawnPoints = []
        for i in range (0,len(self.level['building']['spawns'])):
            self.spawnPoints.append(SpawnPoint(self.level['building']['spawns'][i]['x'],self.level['building']['spawns'][i]['y'],self))

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

        if self.king.health <= self.king.maxHealth:
            self.king.color = Back.BLACK
        if self.king.health <= 65:
            self.king.color = Back.LIGHTMAGENTA_EX
        if self.king.health <= 25:
            self.king.color = Back.LIGHTYELLOW_EX
        if self.king.health <= 0:
            self.king.color = Back.WHITE

        for barbarian in self.barbarians:
            if barbarian.health <= barbarian.maxHealth:
                barbarian.color = Back.BLACK
            if barbarian.health <= 10:
                barbarian.color = Back.LIGHTMAGENTA_EX
            if barbarian.health <= 5:
                barbarian.color = Back.LIGHTYELLOW_EX
            if barbarian.health <= 0:
                barbarian.color = Back.WHITE

    def check_game_over(self):
        # check here for all barbarians dead as well
        if not self.king.isDead:
            return
        for barbarian in self.barbarians:
            if not barbarian.isDead:
                return
        self.game_over = True    
        self.gamelost = True
        print("GAME OVER!")

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
        self.gamestate += 1
        if self.gamestate > 3:
            self.game_over = True
            self.gamewon = True
            return
        self.load_level(self.gamestate)

    def updateHUD(self):
        # using kings health to print a health bar 
        boxes = int(self.king.health/10)
        # print(boxes,file=sys.stderr)
        bar = ""
        for i in range(10):
            if i < boxes:
                bar += Fore.GREEN + "█ " + Style.RESET_ALL
            else:
                bar += Fore.RED + "█ " + Style.RESET_ALL
        # print("Level: ", self.gamestate)
        if self.character == 1:
            print("King's health: " , bar)
        elif self.character == 2:
            print("Queen's health: " , bar)
        print("Heal Spells Left: ", self.healSpell)
        print("Rage Spells Left: ", self.rageSpell)
        print("Level: ", self.gamestate)
    
    def play(self):
        input__ = Get()

        while not self.game_over:
            # self.screen.clear()
            print('\033[0;0H')
            # self.get_input()
            ch = input_to(input__)
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
                elif ch == 'r':
                    if self.rageSpell:
                        self.rageSpell = 0
                        self.king.attack *= 2
                        self.king.cooldown /= 2
                        for barbarian in self.barbarians:
                            barbarian.attack *= 2
                            barbarian.cooldown /= 2
                elif ch == 'h':
                    if self.healSpell:
                        self.healSpell = 0
                        self.king.health *= 1.5
                        if self.king.health > self.king.maxHealth:
                            self.king.health = self.king.maxHealth
                        for barbarian in self.barbarians:
                            barbarian.health *= 1.5
                            if barbarian.health > barbarian.maxHealth:
                                barbarian.health = barbarian.maxHealth
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
            self.screens.append(copy.deepcopy(self.screen.screen))
            self.screen.print()
            self.updateHUD()
            self.time += 1
            # print(self.time, file=sys.stderr)
            sleep(1/self.framerate)
        self.screen.clear()
        if self.gamewon:
            print("You Win!")
        elif self.gamelost:
            print("You Lose!")
        input_char = input("Do you want to save the replay? [Y/n] : ") 
        if input_char == 'Y' or input_char == 'y' or input_char == '':
            name = input("Enter file name: ")
            with open('replays/' + name, 'wb') as f:
                pickle.dump(self.screens,f)
        elif input_char == 'n' or input_char == 'N':
            pass
        else:
            print("Invalid input. Exiting.")
    