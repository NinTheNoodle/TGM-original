from tgm.common import GameObject, sys_event
from tgm.engine.transform import Transform
from tgm.drivers import get_engine

engine = get_engine()


class RenderContext(GameObject):
    @sys_event
    def render(self):
        self.parent.tags.select(
            GameObject[sys_event.render],
            stop=GameObject[RenderContext] - GameObject[self],
            abort=self
        ).render()


class Window(RenderContext):
    settings = {
        "width": 800,
        "height": 600
    }

    def create(self, width, height):
        self.window = engine.get_window(width, height)
        self.window.set_caption("TGM Sample")

        def on_draw():
            self.render()

        def on_mouse_move(x, y):
            self.parent.tags.select(
                    GameObject[sys_event.mouse_move]
            ).mouse_move(x, y)

        engine.render_loop(self.window, on_draw)
        engine.mouse_move_event(self.window, on_mouse_move)


class Sprite(GameObject):
    def create(self, path):
        self.visible = True
        self.image = engine.get_image(path)
        self.sprite = engine.get_sprite(self.image)
        self.transform = Transform(parent=self)

    @sys_event
    def render(self):
        x, y, rot, scale = self.transform.get_transform(
                GameObject[RenderContext])
        engine.draw_sprite(self.sprite, x, y, rot, scale)
