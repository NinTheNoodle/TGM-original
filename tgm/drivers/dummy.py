class App(object):
    def __init__(self):
        pass

    def run(self):
        pass


class Texture(object):
    def __init__(self, width, height, texture=None):
        self.width = width
        self.height = height
        self.texture = texture

    def resize(self, width, height, redraw=True):
        self.width = width
        self.height = height

    def clear(self):
        pass

    def paint(self, func):
        func()

    def draw(self, x, y, width=None, height=None):
        pass


class Context(Texture):
    def __init__(self, width, height):
        super(Context, self).__init__(width, height)

    def update_visibility(self, frame):
        pass

    def redraw(self):
        pass

    def add(self, vertex_list):
        pass

    def migrate(self, vertex_list):
        pass

    def update(self):
        pass


class Window(Context):
    def __init__(self, width, height):
        super(Window, self).__init__(width, height)
        pass

    def get_mouse_buttons(self):
        return set()

    def get_mouse_pos(self):
        return 0, 0

    def get_keyboard_buttons(self):
        pass

    def schedule(self, callback, frequency):
        raise NotImplementedError("Cannot schedule on dummy driver")


class Image(Texture):
    loaded_images = {}

    def __init__(self, path):
        super(Image, self).__init__(0, 0)


class VertexList(object):
    def __init__(self, target, texture, depth, points, colours, uvs):
        self.target = target
        self.texture = texture
        self.depth = depth

        self.mode = None
        self.last_updated = -1
        self.frame = -1
        self.points = points
        self.colours = colours
        self.uvs = uvs
        self.visible = True

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

    def update_visibility(self, frame):
        pass

    def update(self, points=None, uvs=None, colours=None, depth=None):
        pass


class Text(Texture):
    def __init__(self, text, colour, size):
        self.text = text

        super(Text, self).__init__(0, 0)


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
