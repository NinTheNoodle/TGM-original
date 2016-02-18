from collections import OrderedDict
from random import randint

from tgm.system import Entity, tgm_event
from tgm.draw import Sprite
from tgm.collision import BoxCollider
from tgm.input import Cursor


class Button(Entity):
    def create(self, image, text, callback=lambda x: None):
        self.callback = callback

        width = 64
        height = 32
        self.depth = -1

        self.sprite = Sprite(self, image)
        self.sprite.x_scale = width / self.sprite.width
        self.sprite.y_scale = height / self.sprite.height
        BoxCollider(self, width / 2, height / 2)

    @tgm_event
    def tgm_update(self):
        if self.collisions(Cursor[lambda x: "L" in x.pressed]):
            self.callback(self)


class TabList(Entity):
    def create(self):
        self.tabs = OrderedDict()

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

    # @sys_event
    # def update(self):
    #     self.rotation += 1

    # @sys_event
    # def update(self):
    #     buttons = self.children.copy()#self.tags.select(Button, enabled_only=False)
    #     for button in buttons:
    #         if randint(0, 60) == 0:
    #             #button.destroy()
    #             button.disabled = not button.disabled


class Pane(Entity):
    def create(self):
        self.sprite = Sprite(self, r"C:\Users\Docopoper\Desktop\Python Projects"
                                   r"\In Progress\ContributorTest\python.png")
