from tgm.system import GameObject, sys_event, Transform
from tgm.drivers import get_engine
from .base import RenderContext

engine = get_engine()


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
