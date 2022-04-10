from email.policy import default
from unittest import case
from colorama import Fore, Back, Style
import math
import time
from numpy import char


class Character:
    def __init__(self, name, hp, atk, x=0, y=0):
        self.name = name
        self.hp = hp
        self.atk = atk
        self.x = x
        self.y = y
        self.is_dead = False
        self.max_health = hp

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def damage(self, damage):
        self.hp -= damage
        if self.hp <= 0.66 * self.max_health:
            self.color = Back.YELLOW
        if self.hp <= 0.33 * self.max_health:
            self.color = Back.RED
        if self.hp <= 0:
            self.hp = 0
            self.is_dead = True
            return True
        else:
            return False

    def __str__(self):
        return Back.GREEN + self.name + Style.RESET_ALL


class King(Character):
    def __init__(self, map):
        super().__init__('K', 1000, 90)
        self.color = Back.GREEN + Fore.BLUE
        self.char = ['>', '<', '^', 'v']
        self.dir = 0
        map.characters.append(self)
        map.addCharacter(self)
        self.rage = False
        self.speed = 1
        self.healPotion = False

    def movement(self, inp, map):
        if self.is_dead:
            return
        if inp == 'w':
            self.move(-self.speed, 0)
            if map.checkCollision(self):
                self.move(self.speed, 0)
            self.dir = 2
            if self.rage:
                self.move(-self.speed, 0)
                if map.checkCollision(self):
                    self.move(self.speed, 0)
        elif inp == 'a':
            self.move(0, -self.speed)
            if map.checkCollision(self):
                self.move(0, self.speed)
            self.dir = 1
            if self.rage:
                self.move(0, -self.speed)
                if map.checkCollision(self):
                    self.move(0, self.speed)
        elif inp == 's':
            self.move(self.speed, 0)
            if map.checkCollision(self):
                self.move(-self.speed, 0)
            self.dir = 3
            if self.rage:
                self.move(self.speed, 0)
                if map.checkCollision(self):
                    self.move(-self.speed, 0)
        elif inp == 'd':
            self.move(0, self.speed)
            if map.checkCollision(self):
                self.move(0, -self.speed)
            self.dir = 0
            if self.rage:
                self.move(0, self.speed)
                if map.checkCollision(self):
                    self.move(0, -self.speed)
        elif inp == ' ':
            pos = {'x': 0, 'y': 0}
            if self.dir == 0:
                pos['x'], pos['y'] = self.x, self.y + 1
            elif self.dir == 1:
                pos['x'], pos['y'] = self.x, self.y - 1
            elif self.dir == 2:
                pos['x'], pos['y'] = self.x-1, self.y
            elif self.dir == 3:
                pos['x'], pos['y'] = self.x+1, self.y
            buildingAttacked = map.attackBuilding(pos)
            if buildingAttacked:
                buildingAttacked.damage(self.atk)

        elif inp == 'l':
            buildingsToAttack = []
            for building in map.buildings:
                if not building.is_dead and not building.char == 'S':
                    d = 100000
                    for i in range(building.x, building.x+building.size[0], 1):
                        for j in range(building.y, building.y+building.size[1], 1):
                            d1 = math.sqrt((i-self.x)**2 + (j-self.y)**2)
                            if d1 < d:
                                d = d1
                    if d <= 5:
                        buildingsToAttack.append(building)
            for building in buildingsToAttack:
                building.damage(self.atk)
        


class Barbarian(Character):
    def __init__(self, map, x, y):
        super().__init__('B', 200, 20, x=x, y=y)
        self.color = Back.GREEN + Fore.RED
        self.char = 'B'
        self.dir = 0
        map.characters.append(self)
        map.addCharacter(self)
        self.rage = False
        self.movementSpeed = 1

    def __movement(self, map, buildingAttacked, toGo):
        if buildingAttacked:
            if toGo['x'] < self.x:
                self.move(-1, 0)
                if map.checkCollision(self):
                    self.move(1, 0)
                self.dir = 2
            elif toGo['x'] > self.x:
                self.move(1, 0)
                if map.checkCollision(self):
                    self.move(-1, 0)
                self.dir = 3
            elif toGo['y'] < self.y:
                self.move(0, -1)
                if map.checkCollision(self):
                    self.move(0, 1)
                self.dir = 1
            elif toGo['y'] > self.y:
                self.move(0, 1)
                if map.checkCollision(self):
                    self.move(0, -1)
                self.dir = 0

    def movement(self, map):
        if self.rage:
            self.movementSpeed = 2
        dist = 100000
        toGo = {'x': 0, 'y': 0}
        buildingAttacked = None
        for building in map.buildings:
            if not building.name == 'W' and not building.name == 'S' and building.is_dead == False:
                d = 100000
                tempTogo = {'x': 0, 'y': 0}
                for i in range(building.x, building.x + building.size[0], 1):
                    for j in range(building.y, building.y+building.size[1], 1):
                        d1 = math.sqrt((i-self.x)**2 + (j-self.y)**2)
                        if d1 < d:
                            d = d1
                            tempTogo['x'] = i
                            tempTogo['y'] = j
                if d < dist:
                    dist = d
                    toGo = tempTogo
                    buildingAttacked = building
        for i in range(self.movementSpeed):
            self.__movement(map, buildingAttacked, toGo)
        pos = {'x': 0, 'y': 0}
        if self.dir == 0:
            pos['x'], pos['y'] = self.x, self.y + 1
        elif self.dir == 1:
            pos['x'], pos['y'] = self.x, self.y - 1
        elif self.dir == 2:
            pos['x'], pos['y'] = self.x-1, self.y
        elif self.dir == 3:
            pos['x'], pos['y'] = self.x+1, self.y
        buildingAttacked = map.attackBuilding(pos)
        if buildingAttacked:
            buildingAttacked.damage(self.atk)


class Archer(Character):
    def __init__(self, map, x, y):
        super().__init__('A', 100, 10, x=x, y=y)
        self.color = Back.GREEN + Fore.RED
        self.char = 'A'
        self.dir = 0
        map.characters.append(self)
        map.addCharacter(self)
        self.rage = False
        self.movementSpeed = 2

    def __movement(self, map, buildingAttacked, toGo):
        if buildingAttacked:
            if toGo['x'] < self.x:
                self.move(-1, 0)
                if map.checkCollision(self):
                    self.move(1, 0)
                self.dir = 2
            elif toGo['x'] > self.x:
                self.move(1, 0)
                if map.checkCollision(self):
                    self.move(-1, 0)
                self.dir = 3
            elif toGo['y'] < self.y:
                self.move(0, -1)
                if map.checkCollision(self):
                    self.move(0, 1)
                self.dir = 1
            elif toGo['y'] > self.y:
                self.move(0, 1)
                if map.checkCollision(self):
                    self.move(0, -1)
                self.dir = 0

    def movement(self, map):
        if self.rage:
            self.movementSpeed = 4
        dist = 100000
        toGo = {'x': 0, 'y': 0}
        buildingAttacked = None
        for building in map.buildings:
            if not building.name == 'W' and not building.name == 'S' and building.is_dead == False:
                d = 100000
                tempTogo = {'x': 0, 'y': 0}
                for i in range(building.x, building.x + building.size[0], 1):
                    for j in range(building.y, building.y+building.size[1], 1):
                        d1 = math.sqrt((i-self.x)**2 + (j-self.y)**2)
                        if d1 < d:
                            d = d1
                            tempTogo['x'] = i
                            tempTogo['y'] = j
                if d < dist:
                    dist = d
                    toGo = tempTogo
                    buildingAttacked = building
        for i in range(self.movementSpeed):
            self.__movement(map, buildingAttacked, toGo)

        pos = {'x': 0, 'y': 0}
        if self.dir == 0:
            pos['x'], pos['y'] = self.x, self.y + 1
        elif self.dir == 1:
            pos['x'], pos['y'] = self.x, self.y - 1
        elif self.dir == 2:
            pos['x'], pos['y'] = self.x-1, self.y
        elif self.dir == 3:
            pos['x'], pos['y'] = self.x+1, self.y
        buildingAttacked = map.attackBuilding(pos)
        if buildingAttacked:
            buildingAttacked.damage(self.atk)
        else:
            buildingsToAttack = None
            for building in map.buildings:
                if not building.is_dead and not building.char == 'S':
                    d = 100000
                    for i in range(building.x, building.x+building.size[0], 1):
                        for j in range(building.y, building.y+building.size[1], 1):
                            d1 = math.sqrt((i-self.x)**2 + (j-self.y)**2)
                            if d1 < d:
                                d = d1
                    if d <= 5:
                        buildingsToAttack = building
            if not buildingsToAttack == None:
                buildingsToAttack.damage(self.atk)


class Ballon(Character):
    def __init__(self, map, x, y):
        super().__init__('G', 200, 40, x=x, y=y)
        self.color = Back.GREEN + Fore.RED
        self.char = 'G'
        self.dir = 0
        map.characters.append(self)
        map.addCharacter(self)
        self.rage = False
        self.movementSpeed = 2

    def __movement(self, map, buildingAttacked, toGo):
        if buildingAttacked:
            if toGo['x'] < self.x:
                self.move(-1, 0)
                self.dir = 2
            elif toGo['x'] > self.x:
                self.move(1, 0)
                self.dir = 3
            if toGo['y'] < self.y:
                self.move(0, -1)
                self.dir = 1
            elif toGo['y'] > self.y:
                self.move(0, 1)
                self.dir = 0

    def movement(self, map):
        if self.rage:
            self.movementSpeed = 4
        dist = 100000
        toGo = {'x': 0, 'y': 0}
        buildingAttacked = None
        for building in map.buildings:
            if not building.name == 'W' and (building.name == 'C' or building.name == 'J') and building.is_dead == False:
                d = 100000
                tempTogo = {'x': 0, 'y': 0}
                for i in range(building.x, building.x + building.size[0], 1):
                    for j in range(building.y, building.y+building.size[1], 1):
                        d1 = math.sqrt((i-self.x)**2 + (j-self.y)**2)
                        if d1 < d:
                            d = d1
                            tempTogo['x'] = i
                            tempTogo['y'] = j
                if d < dist:
                    dist = d
                    toGo = tempTogo
                    buildingAttacked = building
        if buildingAttacked == None:
            for building in map.buildings:
                if not building.name == 'W' and not building.name == 'S' and not building.is_dead:
                    d = 100000
                    tempTogo = {'x': 0, 'y': 0}
                    for i in range(building.x, building.x + building.size[0], 1):
                        for j in range(building.y, building.y+building.size[1], 1):
                            d1 = math.sqrt((i-self.x)**2 + (j-self.y)**2)
                            if d1 < d:
                                d = d1
                                tempTogo['x'] = i
                                tempTogo['y'] = j
                    if d < dist:
                        dist = d
                        toGo = tempTogo
                        buildingAttacked = building
        for i in range(self.movementSpeed):
            self.__movement(map, buildingAttacked, toGo)
        buildingAttacked = None
        pos = {'x': self.x, 'y': self.y}
        buildingAttacked = map.attackBuilding(pos)
        if buildingAttacked == None:
            if self.dir == 0:
                pos['x'], pos['y'] = self.x, self.y + 1
            elif self.dir == 1:
                pos['x'], pos['y'] = self.x, self.y - 1
            elif self.dir == 2:
                pos['x'], pos['y'] = self.x-1, self.y
            elif self.dir == 3:
                pos['x'], pos['y'] = self.x+1, self.y
            buildingAttacked = map.attackBuilding(pos)
        if buildingAttacked:
            buildingAttacked.damage(self.atk)


class Queen(Character):
    def __init__(self, map):
        super().__init__('Q', 1000, 90)
        self.color = Back.GREEN + Fore.BLUE
        self.char = ['>', '<', '^', 'v']
        self.dir = 0
        map.characters.append(self)
        map.addCharacter(self)
        self.rage = False
        self.speed = 1
        self.healPotion = False
        self.attackFlag = False
        self.attackTime = 0

    def movement(self, inp, map):
        if self.is_dead:
            return
        if inp == 'w':
            self.move(-self.speed, 0)
            if map.checkCollision(self):
                self.move(self.speed, 0)
            self.dir = 2
            if self.rage:
                self.move(-self.speed, 0)
                if map.checkCollision(self):
                    self.move(self.speed, 0)
        elif inp == 'a':
            self.move(0, -self.speed)
            if map.checkCollision(self):
                self.move(0, self.speed)
            self.dir = 1
            if self.rage:
                self.move(0, -self.speed)
                if map.checkCollision(self):
                    self.move(0, self.speed)
        elif inp == 's':
            self.move(self.speed, 0)
            if map.checkCollision(self):
                self.move(-self.speed, 0)
            self.dir = 3
            if self.rage:
                self.move(self.speed, 0)
                if map.checkCollision(self):
                    self.move(-self.speed, 0)
        elif inp == 'd':
            self.move(0, self.speed)
            if map.checkCollision(self):
                self.move(0, -self.speed)
            self.dir = 0
            if self.rage:
                self.move(0, self.speed)
                if map.checkCollision(self):
                    self.move(0, -self.speed)

        elif inp == ' ':
            pos = {'x': 0, 'y': 0}
            if self.dir == 0:
                pos['x'], pos['y'] = self.x, self.y + 8
            elif self.dir == 1:
                pos['x'], pos['y'] = self.x, self.y - 8
            elif self.dir == 2:
                pos['x'], pos['y'] = self.x - 8, self.y
            elif self.dir == 3:
                pos['x'], pos['y'] = self.x + 8, self.y
            for x in range(pos['x'] - 2, pos['x'] + 3):
                for y in range(pos['y'] - 2, pos['y'] + 3):
                    for building in map.buildings:
                        attacked = False
                        for x1 in range(building.x, building.x + building.size[0]):
                            for y1 in range(building.y, building.y + building.size[1]):
                                if x == x1 and y == y1:
                                    building.damage(self.atk)
                                    attacked = True
                                    break
                        if attacked:
                            break

        elif inp == 'l':
            if not self.attackFlag:
                self.attackFlag = True
                self.attackTime = time.time()
                self.specialAttackPos = {'x': 0, 'y': 0}
                pos = {'x': 0, 'y': 0}
                if self.dir == 0:
                    pos['x'], pos['y'] = self.x, self.y + 16
                elif self.dir == 1:
                    pos['x'], pos['y'] = self.x, self.y - 16
                elif self.dir == 2:
                    pos['x'], pos['y'] = self.x - 16, self.y
                elif self.dir == 3:
                    pos['x'], pos['y'] = self.x + 16, self.y
                self.specialAttackPos = pos
                return
            if self.attackFlag and not time.time() - self.attackTime >= 1:
                return
        if self.attackFlag and time.time() - self.attackTime >= 1:
            self.attackFlag = False
            pos = self.specialAttackPos
            for x in range(pos['x'] - 4, pos['x'] + 5):
                for y in range(pos['y'] - 4, pos['y'] + 5):
                    for building in map.buildings:
                        attacked = False
                        for x1 in range(building.x, building.x + building.size[0]):
                            for y1 in range(building.y, building.y + building.size[1]):
                                if x == x1 and y == y1:
                                    building.damage(self.atk)
                                    attacked = True
                                    break
                        if attacked:
                            break
