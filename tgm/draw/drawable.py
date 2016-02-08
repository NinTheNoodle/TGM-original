from tgm.system import Entity, sys_event, Transform
from tgm.drivers import get_engine
from .base import RenderContext

engine = get_engine()

###########
import pyglet


class Sprite(Entity):
    def create(self, path):
        self.visible = True
        self.image = engine.get_image(path)
        self.sprite = engine.get_sprite(self.image)
        #self.transform = Transform(parent=self)
        #VertexList(self)

    @sys_event
    def render(self):
        x, y, rot, scale = self.transform.get_transform(
                Entity[RenderContext])
        engine.draw_sprite(self.sprite, x, y, rot, scale)


class VertexList(Entity):
    def create(self, *points):

        self.vertex_list = pyglet.graphics.vertex_list(2,
            ('v2i', (10, 15, 30, 35)),
            ('c3B', (0, 0, 255, 0, 255, 0))
        )

    @sys_event
    def render(self):
        self.vertex_list.draw(pyglet.gl.GL_POINTS)
