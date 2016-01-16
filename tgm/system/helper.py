def common_ancestor(obj1, obj2):
    """
    Returns the common ancestor of two game objects.
    Returns None if the objects don't share an ancestor.
    If one object is the direct ancestor of the other, it will be returned.
    """
    obj2_branch = set()
    obj = obj2

    while obj is not None:
        obj2_branch.add(obj)
        obj = obj.parent

    obj = obj1

    while obj is not None:
        if obj in obj2_branch:
            return obj
        obj = obj.parent

    return None
