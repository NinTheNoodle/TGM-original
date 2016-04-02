import json
from importlib import import_module

from tgm.system import GameObject, parse_path
import tgm


def parse_code(cls, code, argument_name, path):
    try:
        return eval(compile(code, path, "eval"),
                    {"cls": cls, "tgm": tgm})
    except Exception as e:
        context = "\n<class> {}\n<code> {}\n<argument> '{}'".format(
            cls, code, argument_name
        )
        e.args = (e.args[0] + context,) + e.args[1:]
        raise e


def parse_argument(cls, data, argument_name, path):
    if isinstance(data, str):
        if data.startswith("`") and data.endswith("`"):
            return parse_code(cls, data[1:-1], argument_name, path)
    return data


def load_prefab(target, file):
    if isinstance(file, str):
        with open(parse_path(file)) as fl:
            return load_prefab(target, fl)
    data = json.load(file)

    def load(current_target, instances):
        for instance_data in instances:
            module_name, class_name = instance_data["class"].rsplit(".", 1)
            arguments = instance_data.get("arguments", {})
            attributes = instance_data.get("attributes", {})
            children = instance_data.get("children", [])
            meta = instance_data.get("meta", [])

            module = import_module(module_name)
            cls = getattr(module, class_name)

            parsed_arguments = {
                name: parse_argument(cls, arg, name, file)
                for name, arg in arguments.items()
            }

            if meta:
                parent = [current_target] + meta
            else:
                parent = current_target

            instance = cls(parent, **parsed_arguments)

            for name, value in attributes.items():
                setattr(instance, name, parse_argument(cls, value, name, file))

            load(instance, children)

    load(target, data)


class Level(GameObject):
    def on_create(self, file=None):
        if file is not None:
            load_prefab(self, file)
