from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.stacklayout import StackLayout
from kivy.clock import Clock

from berry import Berry

import time

Builder.load_string("""
<ColorLabel>:
    text_size: self.size
    halign: "center"
    valign: "middle"
    canvas.before:
        BorderImage:
            pos: self.x - 1, self.y - 1
            size: self.width + 2, self.height + 2
        Color:
            rgb: self.rgb
        Rectangle:
            pos: self.pos
            size: self.size
<ColorButton>:
    text_size: self.size
    halign: "center"
    valign: "middle"
    background_normal: ""
    background_color: self.rgb
    canvas.before:
        BorderImage:
            pos: self.x - 1, self.y - 1
            size: self.width + 2, self.height + 2
""") # uses BorderImage and Rectangle to outline every widget in white

def truncate(f, n): # stolen from stackexchange :)
    s = '{}'.format(f)
    if 'e' in s or 'E' in s:
        return '{0:.{1}f}'.format(f, n)
    i, p, d = s.partition('.')
    return '.'.join([i, (d+'0'*n)[:n]])

class ColorLabel(Label):
    def __init__(self, text, sizehint, color):
        self.rgb = color
        super(ColorLabel, self).__init__(text=str(text), size_hint=sizehint)

    def flashText(self, text, time=1):
        oldText = self.text
        self.text = text
        def changeText(text):
            self.text = text
        Clock.schedule_once(lambda _: changeText(oldText), time)

class ColorButton(Button):
    def __init__(self, text, sizehint, color):
        mutedColor = []
        for colorValue in color:
            mutedColor.append(colorValue-(30/255))
        self.rgb = mutedColor+[1]
        super(ColorButton, self).__init__(text=str(text), size_hint=sizehint)
        self.flashing = False

    def flashText(self, text, time=1):
        self.flashing = True
        oldText = self.text
        self.text = text
        def changeText(text):
            self.text = text
            self.flashing = False
        Clock.schedule_once(lambda _: changeText(oldText), time)

class MenuBar(StackLayout):
    def __init__(self, **kwargs):
        super(MenuBar, self).__init__(**kwargs)
        self.widgList = []
        self.index = 0

    def add(self, widget):
        self.widgList.append(widget)

    def display(self):
        self.clear_widgets()

        indexes = range(self.index*5, (self.index+1)*5)
        unbind = False
        for i in indexes:
            try:
                self.add_widget(self.widgList[i])
            except IndexError:
                unbind = True
                break

    def pageChange(self, change):
        oldIndex = self.index
        self.index += change
        if self.index < 0 or (self.index+1)*5 > len(self.widgList)-1:
            self.index = oldIndex
        self.display()

class BerryButton(ColorButton):
    def __init__(self, player, berryName):
        self.berry = Berry(berryName)
        self.player = player
        super(BerryButton, self).__init__(self.berry.name, [1, 1/5], self.berry.hue)
        Clock.schedule_interval(self.update, 1/60)

    def update(self, _):
        self.text = self.berry.name + "\n" + str(self.player.berries[self.berry.name])

class TileButton(ColorButton):
    def __init__(self, tile):
        super(TileButton, self).__init__("plant", (1/5, 1/5), [0, 0, 0])
        self.tile = tile
        Clock.schedule_interval(self.update, 1/60)

    def update(self, _):
        if self.tile.stage == "ripe":
            displayText = "4\nclick to harvest"
        elif self.tile.berry and self.tile.time:
            displayText = str(self.tile.stage) + "\n" + str(truncate(time.time() - self.tile.time, 1))
            self.background_color = self.tile.berry.hue + [1]
        else:
            self.background_color = [0, 0, 0, 1]
            displayText = "click to plant"
        self.text = displayText

    def plant(self, berryType):
        success = self.tile.plant(berryType)
        if not success:
            self.flashText("fuck, you dont have berries")
