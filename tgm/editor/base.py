from tgm.system import Entity
from tgm.ui import TabList
import tgm


class Editor(Entity):
    def create(self):
        tgm.collision.CollisionWorld(self)
        self.taskbar = TaskBar(self)


class TaskBar(Entity):
    def create(self):
        self.tablist = TabList(self)
        self.tablist.add_tab()
        self.tablist.add_tab()
        self.tablist.add_tab()
        print(self.tablist.transform.transform)
