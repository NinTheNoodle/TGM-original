from tgm.system import GameObject
from tgm.draw import Window
from tgm.collision import CollisionWorld
from tgm.input import Cursor


class DefaultEngine(GameObject):
    def on_create(self):
        CollisionWorld(self)
        Window(self, 800, 600)
        Cursor(self)
