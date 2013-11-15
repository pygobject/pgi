# Copyright 2013 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

"""Create a gobject constructor object for a specific combination
of property name using g_object_new.

Compared to g_object_newv, this saves us two function calls per parameter.
"""


from . import ACTIVE_BACKENDS
from .utils import CodeBlock
from pgi.clib.gir import GITypeTag, GIInfoType
from pgi.util import escape_builtin, unescape_name


class ConstructorSetter(object):
    TAG = None

    out_var = ""

    @classmethod
    def get_class(cls, type_):
        return cls

    def __init__(self, prop_name, type_, backend):
        self.type = type_
        self.backend = backend
        self.name = prop_name

    def get_type(self):
        return self.backend.get_type(self.type, may_be_null=True)

    def set(self, name):
        return None, name


class BaseInterfaceSetter(ConstructorSetter):
    TAG = GITypeTag.INTERFACE

    @classmethod
    def get_class(cls, type_):
        iface = type_.get_interface()
        iface_type = iface.type.value

        if iface_type == GIInfoType.ENUM:
            return EnumFlagsSetter
        elif iface_type == GIInfoType.OBJECT:
            return ObjectSetter
        elif iface_type == GIInfoType.STRUCT:
            return StructSetter

        raise NotImplementedError(iface.type)


class ObjectSetter(BaseInterfaceSetter):
    def set(self, name):
        var = self.get_type()
        out = var.pack(var.check(name))
        self.out_var = out
        return var.block, out


class StructSetter(BaseInterfaceSetter):
    def set(self, name):
        var = self.get_type()
        out = var.pack(var.check(name))
        self.out_var = out
        return var.block, out


class EnumFlagsSetter(BaseInterfaceSetter):
    def set(self, name):
        var = self.get_type()
        out = var.pack(var.check(name))
        self.out_var = out
        return var.block, out


class BasicSetter(ConstructorSetter):
    def set(self, name):
        var = self.get_type()
        out = var.pack(var.check(name))
        self.out_var = out
        return var.block, out


class BoolSetter(BasicSetter):
    TAG = GITypeTag.BOOLEAN


class Int32Setter(BasicSetter):
    TAG = GITypeTag.INT32


class UInt32Setter(BasicSetter):
    TAG = GITypeTag.UINT32


class DoubleSetter(BasicSetter):
    TAG = GITypeTag.DOUBLE


class UTF8Argument(ConstructorSetter):
    TAG = GITypeTag.UTF8

    def set(self, name):
        var = self.get_type()
        out = var.pack(var.check(name))
        self.out_var = out
        return var.block, out

_classes = {}


def _find_classes():
    global _classes
    for var in globals().values():
        if not isinstance(var, type):
            continue
        if issubclass(var, ConstructorSetter) and var is not ConstructorSetter:
            _classes[var.TAG] = var
_find_classes()


def get_construct_class(arg_type):
    global _classes
    tag_value = arg_type.tag.value
    try:
        cls = _classes[tag_value]
    except KeyError:
        raise NotImplementedError(
            "%r constructor not implemented" % arg_type.tag)
    else:
        return cls.get_class(arg_type)


def _generate_constructor(gtype, specs, names, backend):

    body = CodeBlock()

    in_args = []
    instances = []
    for name in names:
        spec = getattr(specs, name, None)
        if not spec:
            raise TypeError("Property %r not supported" % name)

        type_ = spec._info.get_type()
        const = get_construct_class(type_)
        real_name = unescape_name(name)
        instance = const(real_name, type_, backend)
        instances.append(instance)

        escaped_name = escape_builtin(name)
        in_args.append(escaped_name)

        block, out = instance.set(escaped_name)
        block.write_into(body)

    call_block, return_var = backend.get_constructor(gtype, instances)

    main, var = backend.parse("""
def init($values):
    $func_body
    $call_block
    return $return_var
""", values=", ".join(in_args), call_block=call_block,
        func_body=body, return_var=return_var)

    func = main.compile()["init"]

    return func


def generate_constructor(gtype, specs, names, _cache={}):
    key = tuple([gtype] + names)
    if key in _cache:
        return _cache[key]
    elif len(_cache) > 30:
        _cache.clear()

    for backend in ACTIVE_BACKENDS:
        if backend.NAME == "ctypes":
            break
    backend = backend()

    func = _generate_constructor(gtype, specs, names, backend)
    _cache[key] = func
    return func
