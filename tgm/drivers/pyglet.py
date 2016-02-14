import pyglet
from pyglet.gl import *


class App(object):
    def __init__(self):
        pass

    def run(self):
        pyglet.app.run()


class Window(object):
    def __init__(self, texture):
        self.texture = texture
        self.window = pyglet.window.Window(texture.width, texture.height)
        self.mouse_buttons = set()
        self.mouse_pos = (0, 0)
        self.frame = 0

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        def mouse_button(button):
            return {
                pyglet.window.mouse.LEFT: "L",
                pyglet.window.mouse.MIDDLE: "M",
                pyglet.window.mouse.RIGHT: "R"
            }[button]

        @self.window.event
        def on_mouse_press(x, y, button, modifiers):
            self.mouse_buttons.add(mouse_button(button))
            self.mouse_pos = x, y

        @self.window.event
        def on_mouse_release(x, y, button, modifiers):
            try:
                self.mouse_buttons.remove(mouse_button(button))
            except KeyError:
                pass
            self.mouse_pos = x, y

        @self.window.event
        def on_mouse_motion(x, y, dx, dy):
            self.mouse_pos = x, y

        @self.window.event
        def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
            self.mouse_pos = x, y

        @self.window.event
        def on_draw():
            self.window.clear()
            self.texture.texture.blit(0, 0)

    def get_mouse_buttons(self):
        return self.mouse_buttons.copy()

    def get_mouse_pos(self):
        return self.mouse_pos

    def get_keyboard_buttons(self):
        pass

    def schedule(self, callback, frequency):
        pyglet.clock.schedule_interval(callback, frequency)

    def update(self):
        self.frame += 1
        self.texture.update_visibility(self.frame)
        self.texture.redraw()


class Texture(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.vertex_lists = []

        self.batch = pyglet.graphics.Batch()
        self.texture = pyglet.image.Texture.create(
            width, height, internalformat=GL_RGBA)

        buffers = pyglet.image.get_buffer_manager()
        self.col_buffer = buffers.get_color_buffer()

    def update_visibility(self, frame):
        for vertex_list in self.vertex_lists:
            vertex_list.update_visibility(frame)

    def redraw(self):
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glMatrixMode(GL_PROJECTION)

        glLoadIdentity()
        gluOrtho2D(
            0,
            self.width,
            0,
            self.height)

        glMatrixMode(GL_MODELVIEW)

        glLoadIdentity()

        glBindFramebufferEXT(GL_DRAW_FRAMEBUFFER_EXT, self.col_buffer.gl_buffer)

        glFramebufferTexture2DEXT(
            GL_DRAW_FRAMEBUFFER_EXT,
            GL_COLOR_ATTACHMENT0_EXT,
            self.texture.target, self.texture.id, 0)
        glClear(GL_COLOR_BUFFER_BIT)

        self.batch.draw()

        glBindFramebufferEXT(GL_DRAW_FRAMEBUFFER_EXT, 0)

    def add(self, vertex_list):
        self.vertex_lists.append(vertex_list)

        data = []

        if vertex_list.points is not None:
            data.append(("v2f", (0, 0) * len(vertex_list.points)))

        if vertex_list.uvs is not None:
            data.append(("t2f", flatten(vertex_list.uvs)))

        if vertex_list.colours is not None:
            data.append(("c3f", flatten(vertex_list.colours)))

        return self.batch.add(
            len(vertex_list.points),
            vertex_list.mode,
            None,
            *data
        )


class Image(object):
    def __init__(self, target, path):
        self.path = path


class VertexList(object):
    def __init__(self, target, texture, depth, points, colours, uvs):
        self.target = target
        self.texture = texture
        self.depth = depth

        self._colours = colours
        self._uvs = uvs
        self._points = points
        self._visible = True

        self.mode = GL_TRIANGLES
        self.last_updated = 0
        self.frame = 0

        self.vertex_list = target.add(self)

    @property
    def points(self):
        return self._points

    @points.setter
    def points(self, value):
        if self._points != value:
            self._points = value
            if self.visible:
                self.vertex_list.vertices = flatten(value)

    @property
    def colours(self):
        return self._colours

    @colours.setter
    def colours(self, value):
        if self._colours != value:
            self._colours = value
            self.vertex_list.colors = flatten(value)

    @property
    def uvs(self):
        return self._uvs

    @uvs.setter
    def uvs(self, value):
        if self._uvs != value:
            self._uvs = value
            self.vertex_list.uvs = flatten(value)

    @property
    def visible(self):
        return self._visible

    @visible.setter
    def visible(self, value):
        if self._visible != value:
            self._visible = value
            if value:
                self.vertex_list.vertices = flatten(self.points)
            else:
                self.vertex_list.vertices = (0, 0) * len(self.points)

    def update_visibility(self, frame):
        if self.last_updated == self.frame:
            if not self.visible:
                self.visible = True
        else:
            if self.visible:
                self.visible = False
        self.frame = frame

    def update(self):
        self.last_updated = self.frame


def flatten(iterator):
    return tuple(
        subelement
        for element in iterator
        for subelement in element
    )
