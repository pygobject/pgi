from ctypes import (
    Structure, POINTER,
    byref, c_bool, c_double, c_uint, c_void_p)
from weakref import WeakSet, proxy

from pgi.codegen.ctypes_backend import CTypesBackend
from pgi.overrides import override, get_introspection_module

Poppler = get_introspection_module('Poppler')

backend = CTypesBackend()
lib = backend.get_library("Poppler")

g_free = lib.g_free

poppler_page_get_text_layout = lib.poppler_page_get_text_layout
poppler_page_get_text_layout.argtypes = [
    c_void_p, POINTER(c_void_p), POINTER(c_uint)]
poppler_page_get_text_layout.restype = c_bool

Rectangle = Poppler.Rectangle

__all__ = []


class _Finalizer(object):
    _objects = set()

    @classmethod
    def new(cls, *args):
        cls._objects.add(cls(*args))

    def __init__(self, obj, ptr):
        self.obj = proxy(obj, self.free)
        self.ptr = ptr

    def free(self, deadweakproxy):
        type(self)._objects.remove(self)
        g_free(self.ptr)


class Rectangle(Structure):
    _fields_ = [
        ("x1", c_double),
        ("y1", c_double),
        ("x2", c_double),
        ("y2", c_double),
    ]

    def __repr__(self):
        fmt = '<Rectangle x1="{:8.3f}" y1="{:8.3f}" x2="{:8.3f}" y2="{:8.3f}">'
        return fmt.format(self.x1, self.y1, self.x2, self.y2)


class Page(Poppler.Page):

    def get_text_layout(self):
        length = c_uint()
        ptr = c_void_p()

        args = c_void_p(self._obj), byref(ptr), byref(length)
        ok = poppler_page_get_text_layout(*args)
        if not ok:
            return False, None

        result = (Rectangle * length.value).from_address(ptr.value)
        _Finalizer.new(result, ptr)
        return True, result

Page = override(Page)
__all__.append('Page')
