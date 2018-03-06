from berry import Berry

import random
import time

class Tile(object):
    def __init__(self):
        self.berry = None
        self.stage = 0

    def plant(self, berryKind):
        self.berry = Berry(berryKind)
        self.stage = 0
        self.time = time.time()

    def update(self):
        if self.berry:
            timeDiff = time.time() - self.time
            if timeDiff > (self.berry.growTime) and not self.stage == "ripe":
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
            return berry
        else:
            return False
