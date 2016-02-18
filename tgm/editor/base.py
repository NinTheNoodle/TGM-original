from tgm.system import Entity, tgm_event
from tgm.ui import TabList
import tgm


class Editor(Entity):
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

        cursor = self.tags.select(tgm.input.Cursor)[0]
        target = tgm.draw.Sprite(cursor, r"C:\Users\Docopoper\Desktop"
                                         r"\Python Projects\In Progress"
                                         r"\ContributorTest\python.png")
        self.taskbar = TaskBar(self)
        self.taskbar.x = 32
        self.taskbar.y = 570
        self.taskbar.add_task(target, "Home")
        self.taskbar.add_task(target, "Doom")
        self.taskbar.add_task(target, "Test")
        self.taskbar.add_task(target, "Pie")


class TaskBar(Entity):
    def create(self):
        self.tablist = TabList(self)

    def add_task(self, pane, name):
        def toggle():
            pane.disabled = not pane.disabled
        self.tablist.add_tab(name, toggle)

    # @sys_event
    # def update(self):
    #     self.rotation -= 1
