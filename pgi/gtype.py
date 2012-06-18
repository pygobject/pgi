# Copyright 2012 Christoph Reiter
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

from gitypes import GType


class PGType(object):
    def __init__(self, type_):
        self._type = type_

    @property
    def name(self):
        return self._type.name()

    @property
    def depth(self):
        return self._type.depth()

    def __repr__(self):
        return "<GType %s (%d)>" % (self.name, self._type.value)
