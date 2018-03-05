from kivy.app import App
from kivy.uix.stacklayout import StackLayout
from kivy.clock import Clock

from colorwidgets import ColorButton, ColorLabel
from tile import Tile
from player import Player
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

class GameLayout(StackLayout):
    def __init__(self):
        super(GameLayout, self).__init__()
        self.player = Player()
        self.displist = []
        self.soil = []
        self.selBerry = "persim"
        self.displayMain()

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

    def displayMain(self):
        self.dispClear()
        black = [0, 0, 0]
        menuLayout = StackLayout(size_hint=[.1, 1])
        self.displist.append(menuLayout)

        plotLayout = StackLayout(size_hint=[.9, 1])
        self.displist.append(plotLayout)
        if not self.soil:
            for _ in range(25):
                tile = Tile(self.player)
                tile.bind(on_release=lambda t: t.plantBerry(self.selBerry))
                self.soil.append(tile)
        for tile in self.soil:
            plotLayout.add_widget(tile)

        self.dispAll()

class MyApp(App):
    def build(self):
        return GameLayout()

if __name__ == "__main__":
    MyApp().run()
