# Copyright 2012 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

from ctypes import POINTER, Structure, c_char_p, cast

from ..glib import gchar_p, Enum, gboolean
from ..ctypesutil import wrap_class, find_library
from .gitypelib import GITypelibPtr

_gir = find_library("girepository-1.0")


class GIInfoType(Enum):
    (INVALID, FUNCTION, CALLBACK, STRUCT, BOXED, ENUM, FLAGS, OBJECT,
     INTERFACE, CONSTANT, INVALID_0, UNION, VALUE, SIGNAL, VFUNC, PROPERTY,
     FIELD, ARG, TYPE, UNRESOLVED) = range(20)

_methods = [
    ("to_string", gchar_p, [GIInfoType]),
]

wrap_class(_gir, GIInfoType, None, "g_info_type_", _methods)


class GIAttributeIter(Structure):
    pass


class GIAttributeIterPtr(POINTER(GIAttributeIter)):
    _type_ = GIAttributeIter


class GIBaseInfo(Structure):
    pass


class GIBaseInfoPtr(POINTER(GIBaseInfo)):
    _type_ = GIBaseInfo
    _unref = False

    def _get_repr(self):
        values = {}
        values["info_type"] = repr(self.type)
        real_type = cast(self, GIBaseInfoPtr).type.value
        if real_type != GIInfoType.TYPE and self.name:
            values["name"] = repr(self.name)
        values["namespace"] = repr(self.namespace)
        values["deprecated"] = repr(self.is_deprecated)
        container = self.get_container()
        if container and container.type.value != GIInfoType.TYPE:
            values["container"] = repr(container.name)

        return values

    def __del__(self):
        if self and self._unref:
            self.unref()

    def __repr__(self):
        l = ", ".join(("%s=%s" % v for v in sorted(self._get_repr().items())))
        return "<%s %s>" % (self._type_.__name__, l)

_methods = [
    ("ref", GIBaseInfoPtr, [GIBaseInfoPtr], False),
    ("unref", None, [GIBaseInfoPtr]),
    ("get_type", GIInfoType, [GIBaseInfoPtr]),
    ("get_name", gchar_p, [GIBaseInfoPtr]),
    ("get_namespace", gchar_p, [GIBaseInfoPtr]),
    ("is_deprecated", gboolean, [GIBaseInfoPtr]),
    ("get_attribute", gchar_p, [GIBaseInfoPtr, gchar_p]),
    ("iterate_attributes", gboolean, [GIBaseInfoPtr, GIAttributeIterPtr,
                                      POINTER(c_char_p), POINTER(c_char_p)]),
    ("get_container", GIBaseInfoPtr, [GIBaseInfoPtr]),
    ("get_typelib", GITypelibPtr, [GIBaseInfoPtr]),
    ("equal", gboolean, [GIBaseInfoPtr, GIBaseInfoPtr]),
]

wrap_class(_gir, GIBaseInfo, GIBaseInfoPtr, "g_base_info_", _methods)

__all__ = ["GIInfoType", "GIAttributeIter", "GIBaseInfo", "GIBaseInfoPtr",
           "GIAttributeIterPtr"]
