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


from .backend import get_backend
from .utils import CodeBlock
from pgi.clib.gir import GITypeTag, GIInfoType
from pgi.util import unescape_parameter


class ConstructorSetter(object):
    TAG = None

    out_var = ""
    desc = ""

    @classmethod
    def get_class(cls, type_):
        return cls

    def __init__(self, prop_name, type_, backend):
        self.type = type_
        self.backend = backend
        self.name = prop_name

    def get_type(self):
        return self.backend.get_type(self.type, self.desc, may_be_null=True)

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

    def set(self, name):
        var = self.get_type()
        out = var.pack_in(name)
        self.out_var = out
        return var.block, out


class ObjectSetter(BaseInterfaceSetter):
    pass


class StructSetter(BaseInterfaceSetter):
    pass


class EnumFlagsSetter(BaseInterfaceSetter):
    pass


class BasicSetter(ConstructorSetter):
    def set(self, name):
        var = self.get_type()
        out = var.pack_in(name)
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


class UTF8Argument(BasicSetter):
    TAG = GITypeTag.UTF8


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


def _generate_constructor(cls, names, backend):

    gtype = cls.__gtype__
    specs = cls.props

    body = CodeBlock()
    in_args = []
    instances = []

    backend.var.add_blacklist(names)

    for name in names:
        try:
            spec = getattr(specs, name)
        except AttributeError:
            raise TypeError("Property %r not supported" % name)

        type_ = spec._info.get_type()
        const = get_construct_class(type_)
        real_name = unescape_parameter(name)
        instance = const(real_name, type_, backend)
        instance.desc = "%s.%s property '%s'" % (
            cls.__module__, cls.__name__, real_name)
        instances.append(instance)

        in_args.append(name)

        block, out = instance.set(name)
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
    func._code = main

    return func


def generate_constructor(cls, names):
    # The generated code depends on the gtype / class and the order
    # of the arguments that can be passed to it.

    cache = cls._constructors
    if names in cache:
        return cache[names]
    elif len(cache) > 3:
        cache.clear()

    backend = get_backend("ctypes")()
    func = _generate_constructor(cls, names, backend)

    cache[names] = func
    return func
