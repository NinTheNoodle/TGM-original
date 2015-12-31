class Feature(object):
    pass


class TagAttribute(Feature):
    def __init__(self):
        self.data = {}

    def __get__(self, instance, owner):
        return self.data[instance]

    def init(self, instance):
        instance.tags.tags.add(instance)

    def __set__(self, instance, value):
        if instance in self.data:
            instance.tags.index.remove((self, self.data[instance]))

        self.data[instance] = value
        instance.tags.index.add((self, value))


class EventGroup(object):
    def __init__(self, *events):
        self._events = frozenset(events)

    def __call__(self, func):
        func_name = func.__name__

        if func_name not in self._events:
            raise AttributeError("event '{}' is not defined".format(func_name))

        return EventMethod(func, self)

    def __getattr__(self, event):
        return EventTag(event, self)


class EventMethod(Feature):
    """
    Substitute for a normal Python method
    automatically tags its own existence
    """
    def __init__(self, function, group):
        self.function = function
        self.group = group

    def init(self, instance):
        self.instance = instance
        EventTag(parent=instance, name=self.function.__name__, group=self.group)

    def __call__(self, *args, **kwargs):
        self.function(self.instance, *args, **kwargs)


class Parent(Feature):
    def __init__(self):
        self.parents = {}

    def __get__(self, instance, owner):
        try:
            return self.parents[instance]
        except KeyError:
            raise AttributeError("'{}' object has no parent set".format(
                owner.__name__
            ))

    def destroy(self, instance):
        self.parents[instance].children.remove(instance)

    def __set__(self, instance, parent):
        if self.parents.get(instance, None) is not None:
            self.parents[instance].children.remove(instance)

        self.parents[instance] = parent

        if parent is not None:
            parent.children.add(instance)


class TagStore(object):
    def __init__(self, owner):
        self.owner = owner
        self.tags = set()
        self.child_tags = {}
        self.index = set()

    def register_tag(self, tag, child=None):
        found = False
        if child is None:
            if tag in self.tags:
                found = True
            else:
                self.tags.add(tag)
        else:
            if tag in self.child_tags:
                found = True
            else:
                self.child_tags[tag] = child

        if not found and self.owner.parent is not None:
            self.owner.parent.tags.register_tag(tag, self.owner)

    def signal(self, event):
        pass

    def event(self, event):
        print(event)

    def select(self, query):
        test = self.owner
        rtn = set()

        for tag_object in test.tags:
            if tag_object.tags.index >= query.tags.index:
                rtn.add(test)
                break

        return rtn

    def _select(self, query):
        test = self.owner
        rtn = set()

        for tag_object in test.tags:
            if tag_object.tags >= query.tags:
                rtn.add(test)
                break

        for child in test.children:
            pass

        return rtn


class GameObject(object):
    parent = Parent()

    def __init__(self, *args, **kwargs):
        self.children = set()
        self.tags = TagStore(self)
        self.features = []

        set_features = {}

        class_dict = {}
        for cls in reversed(self.__class__.mro()):
            class_dict.update(cls.__dict__)

        for name, value in class_dict.items():
            if isinstance(value, Feature):
                self.features.append(value)
                if name in kwargs:
                    set_features[name] = kwargs.pop(name)

        self.init_args = args
        self.init_kwargs = kwargs

        for feature in self.features:
            if hasattr(feature, "init"):
                feature.init(self)

        for name, value in set_features.items():
            setattr(self, name, value)

        if hasattr(self, "init"):
            self.init(*args, **kwargs)

    def destroy(self):
        for feature in self.features:
            if hasattr(feature, "destroy"):
                feature.destroy(self)


class EventTag(GameObject):
    name = TagAttribute()
    group = TagAttribute()


# class TagStore(object):
#     def __init__(self, owner):
#         self._tags = set()
#         self._child_tags = {}
#         self.owner = owner
#
#     def select(self, query):
#         return Selection(query, self)
#
#     def event(self, event, *args, **kwargs):
#         rtn = []
#         for result in self.select(event):
#             rtn.append(getattr(result, event.name)(*args, **kwargs))
#         return rtn
#
#     def register_tag(self, tag, child=None):
#         if child is None:
#             self._tags.add(tag)
#         else:
#             children = self._child_tags.setdefault(tag, set())
#             if child in children:
#                 return
#             children.add(child)
#
#         parent = self.owner.parent
#         if parent is not None:
#             parent.tags.register_tag(tag, self.owner)
#
#     def unregister_tag(self, tag, child=None):
#         if child is None:
#             self._tags.remove(tag)
#         else:
#             self._child_tags[tag].remove(child)
#             if not self._child_tags[tag]:
#                 del self._child_tags[tag]
#
#         if tag not in self._tags and tag not in self._child_tags:
#             parent = self.owner.parent
#             if parent is not None:
#                 parent.tags.unregister_tag(tag, self.owner)
#
#     def __iter__(self):
#         yield from self._tags
#
#     def __contains__(self, item):
#         from tgm.system.tag import TagGroup
#         operators = {
#             "and": operator.and_,
#             "or": operator.or_,
#             "less": lambda x, y: x and not y
#         }
#
#         if isinstance(item, TagGroup):
#             return operators[item.operation](
#                 item.tag1 in self,
#                 item.tag2 in self
#             )
#         else:
#             return item in self._tags
#
#     def _children_containing(self, query):
#         from tgm.system.tag import TagGroup
#
#         operators = {
#             "and": set.intersection,
#             "or": set.union
#         }
#
#         if isinstance(query, TagGroup):
#             operation = query.operation
#
#             if query.operation == "less":
#                 return self._children_containing(query.tag1)
#
#             return operators[operation](
#                 self._children_containing(query.tag1),
#                 self._children_containing(query.tag2)
#             )
#         else:
#             return self._child_tags.get(query, set())
#
#     def __repr__(self):
#         return "Tags({})".format(", ".join(repr(x) for x in self))
#
#
# class Selection(object):
#     def __init__(self, query, tag_store):
#         self.query = query
#         self.tag_store = tag_store
#         self._contents = None
#
#     def _resolve(self):
#         found = set()
#
#         for child in self.tag_store._children_containing(self.query):
#             found.update(child.tags.select(self.query))
#
#         if self.query in self.tag_store:
#             found.add(self.tag_store.owner)
#
#         self._contents = found
#
#     def select(self, query):
#         return Selection(self.query & query, self.tag_store)
#
#     def event(self, event, *args, **kwargs):
#         rtn = []
#         for result in self.select(event):
#             rtn.append(getattr(result, event.name)(*args, **kwargs))
#         return rtn
#
#     def sorted(self, breath=False):
#         if breath:
#             return sorted(self, key=lambda x: len(x.tree_position))
#
#         return sorted(self, key=lambda x: x.tree_position)
#
#     def __iter__(self):
#         if self._contents is None:
#             self._resolve()
#         yield from self._contents
#
#     def __repr__(self):
#         return "Selection({})".format(", ".join(repr(x) for x in self))
