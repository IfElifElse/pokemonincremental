import random
import datetime

from player import Player
from tile import Tile

class Game(object):
    def __init__(self):
        self.player = Player()
        self.soil = [Tile(self.player) for _ in range(25)]
        self.selBerry = "cheri"

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
