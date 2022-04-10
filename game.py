from distutils.spawn import spawn
from re import A
from click import getchar
from src.input import input_to, newSettign, setBack
from src.map import Map
from src.buildings import *
from colorama import Fore, Back, Style
import time
from os import system
from src.character import *
import json

inputList = []
f = open('replay.json', 'r+')
toWrite = []


def mapgenerator():
    maps = []
    map = Map(100, 50)
    townhall = TownHall(40, 40, map)
    hut = Hut(20, 20, map)
    hut = Hut(22, 24, map)
    hut = Hut(24, 24, map)
    hut = Hut(40, 80, map)
    hut = Hut(30, 80, map)

    canon = Canon(30, 30, map)
    canon = Canon(40, 90, map)
    wizardTower = WizardTower(45, 50, map)
    wizardTower = WizardTower(45, 40, map)
    spawn1 = SpawningPoint(map.width - 2, 0, map)
    spawn2 = SpawningPoint(0, map.height - 2, map)
    spawn3 = SpawningPoint(0, int(map.height / 2), map)

    maps.append(map)
    del map

    map = Map(100, 50)
    townhall = TownHall(40, 40, map)
    hut = Hut(20, 20, map)
    hut = Hut(24, 30, map)
    hut = Hut(12, 40, map)
    hut = Hut(40, 80, map)
    hut = Hut(30, 80, map)
    canon = Canon(30, 30, map)
    canon = Canon(40, 90, map)
    canon = Canon(50, 80, map)
    wizardTower = WizardTower(45, 50, map)
    wizardTower = WizardTower(45, 40, map)
    wizardTower = WizardTower(20, 70, map)
    spawn1 = SpawningPoint(map.width - 2, 0, map)
    spawn2 = SpawningPoint(0, map.height - 2, map)
    spawn3 = SpawningPoint(0, int(map.height / 2), map)
    maps.append(map)

    del map

    map = Map(100, 50)
    townhall = TownHall(40, 40, map)
    hut = Hut(20, 20, map)
    hut = Hut(24, 30, map)
    hut = Hut(12, 40, map)
    hut = Hut(40, 80, map)
    hut = Hut(30, 80, map)
    canon = Canon(30, 30, map)
    canon = Canon(40, 90, map)
    canon = Canon(50, 80, map)
    canon = Canon(42, 70, map)
    wizardTower = WizardTower(45, 50, map)
    wizardTower = WizardTower(45, 40, map)
    wizardTower = WizardTower(20, 70, map)
    wizardTower = WizardTower(30, 40, map)
    spawn1 = SpawningPoint(map.width - 2, 0, map)
    spawn2 = SpawningPoint(0, map.height - 2, map)
    spawn3 = SpawningPoint(0, int(map.height / 2), map)

    maps.append(map)

    return maps


def maphelper(char, level, maps):
    kingOrQueen = None
    if char == 'K':
        kingOrQueen = King(maps[level])
    else:
        kingOrQueen = Queen(maps[level])
    spawn1 = SpawningPoint(maps[level].width - 2, 0, maps[level])
    spawn2 = SpawningPoint(0, maps[level].height - 2, maps[level])
    spawn3 = SpawningPoint(0, int(maps[level].height / 2), maps[level])

    return maps[level], kingOrQueen, spawn1, spawn2, spawn3


if __name__ == "__main__":
    def clear(): return system('clear')
    mainCharacter = input("King(K) or Queen(Q): ")
    newSettign()
    numBarabians = 0
    level = 0
    maps = mapgenerator()
    gameShouldRun = True

    map, kingOrQueen, spawn1, spawn2, spawn3 = maphelper(
        mainCharacter, level, maps)
    inputList.append(mainCharacter)
    while gameShouldRun:
        if level == 2:
            print()
        map.render()
        c = input_to(getchar)
        inputList.append(c)
        if c == '1':
            if map.numBarbarians < map.maxBarbarians:
                barbarian = Barbarian(map, spawn1.x, spawn1.y)
                map.numBarbarians += 1
        elif c == '2':
            if map.numBarbarians < map.maxBarbarians:
                barbarian = Barbarian(map, spawn2.x, spawn2.y)
                map.numBarbarians += 1
        elif c == '3':
            if map.numBarbarians < map.maxBarbarians:
                barbarian = Barbarian(map, spawn3.x, spawn3.y)
                map.numBarbarians += 1
        elif c == '4':
            if map.numArchers < map.maxArchers:
                archer = Archer(map, spawn1.x, spawn1.y)
                map.numArchers += 1
        elif c == '5':
            if map.numArchers < map.maxArchers:
                archer = Archer(map, spawn2.x, spawn2.y)
                map.numArchers += 1
        elif c == '6':
            if map.numArchers < map.maxArchers:
                archer = Archer(map, spawn3.x, spawn3.y)
                map.numArchers += 1
        elif c == '7':
            if map.numBallons < map.maxBallons:
                ballon = Ballon(map, spawn1.x, spawn1.y)
                map.numBallons += 1
        elif c == '8':
            if map.numBallons < map.maxBallons:
                ballon = Ballon(map, spawn2.x, spawn2.y)
                map.numBallons += 1
        elif c == '9':
            if map.numBallons < map.maxBallons:
                ballon = Ballon(map, spawn3.x, spawn3.y)
                map.numBallons += 1
        elif c == 'q':
            gameShouldRun = False
            setBack()
        elif c == 'r' and not kingOrQueen.rage:
            kingOrQueen.rage = True
            for chararcter in map.characters:
                if not chararcter.is_dead:
                    chararcter.atk = chararcter.atk*2
                    chararcter.rage = True
        elif c == 'h' and not kingOrQueen.healPotion:
            kingOrQueen.healPotion = True
            for character in map.characters:
                if not character.is_dead:
                    character.hp = 1.5*character.hp
                    if character.hp > character.max_health:
                        character.hp = character.max_health
        kingOrQueen.movement(c, map)
        time.sleep(0.07)
        clear()
        x = not map.checkLoose()
        if not x:
            clear()
            print(Fore.RED + 'You lost!')
            data = json.load(f)
            data.append(inputList)
            f.seek(0)
            json.dump(data, f)
            time.sleep(5)
            setBack()
            gameShouldRun = False
            # print(inputList)
        x = map.checkWin()
        if x:
            clear()
            if level == 2:
                print(Fore.GREEN + 'You won!')
                data = json.load(f)
                data.append(inputList)
                f.seek(0)
                json.dump(data, f)
                time.sleep(5)
                setBack()
                gameShouldRun = False
            else:
                level += 1
                map, kingOrQueen, spawn1, spawn2, spawn3 = maphelper(
                    mainCharacter, level, maps)
            # print(inputList)
