from berry import Berry

import random
import time

class Tile(object):
    def __init__(self, player):
        self.berry = None
        self.player = player
        self.stage = 0
        self.time = None

    def plant(self, berryKind):
        if not self.berry:
            if berryKind in self.player.berries:
                if self.player.berries[berryKind] < 1:
                    return "not enough berries"
            self.player.berries[berryKind] -= 1
            self.berry = Berry(berryKind)
            self.stage = 0
            self.time = time.time()
            return True
        else:
            self.pick()
            return "picked successfully"

    def update(self):
        if self.berry and not self.stage == "ripe":
            timeDiff = time.time() - self.time
            if (timeDiff > (self.berry.growTime)) and (not self.stage == "ripe"):
                self.time = time.time()
                self.stage += 1
            if self.stage >= 4:
                self.stage = "ripe"

    def pick(self):
        if self.stage == "ripe":
            berry = self.berry.name
            self.time = None
            self.stage = 0
            self.berry = None
            self.player.berries[berry] += 2
