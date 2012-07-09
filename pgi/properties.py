# Copyright 2012 Christoph Reiter
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

from ctypes import cast

from gitypes import GObjectClassPtr, G_TYPE_FROM_INSTANCE, GIBaseInfoPtr
from gitypes import GIRepositoryPtr, GIInfoType, GIObjectInfoPtr
from gitypes import GIInterfaceInfoPtr

from util import escape_name
from gtype import PGType


class GParamSpec(object):
    _spec = None

    def __init__(self, spec, name):
        self._spec = spec
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
    def __init__(self, name):
        self.__name = name

    def __get__(self, instance, owner):
        return None

    def __set__(self, instance, value):
        raise AttributeError


class _GProps(object):
    def __init__(self, name, instance):
        self.__name = name
        self.__instance = instance

    def __repr__(self):
        text = (self.__instance and "instance ") or ""
        return "<GProps of %s%r>" % (text, self.__name)


class _Props(object):
    __cache = None
    __inst_cache = None

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


        obj_class = cast(self.__gtype.class_peek(), GObjectClassPtr)
        for i in xrange(info.get_n_properties()):
            prop_info = info.get_property(i)
            prop_base = cast(prop_info, GIBaseInfoPtr)
            real_name = prop_base.get_name()
            spec = obj_class.find_property(real_name)
            attr_name = escape_name(real_name)
            cls_dict[attr_name] = GParamSpec(spec, real_name)
            prop_base.unref()

        base_info.unref()

        attr = type("GProps", tuple(prop_bases), cls_dict)(name, False)
        self.__cache = attr
        return attr

    def __get__(self, instance, owner):
        specs = self.__get_gparam_spec(owner)
        if not instance:
            return specs

        attr = self.__inst_cache
        if not attr:
            cls = _GProps
            cls_dict = dict(cls.__dict__)

            for key in (p for p in dir(specs) if not p.startswith("_")):
                spec = getattr(specs, key)
                cls_dict[key] = Property(spec.name)

            attr = type("GProps", cls.__bases__, cls_dict)(self.__name, True)
            self.__inst_cache = attr

        setattr(instance, "props", attr)
        return attr


def PropertyAttribute(info, namespace, name, gtype):
    cls = _Props
    cls_dict = dict(cls.__dict__)
    return type("props", cls.__bases__, cls_dict)(namespace, name, gtype)
