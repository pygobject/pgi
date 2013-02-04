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
from pgi.gobject import GParameter, GClosureNotify, signal_connect_data
from pgi.gobject import signal_handler_unblock, signal_handler_block
from pgi.gobject import GConnectFlags, signal_handler_disconnect, signal_lookup
from pgi.gir import GIInterfaceInfoPtr, GIFunctionInfoFlags, GIObjectInfoPtr

from pgi.ctypesutil import gicast
from pgi.util import import_attribute, Super
from pgi.util import gparamspec_to_gvalue_ptr
from pgi.gtype import PGType
from pgi.properties import PropertyAttribute, PROPS_NAME
from pgi.constant import ConstantAttribute
from pgi.codegen.funcgen import generate_function
from pgi.codegen.siggen import generate_signal_callback


class _Object(object):
    _obj = 0
    __gtype__ = None
    __signal_cb_ref = {}
    __weak = {}
    __cls = None

    super = Super("__init__")

    def __init__(self, *args, **kwargs):
        if not self.super(*args, **kwargs):
            return

        if self.__gtype__.is_abstract():
            raise TypeError("cannot create instance of abstract type %r" %
                            self.__gtype__.name)

        num_params, params = self.__get_gparam_array(**kwargs)
        obj = gobject.newv(self.__gtype__._type, num_params, params)

        # sink unowned objects
        if self._unowned:
            gobject.ref_sink(obj)

        self.__weak[weakref.ref(self, self.__destroy)] = obj
        self._obj = obj

    def _ref(self):
        gobject.ref_sink(self._obj)

    def __hash__(self):
        return hash(self._obj)

    def __eq__(self, other):
        return self._obj == other._obj

    def __cmp__(self, other):
        return cmp(self._obj, other._obj)

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

    def __get_signal(self, name):
        for base in type(self).__mro__[:-1]:
            if base is InterfaceBase:
                continue
            if name in base._sigs:
                return base._sigs[name]

    def __connect(self, flags, name, callback, *user_args):
        if not callable(callback):
            raise TypeError("second argument must be callable")

        info = self.__get_signal(name)
        if not info:
            raise TypeError("unknown signal name %r" % name)

        def _add_self(*args):
            return callback(self, *itertools.chain(args, user_args))
        cb = generate_signal_callback(info)(_add_self)

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
            return getattr(instance or owner, name)
        elif not func_flags or func_flags & GIFunctionInfoFlags.IS_CONSTRUCTOR:
            func = generate_function(info, method=False, throws=throws)
            func = staticmethod(func)
            setattr(owner, name, func)
            return getattr(owner, name)
        else:
            raise NotImplementedError("%r not supported" % flags)


class InterfaceBase(object):
    pass


class _Interface(InterfaceBase):
    def __init__(self):
        raise NotImplementedError("Interface can not be constructed")


def InterfaceAttribute(info):
    """Creates a GInterface class"""

    iface_info = gicast(info, GIInterfaceInfoPtr)

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

    # Add methods
    for method_info in iface_info.get_methods():
        attr = MethodAttribute(method_info)
        setattr(cls, method_info.name, attr)

    cls._sigs = {}

    return cls


def new_class_from_gtype(gtype):
    """Create a new class for a gtype not in the gir.
    The caller is responsible for caching etc.
    """

    parent = gtype.parent.pytype
    if parent is None or parent == PGType.from_name("void"):
        return
    interfaces = [i.pytype for i in gtype.interfaces]
    bases = tuple([parent] + interfaces)

    cls = type(gtype.name, bases, dict(_Object.__dict__))
    cls.__gtype__ = gtype

    return cls


def ObjectAttribute(obj_info):
    """Creates a GObject class.

    It inherits from the base class and all interfaces it implements.
    """

    obj_info = gicast(obj_info, GIObjectInfoPtr)

    # Get the parent class
    parent_obj = obj_info.get_parent()
    if parent_obj:
        attr = import_attribute(parent_obj.namespace, parent_obj.name)
        bases = (attr,)
    else:
        bases = _Object.__bases__

    # Get all object interfaces
    ifaces = []
    for interface in obj_info.get_interfaces():
        attr = import_attribute(interface.namespace, interface.name)
        ifaces.append(attr)

    # Combine them to a base class list
    if ifaces:
        bases = tuple(list(bases) + ifaces)

    # Create a new class
    cls = type(obj_info.name, bases, dict(_Object.__dict__))
    cls.__module__ = obj_info.namespace

    # Set root to unowned= False and InitiallyUnowned=True
    if obj_info.namespace == "GObject":
        if obj_info.name == "InitiallyUnowned":
            cls._unowned = True
        elif obj_info.name == "Object":
            cls._unowned = False

    # GType
    cls.__gtype__ = PGType(obj_info.g_type)

    # Properties
    setattr(cls, PROPS_NAME, PropertyAttribute(obj_info))

    # Add constants
    for constant in obj_info.get_constants():
        constant_name = constant.get_name()
        attr = ConstantAttribute(constant)
        setattr(cls, constant_name, attr)

    # Add methods
    for method_info in obj_info.get_methods():
        method_name = method_info.name
        attr = MethodAttribute(method_info)
        setattr(cls, method_name, attr)

    # Signals
    cls._sigs = {}
    for sig_info in obj_info.get_signals():
        signal_name = sig_info.name
        cls._sigs[signal_name] = sig_info

    return cls
