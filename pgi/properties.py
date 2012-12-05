# Copyright 2012 Christoph Reiter
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
        return self._spec.get_nick()

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
        self.__tag = type_.get_tag().value

        self.__interface = False
        if self.__tag == GITypeTag.INTERFACE:
            iface_info = type_.get_interface()
            self.__tag = iface_info.get_type().value
            name = iface_info.get_name()
            namespace = iface_info.get_namespace()
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
                func = ptr.get_string
            elif tag == GITypeTag.INT32:
                func = ptr.get_int
            elif tag == GITypeTag.BOOLEAN:
                func = ptr.get_boolean
        else:
            if tag == GIInfoType.ENUM:
                func = lambda: self.__iclass(ptr.get_enum())

        if not func:
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

    def __init__(self, namespace, name, gtype):
        self.__namespace = namespace
        self.__name = name
        self.__gtype = gtype

    def __get_gparam_spec(self, owner):
        if self.__cache:
            return self.__cache

        namespace, name = self.__namespace, self.__name

        # get the base info. props won't be used that frequently, so no reason
        # to keep it arround
        repo = GIRepositoryPtr()
        base_info = repo.find_by_name(namespace, name)
        type_ = base_info.get_type().value
        if type_ == GIInfoType.OBJECT:
            info = cast(base_info, GIObjectInfoPtr)
        else:
            info = cast(base_info, GIInterfaceInfoPtr)

        cls = _GProps
        cls_dict = dict(cls.__dict__)

        # get the prop classes of all base classes, so we inherit all specs
        prop_bases = []
        for base in owner.__bases__:
            if hasattr(base, "props"):
                prop_bases.append(base.props.__class__)
        prop_bases = tuple(prop_bases) or cls.__bases__

        klass = self.__gtype.class_ref()
        obj_class = cast(klass, GObjectClassPtr)
        for i in xrange(info.get_n_properties()):
            prop_info = info.get_property(i)
            real_name = prop_info.get_name()
            spec = obj_class.find_property(real_name)
            attr_name = escape_name(real_name)
            cls_dict[attr_name] = GParamSpec(spec, real_name, prop_info)

        self.__gtype.class_unref(klass)
        base_info.unref()

        attr = type("GProps", tuple(prop_bases), cls_dict)(name, False)
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

        attr = self.__cls_cache(self.__name, instance)
        setattr(instance, "props", attr)
        return attr


def PropertyAttribute(info, namespace, name, gtype):
    cls = _Props
    cls_dict = dict(cls.__dict__)
    return type("props", cls.__bases__, cls_dict)(namespace, name, gtype)
