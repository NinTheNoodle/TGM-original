from tgm.system import Entity, sys_event
from tgm.ui import TabList
import tgm


class Editor(Entity):
    def create(self):
        tgm.collision.CollisionWorld(self)

    def start(self):
        self.taskbar = TaskBar(self)
        self.taskbar.x = 300
        self.taskbar.y = 300
        self.taskbar.add_task(5, "Home")
        self.taskbar.add_task(50, "Doom")
        self.taskbar.add_task(2, "Test")
        self.taskbar.add_task("HI", "Pie")


class TaskBar(Entity):
    def create(self):
        self.tablist = TabList(self)
        self.y_scale = 2
        self.x_scale = 0.5

    def add_task(self, pane, name):
        self.tablist.add_tab(name, lambda: print(name, pane))

    @sys_event
    def update(self):
        self.rotation += 1
