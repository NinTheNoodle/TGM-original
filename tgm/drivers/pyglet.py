import pyglet
from pyglet import gl
import os.path


class App(object):
    def __init__(self):
        pass

    def run(self):
        pyglet.app.run()


class TextureGroup(pyglet.graphics.Group):
    def set_state(self):
        gl.glEnable(gl.GL_TEXTURE_2D)

    def unset_state(self):
        gl.glDisable(gl.GL_TEXTURE_2D)

    def __eq__(self, other):
        return self.__class__ == other.__class__

    def __hash__(self):
        return hash(self.__class__)


class RenderGroup(pyglet.graphics.Group):
    def __init__(self, depth, texture=None):
        self.depth = depth
        if texture is not None:
            self.texture = texture.texture
            super(RenderGroup, self).__init__(parent=TextureGroup())
        else:
            self.texture = None
            super(RenderGroup, self).__init__()

    def set_state(self):
        if self.texture is not None:
            gl.glBindTexture(self.texture.target, self.texture.id)

    def __lt__(self, other):
        if self.__class__ == other.__class__:
            try:
                return self.depth > other.depth
            except TypeError:
                pass
        return super(RenderGroup, self).__lt__(other)

    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False

        return self.depth == other.depth and self.texture == other.texture

    def __hash__(self):
        data = (self.__class__, self.depth)
        if self.texture is not None:
            data = data + (self.texture.id, self.texture.target)
        return hash(data)


class Texture(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.vertex_lists = []

        self.batch = pyglet.graphics.Batch()
        self.texture = pyglet.image.Texture.create(
            width, height, internalformat=gl.GL_RGBA
        )

        buffers = pyglet.image.get_buffer_manager()
        self.col_buffer = buffers.get_color_buffer()

    def update_visibility(self, frame):
        for vertex_list in self.vertex_lists:
            vertex_list.update_visibility(frame)

    def redraw(self):
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()

        gl.gluOrtho2D(
            0,
            self.width,
            0,
            self.height
        )

        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()

        gl.glBindFramebufferEXT(gl.GL_DRAW_FRAMEBUFFER_EXT,
                                self.col_buffer.gl_buffer)

        gl.glFramebufferTexture2DEXT(
            gl.GL_DRAW_FRAMEBUFFER_EXT,
            gl.GL_COLOR_ATTACHMENT0_EXT,
            self.texture.target, self.texture.id, 0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)

        self.batch.draw()

        gl.glBindFramebufferEXT(gl.GL_DRAW_FRAMEBUFFER_EXT, 0)

    def add(self, vertex_list):
        self.vertex_lists.append(vertex_list)

        data = []

        if vertex_list.points is not None:
            data.append("v2f")

        if vertex_list.uvs is not None:
            data.append(("t2f", flatten(vertex_list.uvs)))

        if vertex_list.colours is not None:
            data.append(("c3f", flatten(vertex_list.colours)))

        return self.batch.add(
            len(vertex_list.points),
            vertex_list.mode,
            RenderGroup(vertex_list.depth, vertex_list.texture),
            *data
        )

    def get_vertex_list(self, x, y):
        return pyglet.graphics.vertex_list(
            6,
            ("t2f", flatten(texture_uvs(self.texture))),
            ("v2f", flatten(quad(x, y, self.width, self.height)))
        )


class Window(Texture):
    def __init__(self, width, height):
        super(Window, self).__init__(width, height)
        self.window = pyglet.window.Window(width, height)
        self.mouse_buttons = set()
        self.mouse_pos = (0, 0)
        self.frame = 0

        self.vertex_list = self.get_vertex_list(0, 0)

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
            gl.glEnable(gl.GL_BLEND)
            gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
            gl.glMatrixMode(gl.GL_PROJECTION)
            gl.glLoadIdentity()
            gl.gluOrtho2D(
                0,
                self.width,
                0,
                self.height
            )

            gl.glMatrixMode(gl.GL_MODELVIEW)

            gl.glLoadIdentity()
            gl.glEnable(gl.GL_TEXTURE_2D)
            gl.glBindTexture(self.texture.target, self.texture.id)
            self.vertex_list.draw(gl.GL_TRIANGLES)
            gl.glDisable(gl.GL_TEXTURE_2D)

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
        self.update_visibility(self.frame)
        self.redraw()


class Image(object):
    loaded_images = {}

    def __init__(self, path):
        path = os.path.normpath(os.path.normcase(path))

        if path not in self.loaded_images:
            self.loaded_images[path] = pyglet.image.load(path)

        self.path = path
        self.image = self.loaded_images[path]

        self.texture = self.image.get_texture()
        self.width = self.image.width
        self.height = self.image.height


class VertexList(object):
    def __init__(self, target, texture, depth, points, colours, uvs):
        self.target = target
        self.texture = texture
        self.depth = depth

        if texture is not None:
            width = texture.texture.width
            height = texture.texture.height
            x_scale = width / next_power(width)
            y_scale = height / next_power(height)

            uvs = tuple(
                (x * x_scale, y * y_scale)
                for x, y in uvs
            )

        self._colours = colours
        self._uvs = uvs
        self._points = points
        self._visible = True

        self.mode = gl.GL_TRIANGLES
        self.last_updated = -1
        self.frame = -1

        self.vertex_list = target.add(self)

    @classmethod
    def new_quad(cls, target, texture, depth, x, y, width, height):
        if texture is not None:
            uvs = texture_uvs(texture)
        else:
            uvs = None
        return cls(target, texture, depth,
                   quad(x, y, width, height),
                   None, uvs)

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


def quad(x, y, width, height):
    return (
        (x, y), (x + width, y), (x, y + height),
        (x, y + height), (x + width, y), (x + width, y + height)
    )


def next_power(x):
    return 1 << (x - 1).bit_length()


def texture_uvs(texture):
    tex_w, tex_h = texture.tex_coords[6:8]
    return quad(0, 0, tex_w, tex_h)
