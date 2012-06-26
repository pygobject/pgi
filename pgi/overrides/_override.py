# Copyright 2012 Christoph Reiter
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

import os
import sys

_overrides = None


def load(namespace):
    global _overrides
    _overrides = {}

    # look away now
    p = sys.path
    sys.path = [os.path.dirname(__file__)]
    try:
        __import__(namespace, globals())
    except ImportError:
        pass
    sys.path = p

    return _overrides


def duplicate(klass, name):
    global _overrides
    _overrides[name] = klass


def override(klass):
    global _overrides

    old_klass = klass.__mro__[1]
    name = old_klass.__name__

    _overrides[name] = klass

    klass.__name__ = name
    klass.__module__ = old_klass.__module__

    return klass
