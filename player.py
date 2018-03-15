from kivy.clock import Clock

import time

from berry import Berry

class Player(object):
    def __init__(self):
        self.berries = {"cheri": 0}
        self.poke = 0
        self.pokedex = {}
        self.growing = None

    def grow(self, berry):
        if self.growing:
            return
        self.growing = berry
        self.started = time.time()
        Clock.schedule_once(self.harvest, self.growing.growTime/2)

    def mainLoop(self):
        if self.growing:
            timeDelta = time.time() - self.started
            return darkened(self.growing.hue, timeDelta*5)

    def harvest(self, _):
        self.berries[self.growing.name] += 1
        self.growing = None
