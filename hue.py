from kano_wand.kano_wand import Shop, Wand, PATTERN
from qhue import Bridge
import moosegesture as mg
import time
import random
import math

class GestureWand(Wand):
    def post_connect(self):
        self.gestures = {
            ("DL", "R", "DL"): "stupefy",
            ("DR", "R", "UR", "D"): "wingardium_leviosa",
            ("UL", "UR"): "reducio",
            ("DR", "U", "UR", "DR", "UR"): "flipendo",
            ("R", "D"): "expelliarmus",
            ("UR", "U", "D", "UL", "L", "DL"): "incendio",
            ("UR", "U", "DR"): "lumos",
            ("U", "D", "DR", "R", "L"): "locomotor",
            ("DR", "DL"): "engorgio",
            ("UR", "R", "DR"): "aguamenti",
            ("UR", "R", "DR", "UR", "R", "DR"): "avis",
            ("D", "R", "U"): "reducto"
        }
        self.spell = None
        self.pressed = False
        self.positions = []
        self.subscribe_button()
        self.subscribe_position()

    def on_position(self, x, y, pitch, roll):
        if self.pressed:
            self.positions.append(tuple([x, -1 * y]))

    def on_button(self, pressed):
        self.pressed = pressed

        if pressed:
            self.spell = None
        else:
            gesture = mg.getGesture(self.positions)
            self.positions = []
            closest = mg.findClosestMatchingGesture(gesture, self.gestures, maxDifference=1)

            if closest != None:
                self.spell = self.gestures[closest[0]]
                self.vibrate(PATTERN.SHORT)
            print("{}: {}".format(gesture, self.spell))

shop = Shop(wand_class=GestureWand)
wands = []

try:
    while len(wands) == 0:
        print("Scanning...")
        wands = shop.scan(connect=True)

except KeyboardInterrupt as e:
    for wand in wands:
        wand.disconnect()
