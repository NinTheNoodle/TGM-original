from collections import OrderedDict

from tgm.system import GameObject
from tgm.ui import Button


class TabList(GameObject):
    def on_create(self):
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


class TaskBar(GameObject):
    def on_create(self):
        self.tablist = TabList(self)
        self.panes = []

    def select(self, pane):
        for current_pane in self.panes:
            current_pane.disabled = current_pane != pane

    def add_task(self, pane, name):
        self.tablist.add_tab(name, lambda: self.select(pane))

        if self.panes:
            pane.disabled = True

        self.panes.append(pane)

    def on_add_child(self, child, name=None):
        if name is not None:
            self.add_task(child, name)
