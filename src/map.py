from colorama import Fore, Back, Style
from numpy import char
from src.buildings import Building, Wall
from src.character import Character, King
import math


class Map:
    def __init__(self, height, width,):
        self.width = width + 2
        self.height = height + 2
        self.map = []
        self.buildings = []
        self.characters = []
        self.numBarbarians = 0
        self.numBarbariansKilled = 0
        self.maxBarbarians = 6
        self.numArchers = 0
        self.numArchersKilled = 0
        self.maxArchers = 6
        self.numBallons = 0
        self.numBallonsKilled = 0
        self.maxBallons = 3
        for i in range(self.width):
            self.map.append([])
            if i >= 0 and i <= 2:
                for j in range(self.height):
                    self.map[i].append(' ')
            elif i == 3 or i == self.width - 1:
                for j in range(self.height):
                    if j >= 0 and j <= 2:
                        self.map[i].append(' ')
                    elif j <= self.height:
                        self.map[i].append(Back.GREEN + 'W' + Style.RESET_ALL)
                        wall = Wall(i, j, self)
            else:
                for j in range(self.height):
                    if j >= 0 and j <= 2:
                        self.map[i].append(' ')
                    elif j == 3 or j == self.height-1:
                        self.map[i].append(Back.GREEN + 'W' + Style.RESET_ALL)
                        wall = Wall(i, j, self)
                    else:
                        self.map[i].append(' ')

    def update(self):
        for character in self.characters:
            if not (character.name == 'K' or character.name == 'Q') and not character.is_dead:
                character.movement(self)
        frame = []
        for i in range(self.width):
            frame.append([])
            if i >= 0 and i <= 2:
                for j in range(self.height):
                    frame[i].append(' ')
            if i == 3 or i == self.width-1:
                for j in range(self.height):
                    if j >= 0 and j <= 2:
                        frame[i].append(' ')
                    else:
                        frame[i].append(' ')
            for j in range(self.height):
                if j >= 0 and j <= 2:
                    frame[i].append(' ')
                elif j == 3 or j == self.height-1:
                    frame[i].append(' ')
                else:
                    frame[i].append(' ')
        for building in self.buildings:
            if not building.is_dead:
                for i in range(building.x, building.x+building.size[0], 1):
                    for j in range(building.y, building.y+building.size[1], 1):
                        if i >= len(frame) or j >= len(frame[0]):
                            print("here")
                            print(i,j,building.name)
                            exit()  
                        frame[i][j] = building.color + \
                            building.char + Style.RESET_ALL

                if building.name == 'C':
                    building.hit += 1
                    building.color = Back.GREEN
                    # print("here")
                    if building.hit % 3 == 0:
                        character = self.attackCharacter(building)
                        if character != None and not character.is_dead and not character.name == 'G':
                            x = character.damage(building.attack)
                            if character.name == 'B':
                                if x:
                                    self.numBarbariansKilled += 1
                            if character.name == 'A':
                                if x:
                                    self.numArchersKilled += 1
                            if character.name == 'H':
                                if x:
                                    self.numBallonsKilled += 1
                            building.color = Back.WHITE + Fore.RED

                if building.name == 'J':
                    building.hit += 1
                    building.color = Back.GREEN
                    # print("here")
                    if building.hit % 3 == 0:
                        character = self.attackCharacter(building)
                        if character:
                            for i in range(character.x, character.x+3):
                                for j in range(character.y, character.y+3):
                                    for character in self.characters:
                                        if character.x == i and character.y == j:
                                            dead = character.damage(building.attack)
                                            if dead:
                                                if character.name == 'B':
                                                    self.numBarbariansKilled += 1
                                                if character.name == 'G':
                                                    self.numBallonsKilled += 1
                                                if character.name == 'A':
                                                    self.numArchersKilled += 1
                                            building.color = Back.WHITE + Fore.RED

        for character in self.characters:
            if (character.name == "K" or character.name == 'Q') and not character.is_dead:
                frame[character.x][character.y] = character.color + \
                    character.char[character.dir] + Style.RESET_ALL
            elif not character.is_dead:
                frame[character.x][character.y] = character.color + \
                    character.char + Style.RESET_ALL
        return frame

    def render(self):
        frame = self.update()
        toPrint = ""
        for i in frame:
            for j in i:
                # print(j, end='')
                toPrint += j
            # print()
            toPrint += '\n'
        for character in self.characters:
            if character.name == 'K' or character.name == 'Q':
                # print("Health of King:" + str(character.hp))
                toPrint += "Health of "
                toPrint += "King: " if character.name == 'K' else "Queen: "
                toPrint += str(character.hp)
                # make health bar
                hp = math.ceil(character.hp/character.max_health*30)
                for i in range(hp):
                    # print('█', end='')
                    toPrint += '█'
                for i in range(30-hp):
                    # print('░', end='')
                    toPrint += '░'
                # print()
                toPrint += '\n'
            # toPrint += "Health of Barbarian:" + str(character.hp)+'\n'
        print(toPrint)

    def addTownHall(self, x, y):
        for i in range(x, x+4, 1):
            for j in range(y, y+3, 1):
                self.map[i][j] = Back.GREEN + 'T' + Style.RESET_ALL

    def addHut(self, x, y):
        for i in range(x, x+2, 1):
            for j in range(y, y+2, 1):
                self.map[i][j] = Back.GREEN + 'H' + Style.RESET_ALL

    def addCharacter(self, character):
        self.map[character.x][character.y] = character.color + \
            character.name + Style.RESET_ALL

    def checkCollision(self, character):
        frame = []
        for i in range(self.width):
            frame.append([])
            if i >= 0 and i <= 2:
                for j in range(self.height):
                    frame[i].append(' ')
            if i == 3 or i == self.width-1:
                for j in range(self.height):
                    if j >= 0 and j <= 2:
                        frame[i].append(' ')
                    else:
                        frame[i].append(' ')
            for j in range(self.height):
                if j >= 0 and j <= 2:
                    frame[i].append(' ')
                elif j == 3 or j == self.height-1:
                    frame[i].append(' ')
                else:
                    frame[i].append(' ')
        for building in self.buildings:
            if not building.is_dead:
                for i in range(building.x, building.x+building.size[0], 1):
                    for j in range(building.y, building.y+building.size[1], 1):
                        frame[i][j] = building.color + \
                            building.char + Style.RESET_ALL

        if frame[character.x][character.y] == ' ':
            return False
        else:
            # print("Collision")
            return True

    def attackBuilding(self, pos):
        for building in self.buildings:
            if not building.is_dead:
                for i in range(building.x, building.x+building.size[0], 1):
                    for j in range(building.y, building.y+building.size[1], 1):
                        if i == pos['x'] and j == pos['y']:
                            return building
        return None

    def attackCharacter(self, canon):
        for character in self.characters:
            if not character.is_dead:
                x = character.x
                y = character.y
                dist = math.sqrt((x-canon.x)**2 + (y-canon.y)**2)
                if dist <= 7:
                    return character
        return None

    def checkLoose(self):
        if self.numBarbarians < self.maxBarbarians or self.numBarbariansKilled < self.maxBarbarians:
            return False
        if self.numArchers < self.maxArchers or self.numArchersKilled < self.maxArchers:
            return False
        if self.numBallons < self.maxBallons or self.numBallonsKilled < self.maxBallons:
            return False
        else:
            for character in self.characters:
                if (character.name == 'K' or character.name == 'Q') and character.hp > 0:
                    return False
            return True

    def checkWin(self):
        ans = True
        for building in self.buildings:
            if not building.name == 'W' and not building.name == 'S':
                if not building.is_dead:
                    return False
        return ans
