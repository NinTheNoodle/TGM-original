from tgm.system import Entity, common_ancestor
from math import sin, cos, atan2, sqrt, radians
from tgm.system import sys_event


class Transform(Entity):
    def create(self, x=0, y=0, rotation=0, x_scale=1, y_scale=1):
        self._x, self._y, self._rotation, self._x_scale, self._y_scale = (
            x, y, rotation, x_scale, y_scale
        )

    @property
    def transform(self):
        return self.x, self.y, self.rotation, self.x_scale, self.y_scale

    @transform.setter
    def transform(self, transform):
        self._x, self._y, self._rotation, self._x_scale, self._y_scale = (
            transform)
        self.send_update()

    @property
    def parent_transform(self):
        return self.get_parent_transform()

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value
        self.send_update()

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value
        self.send_update()

    @property
    def rotation(self):
        return self._rotation

    @rotation.setter
    def rotation(self, value):
        self._rotation = value
        self.send_update()

    @property
    def x_scale(self):
        return self._x_scale

    @x_scale.setter
    def x_scale(self, value):
        self._x_scale = value
        self.send_update()

    @property
    def y_scale(self):
        return self._y_scale

    @y_scale.setter
    def y_scale(self, value):
        self._y_scale = value
        self.send_update()

    def send_update(self):
        self.parent.tags.select(
            Entity[sys_event.transform_changed]
        ).transform_changed()

    # def relative_transform(self, other):
    #     ancestor = common_ancestor(self, other)
    #     x1, y1, r1, xs1, ys1 = self.get_transform(ancestor)
    #     x2, y2, r2, xs2, ys2 = other.get_transform(ancestor)
    #
    #     return x2 - x1, y2 - y1, r2 - r1, xs2 / xs1, ys2 / ys1

    def get_parent_transform(self, stop=None):
        try:
            return self.parent.parent.tags.get_first(
                Transform < Entity, stop
            )
        except (AttributeError, IndexError):
            return None

    def get_transform(self, stop=None, transform=None):
        if transform is None:
            transform = self.transform

        accumulated_transform = transform

        parent = self.get_parent_transform(stop)
        while parent is not None:
            accumulated_transform = parent.apply(*accumulated_transform)
            parent = parent.get_parent_transform(stop)

        return accumulated_transform

    def get_inverse_transform(self, transform, stop=None):
        accumulated_transform = transform

        parents = []

        parent = self.get_parent_transform(stop)
        while parent is not None:
            parents.append(parent)
            parent = parent.get_parent_transform(stop)

        for parent in reversed(parents):
            accumulated_transform = parent.apply_inverse(*accumulated_transform)

        return accumulated_transform

    def apply(self, x, y, rotation, x_scale, y_scale):
        return apply_transform(
                (x, y, rotation, x_scale, y_scale),
                self.transform
        )

    def apply_inverse(self, x, y, rotation, x_scale, y_scale):
        return apply_inverse_transform(
                (x, y, rotation, x_scale, y_scale),
                self.transform
        )


def apply_transform(original_transform, transformation):
    x, y, rotation, x_scale, y_scale = original_transform
    t_x, t_y, t_rotation, t_x_scale, t_y_scale = transformation

    rot = atan2(y, x) + radians(t_rotation)
    dist = sqrt(x * x + y * y)

    scale_rot = atan2(y_scale, x_scale) + radians(t_rotation)
    scale_dist = sqrt(x_scale * x_scale + y_scale * y_scale)

    x = t_x + cos(rot) * dist * t_x_scale
    y = t_y + sin(rot) * dist * t_y_scale
    x_scale = cos(scale_rot) * scale_dist * t_x_scale
    y_scale = sin(scale_rot) * scale_dist * t_y_scale
    rotation = (rotation + t_rotation) % 360

    return x, y, rotation, x_scale, y_scale


def apply_inverse_transform(original_transform, transformation):
    x, y, rotation, x_scale, y_scale = original_transform
    t_x, t_y, t_rotation, t_x_scale, t_y_scale = transformation

    x -= t_x
    y -= t_y

    rot = atan2(y, x) + radians(t_rotation)
    dist = sqrt(x * x + y * y)

    scale_rot = atan2(y_scale, x_scale) + radians(t_rotation)
    scale_dist = sqrt(x_scale * x_scale + y_scale * y_scale)

    x = (cos(rot) * dist) / t_x_scale
    y = (sin(rot) * dist) / t_y_scale
    x_scale = (cos(scale_rot) * scale_dist) / t_x_scale
    y_scale = (sin(scale_rot) * scale_dist) / t_y_scale
    rotation = (rotation - t_rotation) % 360

    return x, y, rotation, x_scale, y_scale
