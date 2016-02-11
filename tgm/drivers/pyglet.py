import pyglet
from copy import deepcopy


loaded_images = {}
mouse_state = {}
batches = {}
frame = 0


def get_window(width, height):
    window = pyglet.window.Window(width, height)

    mouse_state[window] = {
        "pos": (0, 0),
        "buttons": set()
    }

    def mouse_button(button):
        return {
            pyglet.window.mouse.LEFT: "L",
            pyglet.window.mouse.MIDDLE: "M",
            pyglet.window.mouse.RIGHT: "R"
        }[button]

    @window.event
    def on_mouse_press(x, y, button, modifiers):
        mouse_state[window]["buttons"].add(mouse_button(button))
        mouse_state[window]["pos"] = x, y

    @window.event
    def on_mouse_release(x, y, button, modifiers):
        try:
            mouse_state[window]["buttons"].remove(mouse_button(button))
        except KeyError:
            pass
        mouse_state[window]["pos"] = x, y

    @window.event
    def on_mouse_motion(x, y, dx, dy):
        mouse_state[window]["pos"] = x, y

    @window.event
    def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
        mouse_state[window]["pos"] = x, y

    return window


def new_batch():
    return pyglet.graphics.Batch()


def draw_batch(batch):
    for vertex_list, updated_frame in batches[batch].items():
        if updated_frame == frame:
            if not vertex_list.enabled:
                vertex_list.vertices = vertex_list.enabled_vertices
                vertex_list.enabled = True
        else:
            if vertex_list.enabled:
                vertex_list.vertices = vertex_list.disabled_vertices
                vertex_list.enabled = False
    #print(batches[batch].values())
    batch.draw()


def add_vertex_list(batch, points, colours):
    points = tuple(coordinate
                   for point in points
                   for coordinate in point)
    colours = tuple(channel
                    for colour in colours
                    for channel in colour)

    vertex_list = batch.add(
        len(points) // 2,
        pyglet.gl.GL_TRIANGLES,
        None,
        ('v2f', points),
        ('c3f', colours)
    )
    vertex_list.disabled_vertices = (0, 0) * vertex_list.get_size()
    vertex_list.enabled_vertices = vertex_list.vertices
    vertex_list.enabled = True

    batches.setdefault(batch, {})[vertex_list] = frame
    return vertex_list


def next_frame():
    global frame
    frame += 1


def vertex_list_tick(batch, vertex_list):
    batches[batch][vertex_list] = frame


def modify_vertex_list(vertex_list, points=None, colours=None):
    if points is not None:
        points = tuple(coordinate
                       for point in points
                       for coordinate in point)

        vertex_list.vertices = points

    if colours is not None:
        colours = tuple(channel
                        for colour in colours
                        for channel in colour)

        vertex_list.colors = colours


def get_mouse_state(window):
    return deepcopy(mouse_state[window])


def render_loop(window, func):
    @window.event
    def on_draw():
        window.clear()
        func()


def get_image(path):
    if path not in loaded_images:
        image = pyglet.image.load(path)
        image.anchor_x = image.width // 2
        image.anchor_y = image.height // 2
        loaded_images[path] = image
    return loaded_images[path]


def get_sprite(image):
    return pyglet.sprite.Sprite(image)


def draw_sprite(sprite, x, y, rotation, scale):
    sprite._x = round(x)
    sprite._y = round(y)
    sprite._rotation = -rotation
    sprite._scale = scale
    sprite._update_position()
    sprite.draw()


def tick(func, fps):
    pyglet.clock.schedule_interval(lambda dt: func(), 1/fps)


def init_audio():
    pass


def init_renderer():
    pass


def run():
    pyglet.app.run()
