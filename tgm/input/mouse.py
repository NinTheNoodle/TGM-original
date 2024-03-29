from tgm.system import GameObject, tgm_event
from tgm.drivers import get_engine
from tgm.draw import RenderContext, Window, Sprite
from tgm.collision import BoxCollider

engine = get_engine()


class Cursor(GameObject):
    def on_create(self):
        self.mouse_x = 0
        self.mouse_y = 0
        self.down = set()
        self.pressed = set()
        self.released = set()
        BoxCollider(self, 32, 32)

    @tgm_event
    def tgm_draw(self):
        self.transform.transform = self.transform.get_inverse_transform(
            (self.mouse_x, self.mouse_y, 0, 0.25, 0.25),
            GameObject[RenderContext]
        )

    @tgm_event
    def tgm_update_init(self):
        window = self.tags.get_first(Window)

        self.mouse_x, self.mouse_y = window.get_mouse_pos()
        prev_down = self.down.copy()
        self.down = window.get_mouse_buttons()
        self.pressed = self.down - prev_down
        self.released = prev_down - self.down
