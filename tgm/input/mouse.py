from tgm.system import Entity, sys_event, Transform
from tgm.drivers import get_engine
from tgm.draw import RenderContext
from tgm.collision import BoxCollider

engine = get_engine()


# class InputMapper(GameObject):
#     def create(self, input_map=None):
#         if input_map is None:
#             input_map = {}
#
#         self.input_map = input_map
#
#     def raw_input(self, input_type, *args, **kwargs):
#         sel = self.parent.tags.select(GameObject > self.input_map[input_type])
#         getattr(sel, self.input_map[input_type])(*args, **kwargs)
#
#
# class MouseInput(GameObject):
#     def create(self):
#         self.down = set()
#         self.pressed = set()
#         self.released = set()
#         self.x = 0
#         self.y = 0
#         self.ancestor_update()
#
#     @sys_event
#     def ancestor_update(self):
#         self.window = self.tags.get_first(RenderContext < GameObject)
#
#     @sys_event
#     def update(self):
#         self.x, self.y = engine.get_mouse_pos(self.window)


class Cursor(Entity):
    def create(self):
        self.mouse_x = 0
        self.mouse_y = 0
        self.down = set()
        self.pressed = set()
        self.released = set()
        BoxCollider(self, 1, 1)

    @sys_event
    def draw(self):
        self.transform.transform = self.transform.get_inverse_transform(
            (self.mouse_x, self.mouse_y, 0, 0.1),
            Entity[RenderContext]
        )

    @sys_event
    def update_init(self):
        mouse_state = engine.get_mouse_state(
            self.tags.get_first(RenderContext < Entity).window
        )
        self.mouse_x, self.mouse_y = mouse_state["pos"]
        prev_down = self.down.copy()
        self.down = mouse_state["buttons"]
        self.pressed = self.down - prev_down
        self.released = prev_down - self.down
