import pyglet


loaded_images = {}
mouse_pos = {}


def get_window(width, height):
    window = pyglet.window.Window(width, height)

    @window.event
    def on_mouse_press(x, y, button, modifiers):
        pass

    return window


def mouse_move_event(window, func):
    @window.event
    def on_mouse_motion(x, y, dx, dy):
        func(x, y)

    @window.event
    def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
        func(x, y)


def mouse_press_event(window, func):
    @window.event
    def on_mouse_press(x, y, button, modifiers):
        func({
            pyglet.window.mouse.LEFT: "L",
            pyglet.window.mouse.MIDDLE: "M",
            pyglet.window.mouse.RIGHT: "R"
        }[button])


def mouse_release_event(window, func):
    @window.event
    def on_mouse_release(x, y, button, modifiers):
        func({
            pyglet.window.mouse.LEFT: "L",
            pyglet.window.mouse.MIDDLE: "M",
            pyglet.window.mouse.RIGHT: "R"
        }[button])


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
