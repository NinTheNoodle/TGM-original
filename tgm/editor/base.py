from tgm.system import GameObject, Level
from tgm.ui import TabList
from tgm.draw import Sprite
import tgm


class Editor(GameObject):
    def create(self):
        tgm.collision.CollisionWorld(self)

    def start(self):
        self.sprite = tgm.draw.Sprite(
            self, r"C:\Users\Docopoper\Desktop"
                  r"\Python Projects\In Progress"
                  r"\TGM\tgm\editor\assets\back.png")
        self.sprite.x_scale = 800 / self.sprite.width
        self.sprite.y_scale = 600 / self.sprite.height
        self.sprite.x = 400
        self.sprite.y = 300
        self.sprite.depth = 5

        target = self.tags.select(Sprite < tgm.input.Cursor)[0]
        self.taskbar = TaskBar(self)
        self.taskbar.x = 32
        self.taskbar.y = 570
        self.taskbar.add_task(target, "Home")
        self.taskbar.add_task(target, "Doom")
        self.taskbar.add_task(target, "Test")
        self.taskbar.add_task(target, "Pie")

        Level(self, r"C:\Users\Docopoper\Desktop\Python Projects\In Progress\TGM\tgm\editor\assets\level_editor.json")


class TaskBar(GameObject):
    def create(self):
        self.tablist = TabList(self)

    def add_task(self, pane, name):
        def toggle():
            pane.disabled = not pane.disabled
        self.tablist.add_tab(name, toggle)
