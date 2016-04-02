from tgm.system import GameObject
from tgm.input import Cursor
from tgm.draw import Sprite


class DefaultEngine(GameObject):
    def on_create(self):
        cursor = Cursor(self)
        cursor.depth = -1
        s = Sprite(cursor, "tgm.engine/assets/cursor.png")

        s.depth = -1000
