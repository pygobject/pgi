# Copyright 2012 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

from warnings import warn
from ctypes import cast, sizeof
import weakref

from pgi import gobject
from pgi.gobject import GValuePtr, GValue, GParameterPtr, GParameter
from pgi.gobject import GCallback, GClosureNotify, signal_connect_data
from pgi.gobject import signal_handler_unblock, signal_handler_block
from pgi.gobject import GConnectFlags, signal_handler_disconnect, signal_lookup
from pgi.glib import gpointer, g_malloc0
from pgi.gir import GIInterfaceInfoPtr, GIFunctionInfoFlags
from pgi.gir import GITypeTag, GIObjectInfoPtr

from pgi.util import import_attribute, typeinfo_to_ctypes, set_gvalue_from_py
from pgi.gtype import PGType
from pgi.properties import PropertyAttribute
from pgi.constant import ConstantAttribute


def gparamspec_to_gvalue_ptr(spec, value):
    type_ = spec._info.get_type()
    tag = type_.get_tag().value

    ptr = GValuePtr(GValue())
    ptr.init(spec.value_type._type.value)

    is_interface = False
    if tag == GITypeTag.INTERFACE:
        iface_info = type_.get_interface()
        tag = iface_info.get_type().value
        iface_info.unref()
        is_interface = True

    if not set_gvalue_from_py(ptr, is_interface, tag, value):
        ptr.unset()
        return None

    return ptr


class _Object(object):
    _obj = None
    __gtype__ = None
    __signal_cb_ref = {}
    __weak = {}

    def __init__(self, **kwargs):
        num_params, params = self.__get_gparam_array(**kwargs)
        obj = gobject.newv(self.__gtype__._type, num_params, params)
        gobject.ref_sink(obj)

        self.__weak[weakref.ref(self, self.__destroy)] = obj
        self._obj = obj

    @classmethod
    def __destroy(cls, ref):
        gobject.unref(cls.__weak.pop(ref))

    def __get_gparam_array(self, **kwargs):
        if not kwargs:
            return 0, None

        specs = type(self).props
        array_size = sizeof(GParameter) * len(kwargs)
        array = cast(g_malloc0(array_size), GParameterPtr)

        for i, (key, value) in enumerate(kwargs.iteritems()):
            spec = getattr(specs, key)
            gvalue_ptr = gparamspec_to_gvalue_ptr(spec, value)
            if not gvalue_ptr:
                raise TypeError
            array[i].name = spec.name
            array[i].value = gvalue_ptr.contents

        return i + 1, array

    def __repr__(self):
        form = "<%s object at 0x%x (%s at 0x%x)>"
        name = type(self).__name__
        return form % (name, id(self), self.__gtype__.name, self._obj)

    def connect(self, name, callback):
        if not signal_lookup(name, self.__gtype__._type):
            raise TypeError("unknown signal name %r" % name)

        cb = GCallback(callback)
        destroy = GClosureNotify()
        id_ = signal_connect_data(self._obj, name, cb, None, destroy, 0)
        self.__signal_cb_ref[id_] = (cb, destroy)
        return id_

    def connect_after(self, name, callback):
        if not signal_lookup(name, self.__gtype__._type):
            raise TypeError("unknown signal name %r" % name)

        cb = GCallback(callback)
        destroy = GClosureNotify()
        flags = GConnectFlags.CONNECT_AFTER
        id_ = signal_connect_data(self._obj, name, cb, None, destroy, flags)
        self.__signal_cb_ref[id_] = (cb, destroy)
        return id_

    def disconnect(self, id_):
        if id_ in self.__signal_cb_ref:
            signal_handler_disconnect(self._obj, id_)
            del self.__signal_cb_ref[id_]

    def handler_block(self, id_):
        signal_handler_block(self._obj, id_)

    def handler_unblock(self, id_):
        signal_handler_unblock(self._obj, id_)

    @property
    def __grefcount__(self):
        return cast(self._obj, gobject.GObjectPtr).contents.ref_count


class _Interface(object):
    pass


class Method(object):
    def __init__(self, handle, obj):
        self._handle = handle
        self._obj = obj

    def __call__(self, *args):
        return self._handle(self._obj, *args)


class _ClassMethodAttribute(object):
    def __init__(self, info, name, lib):
        self._name = name
        self._info = info
        self._lib = lib
        self._handles = {}

    def __get_handle(self, name):
        if name in self._handles:
            return self._handles[name]

        info = self._info

        # get argument types
        args = [gpointer]
        for i in xrange(info.get_n_args()):
            arg_info = info.get_arg(i)

            arg_type_info = arg_info.get_type()
            args.append(typeinfo_to_ctypes(arg_type_info))
            arg_type_info.unref()

            arg_info.unref()

        # get return type
        return_info = info.get_return_type()

        # setup ctypes function
        h = getattr(self._lib, info.get_symbol())
        h.restype = typeinfo_to_ctypes(return_info)
        h.argtypes = args

        return_info.unref()
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
    """Creates a GInterface class"""

    iface_info = cast(info, GIInterfaceInfoPtr)

    # Create a new class with a corresponding gtype
    cls_dict = dict(_Interface.__dict__)
    cls_dict["__gtype__"] = PGType(iface_info.get_g_type())
    cls = type(name, _Interface.__bases__, cls_dict)

    # Add constants
    for constant in iface_info.get_constants():
        constant_name = constant.get_name()
        attr = ConstantAttribute(constant, namespace, constant_name, lib)
        setattr(cls, constant_name, attr)
        constant.unref()

    # Add methods
    for method in iface_info.get_methods():
        func_flags = method.get_flags()

        if func_flags.value == GIFunctionInfoFlags.IS_METHOD:
            method_name = method.get_name()
            attr = _ClassMethodAttribute(method, method_name, lib)
            setattr(cls, method_name, attr)
        else:
            method.unref()

    return cls


def ObjectAttribute(info, namespace, name, lib):
    """Creates a GObject class.

    It inherits from the base class and all interfaces it implements.
    """

    obj_info = cast(info, GIObjectInfoPtr)

    # Get the parent class
    parent_obj = obj_info.get_parent()
    if parent_obj:
        parent_namespace = parent_obj.get_namespace()
        parent_name = parent_obj.get_name()
        parent_obj.unref()

        attr = import_attribute(parent_namespace, parent_name)
        bases = (attr,)
    else:
        bases = _Object.__bases__

    # Get all object interfaces
    ifaces = []
    for interface in obj_info.get_interfaces():
        interface_namespace = interface.get_namespace()
        interface_name = interface.get_name()
        interface.unref()

        attr = import_attribute(interface_namespace, interface_name)
        ifaces.append(attr)

    # Combine them to a base class list
    if ifaces:
        bases = tuple(list(bases) + ifaces)

    # Copy template and add gtype, properties
    cls_dict = dict(_Object.__dict__)
    g_type = obj_info.get_g_type()
    cls_dict["__gtype__"] = PGType(g_type)
    cls_dict["props"] = PropertyAttribute(obj_info, namespace, name, g_type)

    # Create a new class
    cls = type(name, bases, cls_dict)
    cls.__module__ = namespace

    # Add constants
    for constant in obj_info.get_constants():
        constant_name = constant.get_name()
        attr = ConstantAttribute(constant, namespace, constant_name, lib)
        setattr(cls, constant_name, attr)
        constant.unref()

    # Add methods
    for method in obj_info.get_methods():
        func_flags = method.get_flags().value

        if func_flags == GIFunctionInfoFlags.IS_METHOD:
            method_name = method.get_name()
            attr = _ClassMethodAttribute(method, method_name, lib)
            setattr(cls, method_name, attr)
        else:
            method.unref()

    return cls
