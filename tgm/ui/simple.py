from tgm.system import GameObject, tgm_event
from tgm.draw import BorderedSprite, Text
from tgm.collision import BoxCollider
from tgm.input import Cursor


class Button(GameObject):
    def on_create(self, image, text, width, height, callback=lambda x: None):
        self.text = text
        self.callback = callback
        self.depth = 0

        self.sprite = BorderedSprite(self, image, 4)
        self.sprite.width = width
        self.sprite.height = height
        self.label = Text(self, text)
        self.label.depth = -1
        BoxCollider(self, width, height)

    @tgm_event
    def tgm_update(self):
        if self.collisions(Cursor):#[lambda x: "L" in x.pressed]
            from random import random
            print(random())
            self.callback(self)
        #self.y_scale = 1
        self.x_scale = 2
        self.rotation += 1


class Pane(GameObject):
    def on_create(self, image, width, height):
        self.sprite = BorderedSprite(self, image, 4)
        self.sprite.width = width
        self.sprite.height = height

