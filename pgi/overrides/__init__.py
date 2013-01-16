# Copyright 2012 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

import os
import types
import imp
import traceback


_overrides = []
_active_module = []
_proxies = {}


class ProxyModule(object):
    def __init__(self, module):
        super(ProxyModule, self).__init__()
        self._module = module

    def __getattr__(self, name):
        attr = getattr(self._module, name)
        setattr(self, name, attr)
        return attr


def get_introspection_module(namespace):
    global _proxies

    if namespace not in _proxies:
        from pgi.util import import_module
        module = import_module(namespace)
        _proxies[namespace] = ProxyModule(module)
    return _proxies[namespace]


def load(namespace, module):
    global _active_module, _overrides

    _active_module.append(module)
    _overrides.append({})
    try:
        name = __package__ + "." + namespace
        override_module = __import__(name, fromlist=[""])
    except ImportError:
        exc = traceback.format_exc()
        try:
            paths = [os.path.dirname(__file__)]
            fp, pn, desc = imp.find_module(namespace, paths)
        except ImportError:
            pass
        else:
            if fp:
                fp.close()
            print exc
            raise ImportError("Failed to load overrides for %r" % namespace)
    else:
        # add all objects referenced in __all__ to the original module
        override_vars = vars(override_module)
        override_all = override_vars.get("__all__") or []
        for var in override_all:
            item = override_vars.get(var)
            if item:
                setattr(module, var, item)

        # Inject a fake namespace module in the overrides module.
        # It will contain all original classes that were overridden
        # and will pull in any other attribute from the real one if needed.
        proxy = get_introspection_module(namespace)
        for name, klass in _overrides[-1].iteritems():
            setattr(proxy, name, klass)

    _active_module.pop(-1)
    _overrides.pop(-1)


def duplicate(klass, name):
    global _active_module
    module = _active_module[-1]

    assert not hasattr(module, name)
    setattr(module, name, klass)


def override(klass):
    global _active_module, _overrides
    module = _active_module[-1]

    if isinstance(klass, types.FunctionType):
        def wrap(wrapped):
            setattr(module, klass.__name__, wrapped)
            return wrapped
        return wrap

    old_klass = klass.__mro__[1]
    name = old_klass.__name__
    klass.__name__ = name
    klass.__module__ = old_klass.__module__

    assert getattr(module, name) is old_klass

    setattr(module, name, klass)
    _overrides[-1][name] = old_klass

    return klass
