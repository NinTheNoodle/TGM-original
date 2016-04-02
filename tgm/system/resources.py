import os
import sys
import pkgutil
from importlib import import_module

from tgm.system import GameObject

modules = {}
files = {}
hidden_files = {}


def register(package):
    paths = sys.modules[package].__path__

    # Load every file in the package
    for path in paths:
        for fname in os.listdir(path):
            fpath = os.path.join(path, fname)
            if fname.startswith("_"):
                hidden_files.setdefault(package, set()).add(fpath)
                continue
            if os.path.isfile(fpath):
                files.setdefault(package, set()).add(fpath)

    # Load every module in the package
    for loader, name, is_package in pkgutil.iter_modules(paths):
        if name.startswith("_"):
            if name == "__init__":
                continue
            if not (name.startswith("__") and name.endswith("__")):
                continue
        module = loader.find_module(name).load_module(name)
        # Register sub-packages
        if is_package:
            register(module.__package__)

        modules.setdefault(package, set()).add(module)


def get_modules(package=None):
    if package is None:
        return set.union(*modules.values())
    return modules[package]


def get_files(package=None):
    if package is None:
        return set.union(*files.values())
    return files[package]


def get_hidden_files(package=None):
    if package is None:
        return set.union(*hidden_files.values())
    return hidden_files[package]


def get_entity_classes():
    return set(iter_subclasses(GameObject))


def parse_path(path):
    path = os.path.normpath(path)

    path_segments = path.split(os.path.sep)
    if "." in path_segments[0] and path_segments[0] not in [".", ".."]:
        module = import_module(path_segments[0])
        path_segments[0] = os.path.dirname(module.__file__)
        path = os.path.join(*path_segments)

    return path


# https://code.activestate.com/recipes
# /576949-find-all-subclasses-of-a-given-class/
def iter_subclasses(cls, _seen=None):
    if _seen is None:
        _seen = set()
    try:
        subs = cls.__subclasses__()
    except TypeError:
        # fails only when cls is type
        subs = cls.__subclasses__(cls)

    for sub in subs:
        if sub not in _seen:
            _seen.add(sub)
            yield sub
            for sub in iter_subclasses(sub, _seen):
                yield sub
