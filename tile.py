from berry import Berry

import random

def frange(start, stop, step):
    i = start
    while i < stop:
        yield i
        i += step

class Tile(object):
    def __init__(self, player):
        self.berry = None
        self.stage = 0
        self.player = player

    def plantBerry(self, berryName):
        #if the button was pressed after the berry finished growing:
        if self.stage >= 4:
            if self.berry.name in self.player.berries:
                self.player.berries[self.berry.name] += 2
            else:
                self.player.berries[self.berry.name] = 2
            self.stage = 0
        #if the button was pressed and there were no berries and there is not a berry growing:
        elif self.player.berries[berryName] <= 0 and not self.berry:
            self.flashText("not enough berries")
        #if the button was pressed and there is not a berry growing"
        elif not self.berry:
            self.player.berries[berryName] -= 1
            self.berry = Berry(berryName)
            self.text = "growing %s berry" % self.berry.name
            self.background_color = self.berry.hue + [1]
            Clock.schedule_once(lambda _: self.growBerry(self), .75)

    def growBerry(self, tile): # called every frame
        if self.stage < 4:
            self.stage += 1
            newTime = random.choice([i for i in frange(self.berry.ripeTime-.25, self.berry.ripeTime+.25, .01)])
            Clock.schedule_once(lambda _: self.growBerry(self), newTime)
        else:
            self.text = "harvest"
