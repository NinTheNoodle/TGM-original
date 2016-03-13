from tgm.system import GameObject, Level
import tgm


class Editor(GameObject):
    def on_create(self):
        self.taskbar = tgm.ui.TaskBar(self)
        self.taskbar.y = 25
        self.taskbar.x = 40

    def on_add_child(self, child, tab=None):
        if tab is not None:
            self.taskbar.add_task(child, tab)

    @tgm.system.tgm_event
    def tgm_update(self):
        self.x = self.parent.parent.parent.context.width / 2 - 400
        self.y = self.parent.parent.parent.context.height / 2 - 300
