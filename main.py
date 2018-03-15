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

def darkened(colorList):
    return [color-30 if color > 30 else 0 for color in colorList[:3]]

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
        self.berry = Berry(berryName)

        menuLayout = StackLayout(size_hint=[.1, 1])
        self.displist.append(menuLayout)

        #menu configuration
        upButton = ColorButton("^", [1, .15], black)
        menuLayout.add_widget(upButton)

        self.menuBar = MenuBar(size_hint=[1, .7])
        menuLayout.add_widget(self.menuBar)

        upButton.bind(on_release=lambda _: self.menuBar.pageChange(1))

        for berryName in self.player.berries:
            tBerry = Berry(berryName) #tberry is target berry
            berryButton = ColorButton(tBerry.name, [1, 1/5], tBerry.hue)
            berryButton.bind(on_release=lambda button: self.switchScreen(button.text))
            self.menuBar.add(berryButton)

        self.menuBar.display()

        downButton = ColorButton("v", [1, .15], black)
        downButton.bind(on_release=lambda _: self.menuBar.pageChange(-1))
        menuLayout.add_widget(downButton)

        berryLayout = StackLayout(size_hint=[.9, 1])
        self.displist.append(berryLayout)

        #main configuration
        self.addButton(self.berry.name, [1, .8], self.berry.hue, lambda _: self.player.grow(self.berry), berryLayout)
        berryCount = self.addLabel(str(self.player.berries[self.berry.name]), [.2, .2], darkened(self.berry.hue), berryLayout)
        Clock.schedule_interval(lambda _: berryCount.changeText(str(self.player.berries[self.berry.name])), 1/60)

        self.dispAll()

class MyApp(App):
    def build(self):
        return GameLayout()

if __name__ == "__main__":
    MyApp().run()
