from kivy.clock import Clock

import time

from berry import Berry

sCost = lambda x: int(.5*x**2)+1
gCost = lambda x: int(.75*x**2)+1
uCost = lambda x: int(2*x**2)+1

class BerryRef(object):
    def __init__(self, name):
        self.name = name
        self.count = 0
        self.growers = 0
        self.sellers = 0
        self.upgrade = 1

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
        self.berries[self.growing.name].count += self.berries[self.growing.name].upgrade
        self.growing = None

    def sell(self, berry):
        if self.berries[berry.name].count:
            self.berries[berry.name].count -= 1
            self.poke += berry.worth

    def buy(self, ree, berry):
        berryRef = self.berries[berry.name]
        if ree == "grower" and self.poke >= gCost(berryRef.growers):
            print("buying grower")
            self.poke -= gCost(berryRef.growers)
            berryRef.growers += 1
        if ree == "seller" and self.poke >= sCost(berryRef.sellers):
            print("buying seller")
            self.poke -= sCost(berryRef.sellers)
            berryRef.sellers += 1
        if ree == "upgrade" and self.poke >= uCost(berryRef.upgrade):
            print("buying upgrade")
            self.poke -= uCost(berryRef.upgrade)
            berryRef.upgrade += 1


    def newBerry(self, berry):
        if self.poke >= berry.growTime * 200:
            self.poke -= berry.growTime * 200
            self.berries[berry.name] = BerryRef(berry.name)
