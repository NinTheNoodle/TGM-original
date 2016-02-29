import json
from importlib import import_module

from tgm.system import GameObject


def load_prefab(target, file):
    if isinstance(file, str):
        with open(file) as fl:
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

            try:
                editor_obj = cls.editor
            except AttributeError:
                parsed_arguments = {}
            else:
                parsed_arguments = editor_obj.parse_arguments(
                    cls, file.name, arguments
                )

            if meta:
                parent = [current_target] + meta
            else:
                parent = current_target

            instance = cls(parent, **parsed_arguments)

            for name, value in attributes.items():
                setattr(instance, name, value)

            load(instance, children)

    load(target, data)


class Level(GameObject):
    def on_create(self, file=None):
        if file is not None:
            load_prefab(self, file)

    def button_pressed(self, text):
        print(text)
