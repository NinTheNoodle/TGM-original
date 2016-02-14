from tgm.system import Entity, sys_event, Invisible
from tgm.drivers import get_engine
from .base import RenderContext

engine = get_engine()


class Sprite(Entity):
    def create(self, path):
        self.visible = True
        # self.image = engine.get_image(path)
        # self.sprite = engine.get_sprite(self.image)
        self.x_scale = 64
        self.y_scale = 64
        VertexList(
            self,
            points=(
                (-0.5, -0.5), (0.5, -0.5), (-0.5, 0.5),
                (-0.5, 0.5), (0.5, 0.5), (0.5, -0.5)
            ),
            colours=(
                (1, 0.5, 0.5), (1, 0.5, 0.5), (1, 0.5, 0.5),
                (1, 0.5, 0.5), (1, 1, 0.5), (1, 0.5, 0.5),
            )
        )


class VertexList(Entity):
    def create(self, points, colours=None, uvs=None, texture=None):
        self.updated = False
        self.points = points
        self.colours = colours
        self.texture = texture
        self.uvs = uvs

        self.target = self.tags.get_first(RenderContext < Entity).texture

        self.vertex_list = engine.VertexList(
            self.target,
            self.texture,
            None,
            self.get_points(),
            self.colours,
            self.uvs
        )

    @sys_event
    def transform_changed(self):
        self.updated = True

    def get_points(self):
        rtn = []

        for point in self.points:
            x, y, rot, x_scale, y_scale = self.transform.get_transform(
                transform=point + (0, 1, 1)
            )
            rtn.append((x, y))

        return rtn

    @sys_event
    def draw(self):
        if self.updated:
            self.vertex_list.points = self.get_points()
            self.updated = False

        self.vertex_list.update()


class RenderLayer(Entity):
    def create(self, below=False):
        self.below = below
        self.batch = engine.new_batch()

    @sys_event
    def render(self):
        engine.draw_batch(self.batch)

