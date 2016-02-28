from collections import OrderedDict

from tgm.system import GameObject, tgm_event, Group
from tgm.draw import BorderedSprite, Sprite, Text
from tgm.collision import BoxCollider
from tgm.input import Cursor
from tgm.editor import (
    EditorObject, TextSetting, FileSetting, FunctionSetting, NumberSetting
)


class Button(GameObject):
    editor = EditorObject(
        image=TextSetting(""),
        text=FileSetting(""),
        callback=FunctionSetting(lambda x: None)
    )

    def create(self, image, text, callback=lambda x: None):
        self.text = text
        self.callback = callback

        width = 64
        height = 32
        self.depth = 0

        self.sprite = BorderedSprite(self, image, 4)
        self.sprite.width = width
        self.sprite.height = height
        self.label = Text(self, text)
        BoxCollider(self, width / 2, height / 2)

    @tgm_event
    def tgm_update(self):
        if self.collisions(Cursor[lambda x: "L" in x.pressed]):
            self.callback(self)


class TabList(GameObject):
    def create(self):
        self.tabs = OrderedDict()
        print(self.dir)

    def change_tab(self, tab):
        if isinstance(tab, int):
            tab = self.tabs.values[tab]
        self.tabs[tab]()

    def add_tab(self, name, callback):
        icon = r"C:\Users\Docopoper\Desktop\Python Projects" \
               r"\In Progress\TGM\tgm\editor\assets\button.png"
        button = Button(self, icon, name, lambda x: self.change_tab(name))
        button.x = len(self.tabs) * 70
        self.tabs[name] = callback


class Pane(GameObject):
    editor = EditorObject(
        image=TextSetting(""),
        width=NumberSetting(32),
        height=NumberSetting(32)
    )

    def create(self, image, width, height):
        self.sprite = BorderedSprite(self, image, 4)
        self.sprite.width = width
        self.sprite.height = height
