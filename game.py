import random
import datetime

from player import Player
from tile import Tile

class Game(object):
    def __init__(self):
        self.player = Player()
        self.soil = [Tile() for _ in range(25)]
        self.selBerry = "cheri"

    def mainLoop(self):
        for tile in self.soil:
            tile.update()

    def plant(self, n, berryType):
        self.soil[n].plant(berryType)

    def pick(self, n):
        berry = self.soil[n].pick()
        if berry:
            player.berries[berry] += 1
            return True
        else:
            return False
