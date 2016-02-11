from tgm.system import Entity, sys_event, Transform
from tgm.drivers import get_engine
from .base import RenderContext

engine = get_engine()


class Sprite(Entity):
    def create(self, path):
        self.visible = True
        self.image = engine.get_image(path)
        self.sprite = engine.get_sprite(self.image)
        self.transform.scale = 64
        VertexList(
            self,
            ((-0.5, -0.5), (1, 0.5, 0.5)),
            ((0.5, -0.5), (1, 0.5, 0.5)),
            ((-0.5, 0.5), (1, 0.5, 0.5)),

            ((-0.5, 0.5), (1, 0.5, 0.5)),
            ((0.5, 0.5), (1, 1, 0.5)),
            ((0.5, -0.5), (1, 0.5, 0.5))
        )


class VertexList(Entity):
    def create(self, *data):
        self.updated = False
        self.points, self.colours = list(zip(*data))

        self.batch = self.tags.get_first(RenderLayer < Entity).batch

        self.vertex_list = engine.add_vertex_list(
            self.batch, self.get_points(), self.colours)

    @sys_event
    def transform_changed(self):
        self.updated = True

    def get_points(self):
        rtn = []

        for point in self.points:
            x, y, rot, scale = self.transform.get_transform(
                transform=point + (0, 1)
            )
            rtn.append((x, y))

        return rtn

    @sys_event
    def draw(self):
        if self.updated:
            engine.modify_vertex_list(self.vertex_list, self.get_points())
            self.updated = False

        engine.vertex_list_tick(self.batch, self.vertex_list)


class RenderLayer(Entity):
    def create(self):
        self.batch = engine.new_batch()

    @sys_event
    def render(self):
        engine.draw_batch(self.batch)

