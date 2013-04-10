# Copyright 2013 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

from ctypes import byref

from pgi.util import cached_property, escape_name
from pgi.glib import guint
from pgi.gobject import signal_list_ids, signal_query, GSignalQuery
from pgi.gtype import PGType


class GSignal(object):
    def __init__(self, signal_id):
        self.id = signal_id

    @cached_property
    def _query(self):
        query = GSignalQuery()
        signal_query(self.id, byref(query))
        return query

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
        return int(self._query.signal_flags)

    @property
    def param_types(self):
        count = int(self._query.n_params)
        return [PGType(t) for t in self._query.param_types[:count]]


class _GSignalQuery(object):
    def __init__(self, pgtype):
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
            setattr(self, escape_name(sig.name), sig)

_GSignalQuery.__name__ = "GSignalQuery"


class SignalsDescriptor(object):
    def __get__(self, instance, owner):
        return _GSignalQuery(owner.__gtype__)


def SignalsAttribute():
    return SignalsDescriptor()
