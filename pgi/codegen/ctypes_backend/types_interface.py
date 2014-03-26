# Copyright 2012-2014 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

import ctypes

from pgi.clib.gir import GITypeTag, GIInfoType, GIStructInfo
from pgi.clib.gobject import G_TYPE_FROM_INSTANCE, GTypeInstancePtr
from pgi.clib import glib
from pgi.gtype import PGType
from pgi import foreign, _compat
from pgi.util import import_attribute

from .. import generate_callback_wrapper

from .utils import BaseType, register_type


@register_type(GITypeTag.INTERFACE)
class BaseInterface(BaseType):

    @classmethod
    def get_class(cls, type_):
        iface = type_.get_interface()
        iface_type = iface.type.value

        if iface_type == GIInfoType.OBJECT:
            return Object
        elif iface_type == GIInfoType.INTERFACE:
            return Interface
        elif iface_type == GIInfoType.ENUM:
            return Enum
        elif iface_type == GIInfoType.FLAGS:
            return Flags
        elif iface_type == GIInfoType.STRUCT:
            return Struct
        elif iface_type == GIInfoType.CALLBACK:
            return Callback
        elif iface_type == GIInfoType.UNION:
            return Union

        raise NotImplementedError("Iface not implemented: %r" % iface.type)

    def _import_foreign(self):
        """Gives a ForeignStruct implementation or None"""

        struct_info = self.type.get_interface()
        assert isinstance(struct_info, GIStructInfo)

        if not struct_info.is_foreign:
            return

        return foreign.get_foreign(struct_info.namespace, struct_info.name)

    def _import_type(self):
        iface = self.type.get_interface()
        return import_attribute(iface.namespace, iface.name)


class Object(BaseInterface):

    def check(self, name):
        if self.may_be_null:
            return self.parse("""
if $obj is not $none and not $_.isinstance($obj, $type_class):
    raise TypeError("argument $obj: Expected %s, got %s" %
                    ($type_class.__name__, $obj.__class__.__name__))
""", obj=name, type_class=self._import_type(), none=None)["obj"]

        return self.parse("""
if not $_.isinstance($obj, $type_class):
    raise $_.TypeError("argument $obj: Expected %s, got %s" %
                       ($type_class.__name__, $obj.__class__.__name__))
""", obj=name, type_class=self._import_type())["obj"]

    def pack(self, name):
        if self.may_be_null:
            return self.parse("""
$ptr = $ctypes.c_void_p($obj and $obj._obj)
""", obj=name)["ptr"]

        return self.parse("""
$ptr = $ctypes.c_void_p($obj._obj)
""", obj=name)["ptr"]

    def unpack(self, name):
        def get_class_func(pointer):
            instance = ctypes.cast(pointer, GTypeInstancePtr)
            gtype = PGType(G_TYPE_FROM_INSTANCE(instance.contents))
            pytype = gtype.pytype
            if not pytype:
                raise RuntimeError("Couldn't find python type for %r" % gtype)
            return pytype

        return self.parse("""
# unpack object
if $value:
    $pyclass = $get_class($value)
    $obj = $_.object.__new__($pyclass)
    $obj._obj = $value
else:
    $obj = None
""", value=name, get_class=get_class_func)["obj"]

    def ref(self, name):
            self.parse("""
if $obj:
    $obj._ref()
""", obj=name)

    def new(self):
        return self.parse("""
# new object
$value = $ctypes.c_void_p()
""")["value"]


class Interface(Object):
    pass


class Union(BaseInterface):

    def unpack(self, name):
        return self.parse("""
# unpack union
$union = object.__new__($union_class)
$union._obj = $value
""", union_class=self._import_type(), value=name)["union"]


class Flags(BaseInterface):

    def check(self, name):
        return self.parse("""
if not $_.isinstance($value, $basestring) and not $_.int($value):
    $out = 0
elif $_.isinstance($value, $base_type):
    $out = $_.int($value)
else:
    raise $_.TypeError("Expected %r but got %r" %
                       ($base_type.__name__, $_.type($value).__name__))
""", base_type=self._import_type(), value=name,
basestring=_compat.string_types)["out"]

    def pack(self, name):
        return self.parse("""
$c_value = $ctypes.c_uint($value)
""", value=name)["c_value"]

    def pre_unpack(self, name):
        return self.parse("""
$value = $cvalue.value
""", cvalue=name)["value"]

    def unpack(self, name):
        return self.parse("""
$flags = $flags_class($value)
""", flags_class=self._import_type(), value=name)["flags"]

    def new(self):
        return self.parse("""
$val = $ctypes.c_uint()
""")["val"]


class Struct(BaseInterface):

    def check(self, name):
        base_obj = import_attribute("GObject", "Object")

        foreign_struct = self._import_foreign()

        if foreign_struct:
            foreign_type = foreign_struct.get_type()
            return self.parse("""
if not $_.isinstance($obj, $struct_class):
    raise $_.TypeError("%r is not a %r" % ($obj, $struct_class))
""", struct_class=foreign_type, obj=name)["obj"]
        else:
            return self.parse("""
if not $_.isinstance($obj, ($struct_class, $obj_class)):
    raise $_.TypeError("%r is not a structure object" % $obj)
    """, obj_class=base_obj, struct_class=self._import_type(), obj=name)["obj"]

    def pack(self, name):

        foreign_struct = self._import_foreign()

        if not foreign_struct:
            return self.parse("""
$out = $ctypes.c_void_p($obj._obj)
    """, obj=name)["out"]
        else:
            return self.parse("""
$out = $ctypes.c_void_p($foreign_struct.to_pointer($obj))
""", foreign_struct=foreign_struct, obj=name)["out"]

    def pre_unpack(self, name):
        return self.parse("""
$value = $cvalue.value
""", cvalue=name)["value"]

    def unpack(self, name):
        iface = self.type.get_interface()
        foreign_struct = None
        if iface.is_foreign:
            foreign_struct = foreign.get_foreign(iface.namespace, iface.name)

        if foreign_struct:
            return self.parse("""
if $obj:
    $new_foreign = $foreign.from_pointer($obj)
else:
    $new_foreign = $obj
""", obj=name, foreign=foreign_struct)["new_foreign"]

        return self.parse("""
if $value:
    $obj = $_.object.__new__($type)
    $obj._obj = $value
else:
    $obj = None
""", value=name, type=self._import_type())["obj"]

    def new(self):
        return self.parse("""
$value = $ctypes.c_void_p()
""")["value"]

    def alloc(self):
        struct_class = self._import_type()
        size = struct_class._size
        malloc = glib.g_try_malloc0

        return self.parse("""
$mem = $malloc($size)
if not $mem and $size:
    raise $_.MemoryError
$value = $ctypes.c_void_p($mem)
""", malloc=malloc, size=size)["value"]

    def unpack_gvalue(self, name):

        getter_map = {
            "gboolean": lambda v: v.get_boolean(),
            "gchar": lambda v: chr(v.get_schar()),
            "gdouble": lambda v: v.get_double(),
            "gfloat": lambda v: v.get_float(),
            "GType": lambda v: v.get_gtype(),
            "gint64": lambda v: v.get_int64(),
            "gint": lambda v: v.get_int(),
            "glong": lambda v: v.get_long(),
            "GObject": lambda v: v.get_object(),
            "gpointer": lambda v: v.get_pointer(),
            "gchararray": lambda v: v.get_string(),
            "guint64": lambda v: v.get_uint64(),
            "guint": lambda v: v.get_uint(),
            "gulong": lambda v: v.get_ulong(),
        }

        if _compat.PY3:
            getter_map["guchar"] = lambda v: bytes([v.get_uchar()])
        else:
            getter_map["guchar"] = lambda v: chr(v.get_uchar())

        items = getter_map.items()
        getter_map = dict((PGType.from_name(k), v) for (k, v) in items)

        return self.parse("""
try:
    $out = $lookup[$value.g_type]($value)
except KeyError:
    $out = $value
""", value=name, lookup=getter_map)["out"]


class Callback(BaseInterface):

    def check(self, name):
        return self.parse("""
if not $_.callable($py_cb):
    raise $_.TypeError("%r must be callable" % $py_cb)
""", py_cb=name)["py_cb"]

    def pack(self, name):
        interface = self.type.get_interface()
        pack_func, docstring = generate_callback_wrapper(interface)

        return self.parse("""
$ctypes_cb = $pack_func($py_cb)
""", pack_func=pack_func, py_cb=name)["ctypes_cb"]


class Enum(BaseInterface):

    def check(self, name):
        return self.parse("""
if $value not in $base_type._allowed:
    raise $_.TypeError("Invalid enum: %r" % $value)
""", base_type=self._import_type(), value=name)["value"]

    def pack(self, name):
        return self.parse("""
$c_value = $ctypes.c_uint($value)
""", value=name)["c_value"]

    def pre_unpack(self, name):
        return self.parse("""
$value = $cvalue.value
""", cvalue=name)["value"]

    def unpack(self, name):
        return self.parse("""
$enum = $enum_class($value)
""", enum_class=self._import_type(), value=name)["enum"]

    def new(self):
        return self.parse("""
$val = $ctypes.c_uint()
""")["val"]
