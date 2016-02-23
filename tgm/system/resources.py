import os
import sys
import pkgutil

from tgm.system import GameObject

modules = {}
files = {}
hidden_files = {}


def register(package):
    paths = sys.modules[package].__path__

    for path in paths:
        for fname in os.listdir(path):
            fpath = os.path.join(path, fname)
            if fname.startswith("_"):
                hidden_files.setdefault(package, set()).add(fpath)
                continue
            if os.path.isfile(fpath):
                files.setdefault(package, set()).add(fpath)

    for loader, name, is_package in pkgutil.iter_modules(paths):
        if name.startswith("_"):
            continue
        module = loader.find_module(name).load_module(name)
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
