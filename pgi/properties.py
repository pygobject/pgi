# Copyright 2012,2013 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

from warnings import warn
import ctypes

from .clib import gobject
from .clib.gobject import GValue, GValuePtr, G_TYPE_FROM_INSTANCE
from .clib.gobject import GObjectClassPtr
from .clib.gir import GIInfoType, GITypeTag

from .util import escape_name, unescape_name, InfoIterWrapper
from .util import import_attribute, set_gvalue_from_py
from .gtype import PGType


PROPS_NAME = "props"


class GParamSpec(object):
    _spec = None
    _info = None

    def __init__(self, spec, name, info):
        self._spec = spec
        self._info = info
        self.name = name

    @property
    def __gtype__(self):
        return G_TYPE_FROM_INSTANCE(self._spec.contents.g_type_instance)

    @property
    def flags(self):
        return self._spec.contents.flags.value

    @property
    def nick(self):
        return self._spec.nick

    @property
    def blurb(self):
        return self._spec.blurb

    @property
    def owner_type(self):
        return PGType(self._spec.contents.owner_type)

    @property
    def value_type(self):
        return PGType(self._spec.contents.value_type)

    def __repr__(self):
        return "<%s %r>" % (self.__gtype__.name, self.name)


class Property(object):
    def __init__(self, spec):
        self.__spec = spec
        type_ = spec._info.get_type()
        self.__tag = type_.tag.value

        self.__interface = False
        if self.__tag == GITypeTag.INTERFACE:
            iface_info = type_.get_interface()
            self.__tag = iface_info.type.value
            name = iface_info.name
            namespace = iface_info.namespace
            self.__iclass = import_attribute(namespace, name)
            self.__interface = True

        self.__value_type = spec.value_type._type.value

    def __get__(self, instance, owner):
        ptr = GValuePtr(GValue())
        ptr.init(self.__value_type)

        tag = self.__tag

        func = None
        if not self.__interface:
            if tag == GITypeTag.UTF8:
                func = lambda: ptr.string
            elif tag == GITypeTag.INT32:
                func = lambda: ptr.int
            elif tag == GITypeTag.BOOLEAN:
                func = lambda: ptr.boolean
            elif tag == GITypeTag.FLOAT:
                func = lambda: ptr.float
        else:
            if tag == GIInfoType.ENUM:
                func = lambda: self.__iclass(ptr.enum)
            elif tag == GIInfoType.OBJECT:
                def func():
                    adr = ptr.get_object()
                    if adr:
                        new = object.__new__(self.__iclass)
                        new._obj = ptr.get_object()
                        return new
                    else:
                        return None

        if func is None:
            ptr.unset()
            name = self.__spec.name
            warn("Property %r unhandled. Type not supported" % name, Warning)
            return None

        if not instance._object:
            ptr.unset()
            raise TypeError("Object not initialized")

        gobject.get_property(instance._object, self.__spec.name, ptr)
        return func()

    def __set__(self, instance, value):
        ptr = GValuePtr(GValue())
        ptr.init(self.__value_type)

        tag = self.__tag

        if not set_gvalue_from_py(ptr, self.__interface, tag, value):
            ptr.unset()
            name = self.__spec.name
            warn("Property %r unhandled. Type not supported" % name, Warning)
            return

        gobject.set_property(instance._object, self.__spec.name, ptr)


class _GProps(object):
    def __init__(self, name, instance):
        self.__name = name
        self.__instance = instance

    @property
    def _object(self):
        return self.__instance._obj

    def __repr__(self):
        text = (self.__instance and "instance ") or ""
        return "<GProps of %s%r>" % (text, self.__name)


class PropertyIterWrapper(InfoIterWrapper):
    def _get_count(self, source):
        return source.n_properties

    def _get_info(self, source, index):
        return source.get_property(index)

    def _get_name(self, info):
        return info.name


class _ObjectClassProp(object):
    def __init__(self, info, owner):
        self._info = info
        self._wrapper = PropertyIterWrapper(info)
        self._owner = owner

    def __get_base_props(self):
        for base in self._owner.__mro__:
            props = getattr(base, PROPS_NAME, None)
            if not props or props is self:
                continue
            yield props

    def __dir__(self):
        names = [escape_name(n) for n in self._wrapper.iternames()]
        for props in self.__get_base_props():
            names.extend([escape_name(n) for n in props._wrapper.iternames()])

        base = dir(self.__class__)
        return list(set(base + names))

    def __getattr__(self, name):
        for props in self.__get_base_props():
            try:
                return getattr(props, name)
            except AttributeError:
                pass

        info = self._info
        gname = unescape_name(name)
        prop_info = self._wrapper.lookup_name(gname)
        if prop_info:
            gtype = info.g_type
            if info.type.value == GIInfoType.OBJECT:
                klass = gtype.class_ref()
                klass = ctypes.cast(klass, GObjectClassPtr)
                spec = klass.find_property(gname)
                gtype.class_unref(klass)
            else:
                iface = gtype.default_interface_ref()
                spec = iface.find_property(gname)
                gtype.default_interface_unref(iface)
            gspec = GParamSpec(spec, gname, prop_info)
            setattr(self, name, gspec)
            return gspec

        raise AttributeError


class _PropsDescriptor(object):
    __cache = None
    __cls_cache = None

    def __init__(self, info):
        self._info = info

    def __get_gparam_spec(self, owner):
        if not self.__cache:
            cls_dict = dict(_ObjectClassProp.__dict__)
            bases = (object,)
            self.__cache = type("GProps", bases, cls_dict)(self._info, owner)
        return self.__cache

    def __get_gprops_class(self, specs):
        if not self.__cls_cache:
            cls = _GProps
            cls_dict = dict(cls.__dict__)

            for key in (p for p in dir(specs) if not p.startswith("_")):
                spec = getattr(specs, key)
                cls_dict[key] = Property(spec)

            self.__cls_cache = type("GProps", cls.__bases__, cls_dict)
        return self.__cls_cache

    def __get__(self, instance, owner):
        specs = self.__get_gparam_spec(owner)
        if not instance:
            return specs

        gprops = self.__get_gprops_class(specs)
        attr = gprops(self._info.name, instance)
        setattr(instance, PROPS_NAME, attr)
        return attr


def PropertyAttribute(obj_info):
    cls = _PropsDescriptor
    cls_dict = dict(cls.__dict__)
    return type(obj_info.name + "Props", cls.__bases__, cls_dict)(obj_info)
