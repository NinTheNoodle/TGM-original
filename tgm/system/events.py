from tgm.system import EventGroup

tgm_event = EventGroup("tgm", [
    "update",
    "draw",
    "render",
    "update_init",
    "update",
    "ancestor_update",
    "mouse_move",
    "mouse_press",
    "mouse_release",
    "get_collisions",
    "transform_changed"
])
