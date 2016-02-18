from tgm.system import EventGroup

tgm_event = EventGroup(
    "tgm",
    control=[
        "update",
        "update_init",
        "ancestor_update",
        "transform_changed"
    ],
    draw=[
        "draw",
        "render"
    ],
    collision=[
        "get_collisions"
    ],
    input=[
        "mouse_move",
        "mouse_press",
        "mouse_release"
    ]
)
