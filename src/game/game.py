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
from src.army.troops.barbarian import Barbarian
from src.buildings.attacking.cannon import Cannon
from src.buildings.attacking.wizardtower import WizardTower
from src.army.character.king import King
from src.army.character.queen import Queen
from src.buildings.defending.hut import Hut
from src.game.screen import Screen
from src.buildings.defending.wall import Wall
from src.buildings.defending.townhall import Townhall
from src.buildings.attacking.spawnpoint import SpawnPoint
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
            kingdata = self.level['person']['king']
            self.king = King(kingdata['x'],kingdata['y'],self)
        elif self.character == 2:
            queendata = self.level['person']['king']
            self.king = Queen(queendata['x'],queendata['y'],self)

        halldata = self.level['building']['townhall']
        self.townhall = Townhall(halldata['x'],halldata['y'],self)

        self.walls = []
        wallsdata = self.level['building']['walls']
        for i in range (0,len(wallsdata)):
            self.walls += self.generateLine(wallsdata[i]['x'],wallsdata[i]['y'],wallsdata[i]['length'],wallsdata[i]['orientation'])
        
        self.wizardtowers = []
        wizardtowersdata = self.level['building']['wizardtowers']
        for i in range (0,len(wizardtowersdata)):
            self.wizardtowers.append(WizardTower(wizardtowersdata[i]['x'],wizardtowersdata[i]['y'],self))
        
        self.huts = []
        hutsdata = self.level['building']['huts']
        for i in range (0,len(hutsdata)):
            self.huts.append(Hut(hutsdata[i]['x'],hutsdata[i]['y'],self))
        
        self.cannons = []
        cannonsdata = self.level['building']['cannons']
        for i in range (0,len(cannonsdata)):
            self.cannons.append(Cannon(cannonsdata[i]['x'],cannonsdata[i]['y'],self))

        self.barbarians = []
        self.archers = []
        self.balloons = []
        self.spawnPoints = []
        spawnpointsdata = self.level['building']['spawns']
        for i in range (0,len(spawnpointsdata)):
            self.spawnPoints.append(SpawnPoint(spawnpointsdata[i]['x'],spawnpointsdata[i]['y'],self))

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
            wall.updateColors()

        for hut in self.huts:
            hut.updateColors()

        for cannon in self.cannons:
            cannon.updateColors()
        
        for tower in self.wizardtowers:
            tower.updateColors()

        self.townhall.updateColors()

        self.king.updateColors()

        for barbarian in self.barbarians:
            barbarian.updateColors()
        
        for archer in self.archers:
            archer.updateColors()
        
        for balloon in self.balloons:
            balloon.updateColors()
    
    def updateBuildings(self):
        for wall in self.walls:
            wall.updateBuilding(self.screen)
        for hut in self.huts:
            hut.updateBuilding(self.screen)
        for cannon in self.cannons:
            cannon.updateBuilding(self.screen)
            cannon.updateCannons()
        for tower in self.wizardtowers:
            tower.updateBuilding(self.screen)
            tower.updateTowers()
        self.townhall.updateBuilding(self.screen)
    
    def updateArmy(self):
        for barbarian in self.barbarians:
            barbarian.updateBarb(self.screen)
            barbarian.draw(self.screen.screen)
        for archer in self.archers:
            archer.updateArcher(self.screen)
            archer.draw(self.screen.screen)
        for balloon in self.balloons:
            balloon.updateBalloon(self.screen)
            balloon.draw(self.screen.screen)
        for spawnPoint in self.spawnPoints:
            spawnPoint.updateBuilding(self.screen)

    def check_game_over(self):
        # check here for all barbarians dead as well
        if not self.king.isDead:
            return
        for barbarian in self.barbarians:
            if not barbarian.isDead:
                return
        for archer in self.archers:
            if not archer.isDead:
                return
        for balloon in self.balloons:
            if not balloon.isDead:
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
        for tower in self.wizardtowers:
            if not tower.isBroken:
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
                elif ch == '4':
                    self.spawnPoints[0].spawnArch(self.archers)
                elif ch == '5':
                    self.spawnPoints[1].spawnArch(self.archers)
                elif ch == '6':
                    self.spawnPoints[2].spawnArch(self.archers)
                elif ch == '7':
                    self.spawnPoints[0].spawnBalloon(self.balloons)
                elif ch == '8':
                    self.spawnPoints[1].spawnBalloon(self.balloons)
                elif ch == '9':
                    self.spawnPoints[2].spawnBalloon(self.balloons)
                elif ch == 'r':
                    if self.rageSpell:
                        self.rageSpell = 0
                        self.king.attack *= 2
                        self.king.cooldown /= 2
                        for barbarian in self.barbarians:
                            barbarian.attack *= 2
                            barbarian.cooldown /= 2
                        for archer in self.archers:
                            archer.attack *= 2
                            archer.cooldown /= 2
                        for balloon in self.balloons:
                            balloon.attack *= 2
                            balloon.cooldown /= 2
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
                        for archer in self.archers:
                            archer.health *= 1.5
                            if archer.health > archer.maxHealth:
                                archer.health = archer.maxHealth
                        for balloon in self.balloons:
                            balloon.health *= 1.5
                            if balloon.health > balloon.maxHealth:
                                balloon.health = balloon.maxHealth
                else:
                    self.king.updateMove(self.screen, ch)
            
            self.check_game_over()
            self.check_game_win()
            self.updateBuildings()
            self.updateArmy()
            self.updateColors()
            self.king.draw(self.screen.screen)

            self.screens.append(copy.deepcopy(self.screen.screen))
            self.screen.print()

            self.updateHUD()

            self.time += 1
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
    