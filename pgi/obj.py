# Copyright 2012 Christoph Reiter
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

from ctypes import cast
from gitypes import GIObjectInfoPtr, GIRegisteredTypeInfoPtr, GIBaseInfoPtr
from gitypes import gobject, GIFunctionInfoFlags, GIFunctionInfoPtr
from gitypes import GICallableInfoPtr, GITypeTag, GIInterfaceInfoPtr
from gitypes import gpointer, gchar_p, gboolean, guint32

from util import import_attribute
from gtype import PGType


class _Object(object):
    _obj = None
    __gtype__ = None

    def __init__(self):
        self._obj = gobject.new(self.__gtype__._type, 0)
        gobject.ref_sink(self._obj)

    def __repr__(self):
        form = "<%s object at 0x%x (%s at 0x%x)>"
        name = type(self).__name__
        return form % (name, id(self), self.__gtype__.name, self._obj)

    def __del__(self):
        gobject.unref(self._obj)


class _Interface(object):
    pass

def gtypeinfo_to_ctypes(info):
    tag = info.get_tag().value
    ptr = info.is_pointer()

    if ptr:
        if tag == GITypeTag.UTF8:
            return gchar_p
        elif tag == GITypeTag.VOID:
            return gpointer
        elif tag == GITypeTag.UTF8 or tag == GITypeTag.FILENAME:
            return gchar_p
        elif tag == GITypeTag.ARRAY:
            return gpointer
    else:
        if tag == GITypeTag.BOOLEAN:
            return gboolean
        elif tag == GITypeTag.UINT32:
            return guint32
        elif tag == GITypeTag.VOID:
            return


class Method(object):
    def __init__(self, handle, obj):
        self._handle = handle
        self._obj = obj

    def __call__(self, *args):
        return self._handle(self._obj, *args)


class _ClassMethodAttribute(object):
    def __init__(self, info, namespace, name, lib):
        self._name = name
        self._info = info
        self._namespace = namespace
        self._lib = lib
        self._handles = {}

    def __get_handle(self, name):
        if name in self._handles:
            return self._handles[name]

        info = self._info

        call_info = cast(info, GICallableInfoPtr)

        # get argument types
        args = [gpointer]
        for i in xrange(call_info.get_n_args()):
            arg_info = call_info.get_arg(i)
            arg_base = cast(arg_info, GIBaseInfoPtr)

            arg_type_info = arg_info.get_type()
            args.append(gtypeinfo_to_ctypes(arg_type_info))
            cast(arg_type_info, GIBaseInfoPtr).unref()

            arg_base.unref()

        # get return type
        return_info = call_info.get_return_type()

        # setup ctypes function
        func_info = cast(info, GIFunctionInfoPtr)
        h = getattr(self._lib, func_info.get_symbol())
        h.restype = gtypeinfo_to_ctypes(return_info)
        h.argtypes = args

        cast(return_info, GIBaseInfoPtr).unref()
        info.unref()

        self._handles[name] = h
        return h

    def __get__(self, instance, owner):
        name = self._name

        # save each method in the base class, so the handle
        # doesn't get re-created with each new object instance
        # TODO: Make new Method classes and lazy attributes instead
        h = self.__get_handle(name)

        attr = Method(h, instance._obj)
        setattr(instance, name, attr)
        return attr


def InterfaceAttribute(info, namespace, name, lib):
    iface_info = cast(info, GIInterfaceInfoPtr)

    cls_dict = dict(_Interface.__dict__)
    cls = type(name, _Interface.__bases__, cls_dict)

    for i in xrange(iface_info.get_n_methods()):
        func_info = iface_info.get_method(i)
        func_flags = func_info.get_flags().value
        base_info = cast(func_info, GIBaseInfoPtr)

        if func_flags == 0 or func_flags == GIFunctionInfoFlags.IS_METHOD:
            mname = base_info.get_name()
            attr = _ClassMethodAttribute(base_info, namespace, mname, lib)
            setattr(cls, mname, attr)
        else:
            base_info.unref()

    return cls


def ObjectAttribute(info, namespace, name, lib):
    obj_info = cast(info, GIObjectInfoPtr)
    reg_info = cast(info, GIRegisteredTypeInfoPtr)

    # get the parent classes if there are any
    parent_obj = obj_info.get_parent()
    if parent_obj:
        parent_base = cast(parent_obj, GIBaseInfoPtr)
        parent_namespace = parent_base.get_namespace()
        parent_name = parent_base.get_name()
        parent_base.unref()

        attr = import_attribute(parent_namespace, parent_name)
        bases = (attr,)
    else:
        bases = _Object.__bases__

    ifaces = []
    for i in xrange(obj_info.get_n_interfaces()):
        if_info = obj_info.get_interface(i)
        if_base = cast(if_info, GIBaseInfoPtr)
        if_name, if_namespace = if_base.get_name(), if_base.get_namespace()
        attr = import_attribute(if_namespace, if_name)
        ifaces.append(attr)
        if_base.unref()

    if ifaces:
        bases = tuple(list(bases) + ifaces)

    cls_dict = dict(_Object.__dict__)
    cls_dict["__gtype__"] = PGType(reg_info.get_g_type())
    cls = type(name, bases, cls_dict)
    cls.__module__ = namespace

    for i in xrange(obj_info.get_n_methods()):
        func_info = obj_info.get_method(i)
        func_flags = func_info.get_flags().value

        base_info = cast(func_info, GIBaseInfoPtr)

        if func_flags == 0 or func_flags == GIFunctionInfoFlags.IS_METHOD:
            mname = base_info.get_name()
            attr = _ClassMethodAttribute(base_info, namespace, mname, lib)
            setattr(cls, mname, attr)
        else:
            base_info.unref()

    return cls
