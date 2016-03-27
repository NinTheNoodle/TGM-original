from tgm.system import GameObject
from tgm.input import Cursor
from tgm.draw import Sprite


class DefaultEngine(GameObject):
    def on_create(self):
        cursor = Cursor(self)
        cursor.depth = -1
        s = Sprite(cursor,
                   r"C:\Users\Docopoper\Desktop\Python Projects\In Progress"
                   r"\TGM\tgm\editor\assets\button.png")

        s.depth = -1000
