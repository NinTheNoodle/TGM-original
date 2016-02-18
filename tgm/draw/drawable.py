from tgm.system import Entity, tgm_event, Invisible
from tgm.drivers import get_engine
from .base import RenderContext

engine = get_engine()


class Sprite(Entity):
    def create(self, path):
        self.visible = True
        self.image = engine.Image(path)
        w = self.image.width / 2
        h = self.image.height / 2
        VertexList(
            self,
            points=(
                (-w, -h), (w, -h), (-w, h),
                (-w, h), (w, h), (w, -h)
            ),
            uvs=(
                (0, 0), (1, 0), (0, 1),
                (0, 1), (1, 1), (1, 0)
            ),
            texture=self.image
        )

    @property
    def width(self):
        return self.image.width

    @property
    def height(self):
        return self.image.height


class VertexList(Entity):
    def create(self, points, colours=None, uvs=None, texture=None):
        self.updated = False
        self.points = points
        self.colours = colours
        self.texture = texture
        self.uvs = uvs

        self.target = self.tags.get_first(RenderContext < Entity).window

        self.vertex_list = engine.VertexList(
            self.target,
            self.texture,
            self.computed_depth,
            self.get_points(),
            self.colours,
            self.uvs
        )

    @tgm_event
    def tgm_transform_changed(self):
        self.updated = True

    def get_points(self):
        rtn = []

        for point in self.points:
            x, y, rot, x_scale, y_scale = self.transform.get_transform(
                transform=point + (0, 1, 1)
            )
            rtn.append((x, y))

        return rtn

    @tgm_event
    def tgm_draw(self):
        if self.updated:
            self.vertex_list.points = self.get_points()
            self.updated = False

        self.vertex_list.update()
