import pyglet


loaded_images = {}


def get_window():
    return pyglet.window.Window()


def render_loop(window, func):
    window.event(func)


def get_image(path):
    if path not in loaded_images:
        loaded_images[path] = pyglet.image.load(path)
    return loaded_images[path]


def get_sprite(image):
    return pyglet.sprite.Sprite(image)


def draw_sprite(sprite, x, y, rotation, scale):
    sprite._x = x
    sprite._y = y
    sprite._rotation = rotation
    sprite._scale = scale
    sprite._update_position()
    sprite.draw()


def tick(func, fps):
    pyglet.clock.schedule_interval(lambda dt: func(), 1/fps)


def init_audio():
    pass


def init_renderer():
    pass


def init_controller():
    pass


def run():
    pyglet.app.run()
