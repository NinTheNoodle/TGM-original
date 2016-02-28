from tgm.system import GameObject, tgm_event
from tgm.drivers import get_engine
from tgm.draw import RenderContext

engine = get_engine()


class Sprite(GameObject):
    def create(self, path):
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


class BorderedSprite(GameObject):
    def create(self, path, border_size):
        self.image = engine.Image(path)
        self._width = self.image.width
        self._height = self.image.height
        self._border_size = border_size
        w = self.width / 2
        h = self.height / 2
        b = self._border_size / 2
        self.vertex_list = VertexList(
            self,
            points=self._get_pts(0, 0, w, h, b, b),
            uvs=self._get_pts(0.5, 0.5, 0.5, 0.5, b / w, b / h),
            texture=self.image
        )

    def _get_pts(self, x, y, w, h, bx, by):
        return (self._quad(x, y, w - bx * 2, h - by * 2) +
                self._quad(x - w + bx, y, bx, h - by * 2) +
                self._quad(x + w - bx, y, bx, h - by * 2) +
                self._quad(x, y - h + by, w - bx * 2, by) +
                self._quad(x, y + h - by, w - bx * 2, by) +
                self._quad(x - w + bx, y - h + by, bx, by) +
                self._quad(x + w - bx, y + h - by, bx, by) +
                self._quad(x + w - bx, y - h + by, bx, by) +
                self._quad(x - w + bx, y + h - by, bx, by))

    def _quad(self, x, y, w, h):
        return (
            (x - w, y - h), (x + w, y - h), (x - w, y + h),
            (x - w, y + h), (x + w, y + h), (x + w, y - h)
        )

    def _update(self):
        w = self.width / 2
        h = self.height / 2
        b = self._border_size / 2
        self.vertex_list.points = self._get_pts(0, 0, w, h, b, b)
        self.vertex_list.uvs = self._get_pts(0.5, 0.5, 0.5, 0.5, b / w, b / h)

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        value = max(value, self._border_size)
        self._width = value
        self._update()

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        value = max(value, self._border_size)
        self._height = value
        self._update()


class VertexList(GameObject):
    def create(self, points, colours=None, uvs=None, texture=None):
        self.update_map = {
            "points": self.get_points,
            "depth": lambda: self.computed_depth,
            "colours": lambda: self._colours,
            "uvs": lambda: self._uvs
        }
        self.updates = set()

        self._points = points
        self._colours = colours
        self._texture = texture
        self._uvs = uvs

        self.target = self.tags.get_first(RenderContext < GameObject).window

        self.vertex_list = engine.VertexList(
            self.target,
            self._texture,
            self.computed_depth,
            self.get_points(),
            self.colours,
            self.uvs
        )

    @tgm_event
    def tgm_transform_changed(self):
        self.updates.add("points")

    def get_points(self):
        rtn = []

        for point in self.points:
            x, y, rot, x_scale, y_scale = self.transform.get_transform(
                transform=point + (0, 1, 1)
            )
            rtn.append((x, y))

        return rtn

    @tgm_event
    def tgm_depth_update(self):
        self.updates.add("depth")

    @tgm_event
    def tgm_draw(self):
        self.vertex_list.update(**{
            name: self.update_map[name]() for name in self.updates
        })

    @property
    def points(self):
        return self._points

    @points.setter
    def points(self, value):
        self._points = value
        self.updates.add("points")

    @property
    def uvs(self):
        return self._uvs

    @uvs.setter
    def uvs(self, value):
        self._uvs = value
        self.updates.add("uvs")

    @property
    def colours(self):
        return self._colours

    @colours.setter
    def colours(self, value):
        self._colours = value
        self.updates.add("colours")


class Text(GameObject):
    def create(self, text):
        self.text = text
        self.texture = engine.Text(text, (0, 0, 0, 255), 12)
        w = self.texture.width / 2
        h = self.texture.height / 2
        self.vertex_list = VertexList(
            self,
            points=(
                (-w, -h), (w, -h), (-w, h),
                (-w, h), (w, h), (w, -h)
            ),
            uvs=(
                (0, 0), (1, 0), (0, 1),
                (0, 1), (1, 1), (1, 0)
            ),
            texture=self.texture
        )
        # print(self.x)
        # self.vertex_list.updates.add("points")


