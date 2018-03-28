from kivy.app import App
from kivy.uix.stacklayout import StackLayout
from kivy.clock import Clock

from colorwidgets import *
from player import Player, sCost, gCost, uCost, BerryRef
from berry import Berry
from berrydex import BerryDex

import random

"""
plant oran berries
grow and collect them
sell them for money
buy more berries
lay out berries to attract pokemon
fill pokedex
combine berries to make poffins
"""

def darkened(colorList, darkened=30):
    return [color-(darkened/255) if color > (darkened/255) else 0 for color in colorList[:3]]

class GameLayout(StackLayout):
    def __init__(self):
        super(GameLayout, self).__init__()
        self.displist = []
        self.player = Player()
        self.displayBerry("cheri")
        self.growStarted = None
        self.sellStarted = None

    def addButton(self, text, sizehint, color, binding, parent=None):
        button = ColorButton(text, sizehint, color)
        button.bind(on_release=binding)
        if not parent:
            self.displist.append(button)
        else:
            parent.add_widget(button)
        return button
    def addLabel(self, text, sizehint, color, parent=None):
        label = ColorLabel(text, sizehint, color)
        if not parent:
            self.displist.append(label)
        else:
            parent.add_widget(label)
        return label
    def dispClear(self):
        self.displist = []
        self.clear_widgets()
    def dispAll(self):
        for widget in self.displist:
            self.add_widget(widget)

    def displayBerry(self, berryName):
        self.dispClear()
        black = [0, 0, 0]
        green = [5/255, 100/255, 5/255]
        self.berry = Berry(berryName)

        menuLayout = StackLayout(size_hint=[.1, 1])
        self.displist.append(menuLayout)

        #menu configuration
        self.moneyDisp = self.addLabel("", [1, .1], green, menuLayout)

        storeButton = self.addButton("Store", [1, .1], black, self.storeDisplay, menuLayout)

        self.menuBar = MenuBar(size_hint=[1, .5])
        upButton = self.addButton("^", [1, .15], black, lambda _: self.menuBar.pageChange(1), menuLayout)
        menuLayout.add_widget(self.menuBar)

        for berryName in self.player.berries:
            tBerry = Berry(berryName) #tberry is target berry
            berryBtn = ColorButton(tBerry.name, [1, .2], tBerry.hue)
            berryBtn.bind(on_release=lambda button: self.displayBerry(button.text))
            self.menuBar.add(berryBtn)

        self.menuBar.display()

        downButton = self.addButton("v", [1, .15], black, lambda _: self.menuBar.pageChange(-1), menuLayout)

        berryLayout = StackLayout(size_hint=[.9, 1])
        self.displist.append(berryLayout)

        #main configuration
        self.berryBtn = self.addButton(self.berry.name, [1, .8], self.berry.hue, lambda _: self.player.grow(self.berry), berryLayout)
        self.berryCount = self.addLabel("", [.2, .2], darkened(self.berry.hue), berryLayout)
        sellButton = self.addButton("sell", [.2, .2], darkened(self.berry.hue), lambda _: self.player.sell(self.berry), berryLayout)
        self.upgradeBtn = self.addButton("", [.2, .2], darkened(self.berry.hue), lambda _: self.player.buy("upgrade", self.berry), berryLayout)
        self.sellerBtn = self.addButton("", [.2, .2], darkened(self.berry.hue), lambda _: self.player.buy("seller", self.berry), berryLayout)
        self.growerBtn = self.addButton("", [.2, .2], darkened(self.berry.hue), lambda _: self.player.buy("grower", self.berry), berryLayout)

        for berry in self.player.berries:
            berry = self.player.berries[berry]
            Clock.schedule_interval(lambda _: self.sellLoop(berry), Berry(berry.name).growTime*1.5)
            Clock.schedule_interval(lambda _: self.growLoop(berry), Berry(berry.name).growTime)
        Clock.schedule_interval(self.mainLoop, 1/60)

        self.dispAll()

    def storeDisplay(self, _):
        self.dispClear()

        backButton = self.addButton("Back", [1, .05], [0, 0, 0], lambda _: self.displayBerry(self.berry.name))
        menuBar = MenuBar(size_hint=[1, .75])
        upButton = self.addButton("^", [1, .1], [0, 0, 0], lambda _: menuBar.pageChange(1))
        self.displist.append(menuBar)

        storeBerries = [Berry(berry) for berry in BerryDex if BerryDex[berry][0] <= 15]

        for berry in storeBerries:
            cost = berry.growTime * 200
            color = darkened(berry.hue, 150)
            func = lambda _: self.player.newBerry(berry) # assigning function newBerry() to func
            if berry.name in self.player.berries: #if the berry is unlocked
                color = berry.hue
                func = lambda _: 0

            button = ColorButton("%s\ncost: %s" % (berry.name, cost), [.2, .2], color)
            button.bind(on_release=func)
            menuBar.add(button)

        downButton = self.addButton("v", [1, .1], [0, 0, 0], lambda _: menuBar.pageChange(-1))

        self.dispAll()

    def mainLoop(self, _):
        #graphical stuff
        self.berryCount.text = "%s: %s" % (self.berry.name, self.player.berries[self.berry.name].count)
        self.moneyDisp.text = "poke: %s" % (self.player.poke)
        currentBerry = self.player.berries[self.berry.name]
        self.upgradeBtn.text = "%s per harvest\n\ncost: %s" % (currentBerry.upgrade, int(2*currentBerry.upgrade**2)+1)
        self.sellerBtn.text = "%s sellers\n%s\ncost: %s" % (self.berry.name, currentBerry.sellers, sCost(currentBerry.sellers))
        self.growerBtn.text = "%s growers\n%s\ncost: %s" % (self.berry.name, currentBerry.growers, gCost(currentBerry.growers))

        #button timed shading
        if self.player.growing:
            timeDelta = time.time() - self.player.started
            self.berryBtn.background_color = darkened(self.berry.hue, timeDelta/2) + [1]
        else:
            self.berryBtn.background_color = self.berry.hue + [1]
        if self.sellStarted:
            timeDelta = time.time() - self.sellStarted
            self.sellerBtn.background_color = darkened(self.berry.hue, timeDelta/6) + [1]
        if self.growStarted:
            timeDelta = time.time() - self.growStarted
            self.growerBtn.background_color = darkened(self.berry.hue, timeDelta/4) + [1]

    def growLoop(self, berry):
        if berry.name == self.berry.name and self.player.berries[self.berry.name].growers:
            self.growStarted = time.time()
        for _ in range(berry.growers):
            berry.count += 1

    def sellLoop(self, berry):
        if berry.name == self.berry.name and self.player.berries[self.berry.name].sellers:
            self.sellStarted = time.time()
        for _ in range(berry.sellers):
            self.player.sell(self.berry)

class MyApp(App):
    def build(self):
        return GameLayout()

if __name__ == "__main__":
    MyApp().run()
