from tgm.system import EventGroup

sys_event = EventGroup(
    "update",
    "draw",
    "render",
    "update",
    "ancestor_update",
    "mouse_move",
    "mouse_press",
    "mouse_release",
    "get_collisions",
    "transform_changed"
)
