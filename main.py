from kivy.app import App
from kivy.uix.stacklayout import StackLayout
from kivy.clock import Clock

from colorwidgets import *
from player import Player
from berry import Berry

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
    return [color-darkened if color > darkened else 0 for color in colorList[:3]]

class GameLayout(StackLayout):
    def __init__(self):
        super(GameLayout, self).__init__()
        self.displist = []
        self.player = Player()
        self.displayBerry("cheri")

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
        moneyDisplay = self.addLabel("", [1, .1], green, menuLayout)

        storeButton = self.addButton("Store", [1, .1], black, lambda _: self.switchScreen(button.text), menuLayout)

        self.menuBar = MenuBar(size_hint=[1, .5])
        upButton = self.addButton("^", [1, .15], black, lambda _: self.menuBar.pageChange(1), menuLayout)
        menuLayout.add_widget(self.menuBar)

        for berryName in self.player.berries:
            tBerry = Berry(berryName) #tberry is target berry
            berryButton = ColorButton(tBerry.name, [1, .2], tBerry.hue)
            berryButton.bind(on_release=lambda button: self.switchScreen(button.text))
            self.menuBar.add(berryButton)

        self.menuBar.display()

        downButton = ColorButton("v", [1, .15], black)
        downButton.bind(on_release=lambda _: self.menuBar.pageChange(-1))
        menuLayout.add_widget(downButton)

        berryLayout = StackLayout(size_hint=[.9, 1])
        self.displist.append(berryLayout)

        #main configuration
        berryButton = self.addButton(self.berry.name, [1, .8], self.berry.hue, lambda _: self.player.grow(self.berry), berryLayout)
        berryCount = self.addLabel("", [.2, .2], darkened(self.berry.hue), berryLayout)
        sellButton = self.addButton("sell", [.2, .2], darkened(self.berry.hue), lambda _: self.player.sell(self.berry), berryLayout)
        collectorButton = self.addButton("", [.2, .2], darkened(self.berry.hue), lambda _: self.player.buy("seller", self.berry), berryLayout)

        def mainLoop(_):
            berryCount.text = str(self.player.berries[self.berry.name].count)
            moneyDisplay.text = str(self.player.poke)
            collectorButton.text = "%s sellers\n\n%s" % (self.berry.name, self.player.berries[self.berry.name].sellers)
            if self.player.growing:
                print("ree")
                timeDelta = time.time() - self.player.started
                berryButton.background_color = darkened(self.berry.hue, timeDelta/2) + [1]
            else:
                berryButton.background_color = self.berry.hue + [1]
        Clock.schedule_interval(mainLoop, 1/60)

        self.dispAll()


class MyApp(App):
    def build(self):
        return GameLayout()

if __name__ == "__main__":
    MyApp().run()
