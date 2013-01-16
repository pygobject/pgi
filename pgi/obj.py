# Copyright 2012 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

from ctypes import cast
import weakref

from pgi import gobject
from pgi.gobject import GValuePtr, GValue, GParameterPtr, GParameter
from pgi.gobject import GCallback, GClosureNotify, signal_connect_data
from pgi.gobject import signal_handler_unblock, signal_handler_block
from pgi.gobject import GConnectFlags, signal_handler_disconnect, signal_lookup
from pgi.gir import GIInterfaceInfoPtr, GIFunctionInfoFlags
from pgi.gir import GITypeTag, GIObjectInfoPtr

from pgi.util import import_attribute, set_gvalue_from_py
from pgi.gtype import PGType
from pgi.properties import PropertyAttribute
from pgi.constant import ConstantAttribute
from pgi.codegen.funcgen import generate_function


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

    def __init__(self, *args, **kwargs):
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
        nums = len(kwargs)
        array = (GParameter * nums)()
        for i, (key, value) in enumerate(kwargs.iteritems()):
            spec = getattr(specs, key, None)
            if not spec:
                raise TypeError("Property %r not supported" % key)
            gvalue_ptr = gparamspec_to_gvalue_ptr(spec, value)
            param = array[i]
            param.name = spec.name
            param.value = gvalue_ptr.contents

        return nums, array

    def __repr__(self):
        form = "<%s object at 0x%x (%s at 0x%x)>"
        name = type(self).__name__
        return form % (name, id(self), self.__gtype__.name, self._obj)

    def connect(self, name, callback):
        if not callable(callback):
            raise TypeError("second argument must be callable")

        if not signal_lookup(name, self.__gtype__._type):
            raise TypeError("unknown signal name %r" % name)

        def _add_self(*args):
            return callback(self, *args)
        cb = GCallback(_add_self)
        destroy = GClosureNotify()
        id_ = signal_connect_data(self._obj, name, cb, None, destroy, 0)
        self.__signal_cb_ref[id_] = (cb, destroy)
        return id_

    def connect_after(self, name, callback):
        if not callable(callback):
            raise TypeError("second argument must be callable")

        if not signal_lookup(name, self.__gtype__._type):
            raise TypeError("unknown signal name %r" % name)

        def _add_self(*args):
            return callback(self, *args)
        cb = GCallback(_add_self)
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


class MethodAttribute(object):
    def __init__(self, info, namespace, name, *args):
        super(MethodAttribute, self).__init__()

        self._info = info
        self._namespace = namespace
        self._name = name

    def __get__(self, instance, owner):
        func_flags = self._info.get_flags().value
        name = self._name
        info = self._info
        namespace = self._namespace

        if func_flags == GIFunctionInfoFlags.IS_METHOD:
            func = generate_function(info, namespace, name, method=True)
            setattr(owner, name, func)
            return getattr(instance or owner, name)
        elif func_flags == GIFunctionInfoFlags.IS_CONSTRUCTOR:
            func = generate_function(info, namespace, name, method=False)
            func = staticmethod(func)
            setattr(owner, name, func)
            return getattr(owner, name)
        elif func_flags == 0:
            func = generate_function(info, namespace, name, method=False)
            func = staticmethod(func)
            setattr(owner, name, func)
            return getattr(owner, name)
        else:
            raise NotImplementedError


class _Interface(object):
    pass


def InterfaceAttribute(info, namespace, name, lib):
    """Creates a GInterface class"""

    iface_info = cast(info, GIInterfaceInfoPtr)

    # Create a new class with a corresponding gtype
    cls_dict = dict(_Interface.__dict__)
    g_type = iface_info.get_g_type()
    cls_dict["__gtype__"] = PGType(g_type)
    cls_dict["props"] = PropertyAttribute(iface_info, namespace, name, g_type)

    cls = type(name, _Interface.__bases__, cls_dict)

    # Add constants
    for constant in iface_info.get_constants():
        constant_name = constant.get_name()
        attr = ConstantAttribute(constant, namespace, constant_name, lib)
        setattr(cls, constant_name, attr)
        constant.unref()

    # Add methods
    for method_info in iface_info.get_methods():
        method_name = method_info.get_name()
        attr = MethodAttribute(method_info, namespace, method_name, lib)
        if attr:
            setattr(cls, method_name, attr)

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
    for method_info in obj_info.get_methods():
        method_name = method_info.get_name()
        attr = MethodAttribute(method_info, namespace, method_name, lib)
        if attr:
            setattr(cls, method_name, attr)

    return cls
