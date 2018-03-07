from berry import Berry

import random
import time

class Tile(object):
    def __init__(self):
        self.berry = None
        self.stage = 0
        self.time = None

    def plant(self, berryKind):
        if not self.berry:
            self.berry = Berry(berryKind)
            self.stage = 0
            self.time = time.time()
        else:
            self.pick()

    def update(self):
        if self.berry and not self.stage == "ripe":
            timeDiff = time.time() - self.time
            print("berry update for %s, time %s" % (self.berry.name, timeDiff))
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
            return berry
        else:
            return False
