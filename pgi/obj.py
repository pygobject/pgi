# Copyright 2012 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

import itertools
from ctypes import cast
import weakref

from pgi import gobject
from pgi.gobject import GParameter
from pgi.gobject import GCallback, GClosureNotify, signal_connect_data
from pgi.gobject import signal_handler_unblock, signal_handler_block
from pgi.gobject import GConnectFlags, signal_handler_disconnect, signal_lookup
from pgi.gir import GIInterfaceInfoPtr, GIFunctionInfoFlags
from pgi.gir import GITypeTag, GIObjectInfoPtr

from pgi.util import import_attribute, set_gvalue_from_py
from pgi.util import gparamspec_to_gvalue_ptr
from pgi.gtype import PGType
from pgi.properties import PropertyAttribute
from pgi.constant import ConstantAttribute
from pgi.codegen.funcgen import generate_function


class _Object(object):
    _obj = 0
    __gtype__ = None
    __signal_cb_ref = {}
    __weak = {}
    __cls = None

    def __init__(self, *args, **kwargs):
        # HACK: no __class__, no super
        # traverse manually in mro until object is reached
        self.__cls = self.__cls or type(self)
        next_cls = self.__cls.__mro__[1]
        if next_cls is not object:
            self.__cls = next_cls
            next_cls.__init__(self, *args, **kwargs)
            return
        del self.__cls

        num_params, params = self.__get_gparam_array(**kwargs)
        obj = gobject.newv(self.__gtype__._type, num_params, params)

        # sink unowned objects
        unowned = import_attribute("GObject", "InitiallyUnowned")
        if isinstance(self, unowned):
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

    def __connect(self, flags, name, callback, *user_args):
        if not callable(callback):
            raise TypeError("second argument must be callable")

        if not signal_lookup(name, self.__gtype__._type):
            raise TypeError("unknown signal name %r" % name)

        def _add_self(*args):
            return callback(self, *itertools.chain(args, user_args))
        cb = GCallback(_add_self)
        destroy = GClosureNotify()
        id_ = signal_connect_data(self._obj, name, cb, None, destroy, flags)
        self.__signal_cb_ref[id_] = (cb, destroy)
        return id_


    def connect(self, name, callback, *args):
        return self.__connect(0, name, callback, *args)

    def connect_after(self, name, callback, *args):
        flags = GConnectFlags.CONNECT_AFTER
        return self.__connect(flags, name, callback, *args)

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
    def __init__(self, info):
        super(MethodAttribute, self).__init__()
        info.ref()
        self._info = info

    def __get__(self, instance, owner):
        info = self._info
        flags = info.flags
        func_flags = flags.value
        name = info.name

        throws = func_flags & GIFunctionInfoFlags.THROWS

        if func_flags & GIFunctionInfoFlags.IS_METHOD:
            func = generate_function(info, method=True, throws=throws)
            setattr(owner, name, func)
            info.unref()
            return getattr(instance or owner, name)
        elif not func_flags or func_flags & GIFunctionInfoFlags.IS_CONSTRUCTOR:
            func = generate_function(info, method=False, throws=throws)
            func = staticmethod(func)
            setattr(owner, name, func)
            info.unref()
            return getattr(owner, name)
        else:
            raise NotImplementedError("%r not supported" % flags)


class _Interface(object):
    pass


def InterfaceAttribute(info):
    """Creates a GInterface class"""

    iface_info = cast(info, GIInterfaceInfoPtr)

    # Create a new class
    cls = type(info.name, _Interface.__bases__, dict(_Interface.__dict__))
    cls.__module__ = iface_info.namespace

    # GType
    cls.__gtype__ = PGType(iface_info.g_type)

    # Properties
    cls.props = PropertyAttribute(iface_info)

    # Add constants
    for constant in iface_info.get_constants():
        constant_name = constant.name
        attr = ConstantAttribute(constant)
        setattr(cls, constant_name, attr)
        constant.unref()

    # Add methods
    for method_info in iface_info.get_methods():
        attr = MethodAttribute(method_info)
        setattr(cls, method_info.name, attr)
        method_info.unref()

    return cls


def ObjectAttribute(info):
    """Creates a GObject class.

    It inherits from the base class and all interfaces it implements.
    """

    obj_info = cast(info, GIObjectInfoPtr)

    # Get the parent class
    parent_obj = obj_info.get_parent()
    if parent_obj:
        attr = import_attribute(parent_obj.namespace, parent_obj.name)
        parent_obj.unref()
        bases = (attr,)
    else:
        bases = _Object.__bases__

    # Get all object interfaces
    ifaces = []
    for interface in obj_info.get_interfaces():
        attr = import_attribute(interface.namespace, interface.name)
        ifaces.append(attr)
        interface.unref()

    # Combine them to a base class list
    if ifaces:
        bases = tuple(list(bases) + ifaces)

    # Create a new class
    cls = type(info.name, bases, dict(_Object.__dict__))
    cls.__module__ = obj_info.namespace

    # GType
    cls.__gtype__ = PGType(obj_info.g_type)

    # Properties
    cls.props = PropertyAttribute(obj_info)

    # Add constants
    for constant in obj_info.get_constants():
        constant_name = constant.get_name()
        attr = ConstantAttribute(constant)
        setattr(cls, constant_name, attr)
        constant.unref()

    # Add methods
    for method_info in obj_info.get_methods():
        method_name = method_info.name
        attr = MethodAttribute(method_info)
        if attr:
            setattr(cls, method_name, attr)

    return cls
