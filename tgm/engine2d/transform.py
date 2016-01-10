from tgm.common import GameObject, TagAttribute, EventGroup, sys_tags


transform_event = EventGroup("get_pos")


class Transform(GameObject):
    x = TagAttribute(default=0)
    y = TagAttribute(default=0)

    @transform_event
    def get_pos(self):
        try:
            parent_transform = self.parent.parent.tags.get(Transform())
        except (AttributeError, IndexError):
            return self.x, self.y

        pos = parent_transform.transform.get_pos()
        return self.x + pos[0], self.y + pos[1]
