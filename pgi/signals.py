# Copyright 2013 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

from ctypes import byref

from .util import cached_property, escape_parameter
from .clib.glib import guint
from .clib.gobject import signal_list_ids, signal_query, GSignalQuery
from .codegen import generate_callback
from .gtype import PGType


class GSignal(object):
    def __init__(self, signal_id):
        self._id = signal_id
        self._func = None

    @property
    def __doc__(self):
        if self._func:
            return self._func.__doc__
        else:
            # We only expose signals for types in the typelib atm
            # but when we expose others like in pygobject we might want
            # to create a docstring here from the signal query info
            return ""

    def __call__(self, *args, **kwargs):
        assert self._func
        return self._func(*args, **kwargs)

    @cached_property
    def _query(self):
        query = GSignalQuery()
        signal_query(self._id, byref(query))
        return query

    @property
    def id(self):
        return self._query.signal_id

    @property
    def name(self):
        return self._query.signal_name

    @property
    def instance_type(self):
        return PGType(self._query.itype)

    @property
    def return_type(self):
        return PGType(self._query.return_type)

    @property
    def flags(self):
        return self._query.signal_flags.value

    @property
    def param_types(self):
        count = int(self._query.n_params)
        return [PGType(t) for t in self._query.param_types[:count]]


class _GSignalQuery(object):
    def __init__(self, info, pgtype):
        # FIXME: DBusGLib.Proxy ?
        if pgtype == PGType.from_name("void"):
            return

        gtype = pgtype._type
        is_interface = pgtype.is_interface()

        def get_sig_ids(gtype):
            length = guint()
            array = signal_list_ids(gtype, byref(length))
            return array[:length.value]

        if is_interface:
            iface = gtype.default_interface_ref()
            sig_ids = get_sig_ids(gtype)
            gtype.default_interface_unref(iface)
        else:
            klass = gtype.class_ref()
            sig_ids = get_sig_ids(gtype)
            gtype.class_unref(klass)

        for id_ in sig_ids:
            sig = GSignal(id_)
            sig_info = info.find_signal(sig.name)
            if sig_info:
                sig._func = generate_callback(sig_info)
            setattr(self, escape_parameter(sig.name), sig)

_GSignalQuery.__name__ = "GSignalQuery"


class SignalsDescriptor(object):

    def __init__(self, info):
        self.info = info

    def __get__(self, instance, owner):
        return _GSignalQuery(self.info, owner.__gtype__)


def SignalsAttribute(info):
    return SignalsDescriptor(info)
