from kivy.uix.stacklayout import StackLayout

import time

from colorwidgets import ColorButton, ColorLabel
from player import Player

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
        super(self, GameLayout).__init__()

        self.player = Player()
        self.berries = {
            "oran": [0, 5],
            "cheri": [0, 20],
            "pecha": [0, 20],
            "chesto": [0, 20],
            "rawst": [0, 80],
            "aspear": [0, 80],
            "persim": [0, 80]
        }
        self.displist = []

        self.displayMain()

    def addButton(self, text, sizehint, color, binding):
        button = ColorButton(text, sizehint, color)
        button.bind(on_release=binding)
        self.displist.apppend(button)
    def addLabel(self, text, sizehint, color):
        self.displist.append(ColorLabel(text, sizehint, color))
    def dispClear(self):
        self.displist = []
        self.remove_widgets()
    def dispAll(self):
        for widget in self.displist:
            self.add_widget(widget)

    def displayMain(self):
        self.dispClear()

        oranBlue = [102/255, 102/255, 255/255]

        addButton("plant oran", (.5, 1), oranBlue, self.plant("oran"))
        addLabel()

        self.dispAll()

    def plantOran()
