from tgm.common import GameObject, EventGroup, sys_tags
from math import sin, cos, atan2, sqrt, radians


transform_event = EventGroup("get_transform")


class Transform(GameObject):
    def create(self, x=0, y=0, rotation=0, scale=1):
        self.x = x
        self.y = y
        self.rotation = rotation
        self.scale = scale

    @transform_event
    def get_transform(self):
        try:
            transform = self.parent.parent.tags.get_first(
                    Transform < GameObject
            )
        except (AttributeError, StopIteration):
            return self.x, self.y, self.rotation, self.scale

        px, py, pr, ps = transform.get_transform()
        rot = atan2(self.y, self.x)
        dist = sqrt(self.x * self.x + self.y * self.y)

        x = px + sin(rot + radians(pr)) * dist * ps
        y = py + cos(rot + radians(pr)) * dist * ps
        rotation = self.rotation + pr
        scale = self.scale * ps

        return x, y, rotation, scale

    def get_pos(self):
        return self.get_transform()[:2]
