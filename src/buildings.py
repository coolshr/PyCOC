from colorama import Fore, Back, Style
from numpy import False_
from pyparsing import Char


class Building:
    def __init__(self, x, y, char, color, health):
        self.x = x
        self.y = y
        self.name = char
        self.char = char
        self.color = color
        self.health = health
        self.max_health = health
        self.is_dead = False
    def damage(self, damage):
        self.health -= damage
        if self.health <= 0.66 * self.max_health:
            self.color = Back.YELLOW
        if self.health <= 0.33 * self.max_health:
            self.color = Back.RED
        if self.health <= 0:
            self.health = 0
            self.is_dead = True
            return True
        else:
            return False

class TownHall(Building):
    def __init__(self, x, y, map):
        super().__init__(x, y, 'T', Back.GREEN, 1000)
        map.buildings.append(self)
        map.addTownHall(x, y)   
        self.size = (4, 3)

class Hut(Building):
    def __init__(self, x, y, map):
        super().__init__(x, y, 'H', Back.GREEN, 250)
        map.buildings.append(self)
        map.addHut(x, y)   
        self.size = (2, 2)

class Wall(Building):
    def __init__(self, x, y, map):
        super().__init__(x, y, 'W', Back.GREEN, 10)
        map.buildings.append(self)
        self.size = (1, 1)

class Canon(Building):
    def __init__(self, x, y, map):
        super().__init__(x, y, 'C', Back.GREEN,300)
        map.buildings.append(self)
        self.size = (1, 1)
        self.attack = 800
        self.hit = 0
    def attack(self, target):
        target.damage(self.attack)

class SpawningPoint(Building):
    def __init__(self, x, y, map):
        super().__init__(x, y, 'S', Back.BLUE, 100)
        map.buildings.append(self)
        self.size = (1, 1)

class WizardTower(Building):
    def __init__(self, x, y, map):
        super().__init__(x, y, 'J', Back.BLUE, 500)
        map.buildings.append(self)
        self.size = (1, 1)
        self.attack = 800
        self.hit = 0
    def attack(self, target):
        target.damage(self.attack)