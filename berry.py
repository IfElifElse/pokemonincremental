from berrydex import BerryDex

class Berry(object):
    def __init__(self, name):
        info = BerryDex[name]
        self.name = name
        self.ripeTime = info[0]
        self.spicy = info[1][0]
        self.dry = info[1][1]
        self.sweet = info[1][2]
        self.bitter = info[1][3]
        self.sour = info[1][4]
        self.type = info[2]
        self.hue = info[3]
