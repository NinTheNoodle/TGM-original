from functools import partial

from tgm.system import Entity, sys_event
from tgm.draw import Sprite
from tgm.collision import BoxCollider
from tgm.input import Cursor


class Button(Entity):
    def create(self, callback=lambda x: None):
        self.callback = callback
        self.sprite = Sprite(self, r"C:\Users\Docopoper\Desktop\Python Projects"
                                   r"\In Progress\ContributorTest\python.png")
        BoxCollider(self, 32, 32)

    @sys_event
    def update(self):
        if set(*self.tags.select(
                Entity[sys_event.get_collisions]
        ).get_collisions(Cursor["clicking": True])):
            self.callback(self)


class TabList(Entity):
    def create(self):
        self.tabs = []
        self.x = 35
        self.y = 600 - 35

    def change_tab(self, number):
        print("change tab ", number)

    def add_tab(self):
        button = Button(self, lambda x: self.change_tab(self.tabs.index(x)))
        button.x = len(self.tabs) * 70
        button.transform.scale = 0.5
        print(button.transform.get_transform(), button.transform.parent_transform.transform)
        self.tabs.append(button)
