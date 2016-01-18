from tgm.common import GameObject, sys_event
from tgm.drivers import get_engine
from tgm.engine.rendering import Window

engine = get_engine()


class MouseInput(GameObject):
    def create(self):
        self.down = set()
        self.pressed = set()
        self.released = set()
        self.ancestor_update()

    @sys_event
    def ancestor_update(self):
        print(self.tags.get(Window < GameObject))