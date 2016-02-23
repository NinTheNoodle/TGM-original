import tgm


class EditorObject(object):
    def __init__(self, **settings):
        self.settings = settings

    def parse_arguments(self, cls, file, arguments):
        args = {
            name: obj.load(cls, file, arguments.get(name))
            for name, obj in self.settings.items()
        }
        if "_x" in arguments:
            args["_x"] = arguments["_x"]
        if "_y" in arguments:
            args["_y"] = arguments["_y"]
        if "_rotation" in arguments:
            args["_rotation"] = arguments["_rotation"]
        if "_x_scale" in arguments:
            args["_x_scale"] = arguments["_x_scale"]
        if "_y_scale" in arguments:
            args["_y_scale"] = arguments["_y_scale"]
        if "_depth" in arguments:
            args["_depth"] = arguments["_depth"]

        return args


class Setting(object):
    def __init__(self, default):
        self.default = default


class TextSetting(Setting):
    def instantiate(self):
        pass

    def load(self, cls, file, value):
        if value is None:
            return self.default
        return str(value)


class FileSetting(Setting):
    def load(self, cls, file, value):
        if value is None:
            return self.default
        return str(value)


class FunctionSetting(Setting):
    def load(self, cls, file, value):
        if value is None:
            return self.default
        code = compile(value, file, "eval")
        return lambda obj: eval(code, {"cls": cls, "self": obj, "tgm": tgm})
