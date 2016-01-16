from tgm.common import GameObject, TagAttribute, EventGroup, sys_tags
from math import sin, cos, atan2, sqrt, radians


transform_event = EventGroup("get_transform")


class Transform(GameObject):
    x = TagAttribute(default=0)
    y = TagAttribute(default=0)
    rotation = TagAttribute(default=0)
    scale = TagAttribute(default=1)

    @transform_event
    def get_transform(self):
        try:
            parent_transform = self.parent.parent.tags.get(Transform())
        except (AttributeError, IndexError):
            return self.x, self.y, self.rotation, self.scale

        px, py, pr, ps = parent_transform.transform.get_transform()
        rot = atan2(self.y, self.x)
        dist = sqrt(self.x * self.x + self.y * self.y)

        x = px + sin(rot + radians(pr)) * dist * ps
        y = py + cos(rot + radians(pr)) * dist * ps
        rotation = self.rotation + pr
        scale = self.scale * ps

        return x, y, rotation, scale

    def get_pos(self):
        return self.get_transform()[:2]
