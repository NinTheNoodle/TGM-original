from tgm.common import GameObject, sys_event
from tgm.engine.transform import Transform
from tgm.drivers import get_engine

engine = get_engine()


class Window(GameObject):
    settings = {
        "width": 800,
        "height": 600
    }

    def create(self, width, height):
        self.window = engine.get_window()

        def on_draw():
            self.parent.tags.select(GameObject[sys_event.render]).render()

        engine.render_loop(self.window, on_draw)


class Sprite(GameObject):
    def create(self, path):
        self.visible = True
        self.image = engine.get_image(path)
        self.sprite = engine.get_sprite(self.image)
        self.transform = Transform(parent=self)

    @sys_event
    def render(self):
        x, y, rot, scale = self.transform.get_transform()
        engine.draw_sprite(self.sprite, x, y, rot, scale)
