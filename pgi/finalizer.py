from weakref import proxy


class _BaseFinalizer(object):

    # Set used to keep the proxy around.
    # Deletion automatically removes proxies from the set.
    _objects = set()

    @classmethod
    def track(cls, obj, ptr):
        """
        Track an object which needs destruction when it is garbage collected.
        """
        cls._objects.add(cls(obj, ptr))

    def __init__(self, obj, ptr):
        self.obj = proxy(obj, self.delete)
        self.ptr = ptr

    def delete(self, deadweakproxy):
        type(self)._objects.remove(self)
        self.destructor(deadweakproxy, self.ptr)
