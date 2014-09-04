# Copyright 2012,2014 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

import os
import types
import sys
import imp
import warnings
from functools import wraps

from pgi import _compat
from pgi import const


class ProxyModule(types.ModuleType):

    def __init__(self, module):
        super(ProxyModule, self).__init__(module.__name__)
        self._module = module

    def __getattr__(self, name):
        return getattr(self._module, name)

    def __dir__(self):
        attrs = set(self.__dict__.keys())
        attrs.update(dir(self._module))
        return sorted(attrs)

    def __repr__(self):
        return repr(self._module)


def get_introspection_module(namespace):
    """Returns the non proxied module for a namespace"""

    mod = sys.modules["pgi.repository." + namespace]
    return getattr(mod, "_module", mod)


def load(namespace, module):
    """Takes a namespace e.g. 'Gtk' and a gi module and returns a proxy
    which contains overrides and will fall back to the original module
    if needed.

    The returned module is either a proxy or the passed in module in
    case no overrides exist.
    """

    proxy = ProxyModule(module)
    for prefix in const.PREFIX:
        sys.modules[prefix + "." + namespace] = proxy

    try:
        name = __name__ + "." + namespace
        override_module = __import__(name, fromlist=[""])
    except Exception as err:
        try:
            paths = [os.path.dirname(__file__)]
            fp, pn, desc = imp.find_module(namespace, paths)
        except ImportError:
            # no need for a proxy then, so revert back
            for prefix in const.PREFIX:
                sys.modules[prefix + "." + namespace] = module
            return module
        else:
            if fp:
                fp.close()
            _compat.reraise(ImportError, err, sys.exc_info()[2])
    else:
        # add all objects referenced in __all__ to the original module
        override_vars = vars(override_module)
        override_all = override_vars.get("__all__") or []

        for var in override_all:
            item = override_vars.get(var)
            assert item is not None
            # make sure new classes have a proper __module__
            try:
                if item.__module__.split(".")[-1] == namespace:
                    item.__module__ = namespace
            except AttributeError:
                pass
            setattr(proxy, var, item)

        return proxy


def override(klass):
    """Takes a override class or function and assigns it dunder arguments
    form the overidden one.
    """

    namespace = klass.__module__.rsplit(".", 1)[-1]
    mod_name = const.PREFIX[-1] + "." + namespace
    module = sys.modules[mod_name]

    if isinstance(klass, types.FunctionType):
        def wrap(wrapped):
            setattr(module, klass.__name__, wrapped)
            return wrapped
        return wrap

    old_klass = klass.__mro__[1]
    name = old_klass.__name__
    klass.__name__ = name
    klass.__module__ = old_klass.__module__

    setattr(module, name, klass)

    return klass


def deprecated(function, instead):
    """Mark a function deprecated so calling it issues a warning"""

    from pgi import PyGIDeprecationWarning

    @wraps(function)
    def wrap(*args, **kwargs):
        warnings.warn("Deprecated, use %s instead" % instead,
                      PyGIDeprecationWarning)
        return function(*args, **kwargs)

    return wrap
