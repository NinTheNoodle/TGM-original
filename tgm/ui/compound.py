from collections import OrderedDict

from tgm.system import GameObject
from tgm.ui import Button


class ButtonList(GameObject):
    def on_create(self, vertical=False):
        self._vertical = vertical
        self.tabs = OrderedDict()

    def click_button(self, button):
        if isinstance(button, int):
            button = self.tabs.values[button]
        self.tabs[button]()

    def add_button(self, name, callback):
        icon = r"C:\Users\Docopoper\Desktop\Python Projects" \
               r"\In Progress\TGM\tgm\editor\assets\button.png"
        button = Button(self, icon, name, 64, 32,
                        lambda x: self.click_button(name))
        if self._vertical:
            button.y = -len(self.tabs) * 40
        else:
            button.x = len(self.tabs) * 70
        self.tabs[name] = callback


class TaskBar(GameObject):
    def on_create(self):
        self.tablist = ButtonList(self, False)
        self.panes = []

    def select(self, pane):
        for current_pane in self.panes:
            current_pane.disabled = current_pane != pane

    def add_task(self, pane, name):
        self.tablist.add_button(name, lambda: self.select(pane))

        if self.panes:
            pane.disabled = True

        self.panes.append(pane)

    def on_add_child(self, child, name=None):
        if name is not None:
            self.add_task(child, name)
