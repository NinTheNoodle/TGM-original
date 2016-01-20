from tgm.common import GameObject, common_ancestor
from math import sin, cos, atan2, sqrt, radians


class Transform(GameObject):
    def create(self, x=0, y=0, rotation=0, scale=1):
        self.x = x
        self.y = y
        self.rotation = rotation
        self.scale = scale

    @property
    def transform(self):
        return self.x, self.y, self.rotation, self.scale

    @property
    def parent_transform(self):
        return self.get_parent_transform()

    @transform.setter
    def transform(self, transform):
        self.x, self.y, self.rotation, self.scale = transform

    def relative_transform(self, other):
        ancestor = common_ancestor(self, other)
        x1, y1, r1, s1 = self.get_transform(ancestor)
        x2, y2, r2, s2 = other.get_transform(ancestor)

        return x2 - x1, y2 - y1, r2 - r1, s2 / s1

    def get_parent_transform(self, stop=None):
        try:
            return self.parent.parent.tags.get_first(
                    Transform < GameObject, stop
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

    def apply(self, x, y, rotation, scale):
        return self.apply_transform(
                (x, y, rotation, scale),
                self.transform
        )

    def apply_inverse(self, x, y, rotation, scale):
        return self.apply_inverse_transform(
                (x, y, rotation, scale),
                self.transform
        )

    def get_pos(self):
        return self.get_transform()[:2]

    @staticmethod
    def apply_transform(original_transform, transformation):
        x, y, rotation, scale = original_transform
        t_x, t_y, t_rotation, t_scale = transformation

        rot = atan2(y, x) + radians(t_rotation)
        dist = sqrt(x * x + y * y) * t_scale

        x = t_x + sin(rot) * dist
        y = t_y + cos(rot) * dist
        rotation += t_rotation
        scale *= t_scale

        return x, y, rotation, scale

    @staticmethod
    def apply_inverse_transform(original_transform, transformation):
        x, y, rotation, scale = original_transform
        t_x, t_y, t_rotation, t_scale = transformation

        x -= t_x
        y -= t_y

        rot = atan2(y, x) + radians(t_rotation)
        dist = sqrt(x * x + y * y) / t_scale

        x = sin(rot) * dist
        y = cos(rot) * dist
        rotation -= t_rotation
        scale /= t_scale

        return x, y, rotation, scale
