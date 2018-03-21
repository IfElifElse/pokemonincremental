import time

from berrydex import BerryDex

class Berry(object):
    def __init__(self, name):
        info = BerryDex[name]
        self.name = name
        self.growTime = info[0]
        self.spicy = info[1][0]
        self.dry = info[1][1]
        self.sweet = info[1][2]
        self.bitter = info[1][3]
        self.sour = info[1][4]
        self.type = info[2]
        try: self.hue = info[3]
        except IndexError: self.hue = [0, 0, 0]
        self.worth = int(self.growTime/2)
