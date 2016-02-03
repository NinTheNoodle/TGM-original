from tgm.common import GameObject, sys_event, EventGroup
from tgm.drivers import get_engine
from tgm.engine.rendering import RenderContext
from tgm.engine.transform import Transform
from tgm.engine.colliders import BoxCollider

engine = get_engine()


class InputMapper(GameObject):
    def create(self, input_map=None):
        if input_map is None:
            input_map = {}

        self.input_map = input_map

    def raw_input(self, input_type, *args, **kwargs):
        sel = self.parent.tags.select(GameObject > self.input_map[input_type])
        getattr(sel, self.input_map[input_type])(*args, **kwargs)


class MouseInput(GameObject):
    def create(self):
        self.down = set()
        self.pressed = set()
        self.released = set()
        self.x = 0
        self.y = 0
        self.ancestor_update()

    @sys_event
    def ancestor_update(self):
        self.window = self.tags.get_first(RenderContext < GameObject)

    @sys_event
    def update(self):
        self.x, self.y = engine.get_mouse_pos(self.window)


class Cursor(GameObject):
    def create(self):
        self.transform = Transform(self)
        self.mouse_x = 0
        self.mouse_y = 0
        BoxCollider(self, 1, 1)

    @sys_event
    def draw(self):
        self.transform.transform = self.transform.get_inverse_transform(
            (self.mouse_x, self.mouse_y, 0, 0.4),
            GameObject[RenderContext]
        )

    @sys_event
    def mouse_move(self, x, y):
        self.mouse_x = x
        self.mouse_y = y
