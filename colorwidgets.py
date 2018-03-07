from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock

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

    def flashText(self, text, time=1):
        oldText = self.text
        self.text = text
        def changeText(text):
            self.text = text
        Clock.schedule_once(lambda _: changeText(oldText), time)

class TileButton(ColorButton):
    def __init__(self, tile):
        super(TileButton, self).__init__("plant", (1/5, 1/5), [0, 0, 0])
        self.tile = tile
        Clock.schedule_interval(self.update, 1/60)

    def update(self, _):
        if self.tile.berry and self.tile.time:
            displayText = str(self.tile.stage) + "\n" + str(truncate(time.time() - self.tile.time, 1))
            self.background_color = self.tile.berry.hue + [1]
            print("berry has been planted")
        elif self.tile.stage == "ripe":
            displayText = "4\nclick to harvest"
        else:
            displayText = "click to plant"
        self.text = displayText
