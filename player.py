from kivy.clock import Clock

import time

from berry import Berry

class BerryRef(object):
    def __init__(self, name):
        self.name = name
        self.count = 0
        self.growers = 0
        self.sellers = 0

class Player(object):
    def __init__(self):
        self.berries = {"cheri": BerryRef("cheri")}
        self.poke = 0
        self.pokedex = {}
        self.growing = None

    def grow(self, berry):
        if self.growing:
            return
        self.growing = berry
        self.started = time.time()
        Clock.schedule_once(self.harvest, self.growing.growTime/2)

    def harvest(self, _):
        self.berries[self.growing.name].count += 1
        self.growing = None

    def sell(self, berry):
        if self.berries[berry.name].count:
            self.berries[berry.name].count -= 1
            self.poke += berry.worth

    def buy(self, ree, berry):
        if ree == "berry":
            if berryName in self.berries:
                self.berries[berry.name].count += 1
            else:
                self.berries[berry.name] = 1
        if ree == "seller":
            print("buying seller")
            miniBerry = self.berries[berry.name]
            if self.poke >= int((.5*(miniBerry.sellers)**2)+1): # .5x^2
                print("bought")
                self.poke -= int((.5*(miniBerry.sellers)**2)+1)
                self.berries[berry.name].sellers += 1
