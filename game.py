import random
import datetime

from player import Player
from colorwidgets import Tile

class Game(object):
    def __init__(self):
        self.player = Player()
        self.soil = [Tile("plant", [1/5, 1/5], black) for i in range(25)]
