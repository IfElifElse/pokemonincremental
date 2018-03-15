import random
import datetime

from player import Player
from tile import Tile
from berry import Berry

class Game(object):
    def __init__(self):
        self.player = Player()
        self.soil = [Tile(self.player) for _ in range(25)]

    def mainLoop(self, _):
        for tile in self.soil:
            tile.update()

    def pick(self, n):
        berry = self.soil[n].pick()
        if berry:
            player.berries[berry] += 1
            return True
        else:
            return False

    def sell(self, berryName):
        if self.player.berries[berryName]:
            self.player.berries[berryName] -= 1
            self.player.poke += Berry(berryName).worth
