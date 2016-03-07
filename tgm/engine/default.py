from tgm.system import GameObject
from tgm.collision import CollisionWorld
from tgm.input import Cursor


class DefaultEngine(GameObject):
    def on_create(self):
        CollisionWorld(self)
        Cursor(self).depth = -1
