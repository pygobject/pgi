# Copyright 2012,2013 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

from warnings import warn
from ctypes import cast

from pgi import gobject
from pgi.gobject import GValue, GValuePtr, GObjectClassPtr
from pgi.gobject import G_TYPE_FROM_INSTANCE
from pgi.gir import GIRepositoryPtr, GIInfoType, GIObjectInfoPtr
from pgi.gir import GIInterfaceInfoPtr, GITypeTag

from pgi.util import escape_name, import_attribute, set_gvalue_from_py
from pgi.gtype import PGType


class GParamSpec(object):
    _spec = None
    _info = None

    def __init__(self, spec, name, info):
        self._spec = spec
        self._info = info
        g_type = G_TYPE_FROM_INSTANCE(spec.contents.g_type_instance)
        self.__gtype__ = PGType(g_type)
        self.name = name

    @property
    def flags(self):
        return self._spec.contents.flags.value

    @property
    def nick(self):
        return self._spec.nick

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
            iface_info.unref()
            self.__interface = True

        type_.unref()
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
        else:
            if tag == GIInfoType.ENUM:
                func = lambda: self.__iclass(ptr.enum)

        if func is None:
            ptr.unset()
            name = self.__spec.name
            warn("Property %r unhandled. Type not supported" % name, Warning)
            return None

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


class _Props(object):
    __cache = None
    __cls_cache = None

    def __init__(self, info):
        info.ref()
        self.__info = info

    def __get_gparam_spec(self, owner):
        if self.__cache:
            return self.__cache

        info = self.__info
        cls = _GProps
        cls_dict = dict(cls.__dict__)

        # get the prop classes of all base classes, so we inherit all specs
        prop_bases = []
        for base in owner.__bases__:
            if hasattr(base, "props"):
                prop_bases.append(base.props.__class__)
        prop_bases = tuple(prop_bases) or cls.__bases__

        gtype = info.g_type
        if info.type.value == GIInfoType.OBJECT:
            klass = gtype.class_ref()
            for prop_info in info.get_properties():
                real_name = prop_info.name
                spec = klass.find_property(real_name)
                attr_name = escape_name(real_name)
                cls_dict[attr_name] = GParamSpec(spec, real_name, prop_info)
            gtype.class_unref(klass)
        else:
            iface = gtype.default_interface_ref()
            for prop_info in info.get_properties():
                real_name = prop_info.name
                spec = iface.find_property(real_name)
                attr_name = escape_name(real_name)
                cls_dict[attr_name] = GParamSpec(spec, real_name, prop_info)
            gtype.default_interface_unref(iface)

        attr = type("GProps", tuple(prop_bases), cls_dict)(info.name, False)
        self.__cache = attr
        return attr

    def __get__(self, instance, owner):
        specs = self.__get_gparam_spec(owner)
        if not instance:
            return specs

        # get all the property names of the specs and build properties
        if not self.__cls_cache:
            props = {}
            for key in (p for p in dir(specs) if not p.startswith("_")):
                spec = getattr(specs, key)
                props[key] = Property(spec)

            cls = _GProps
            cls_dict = dict(cls.__dict__)
            cls_dict.update(props)

            self.__cls_cache = type("GProps", cls.__bases__, cls_dict)

        attr = self.__cls_cache(self.__info.name, instance)
        setattr(instance, "props", attr)
        return attr


def PropertyAttribute(obj_info):
    cls = _Props
    cls_dict = dict(cls.__dict__)
    return type("props", cls.__bases__, cls_dict)(obj_info)
