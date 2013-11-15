# Copyright 2012 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

from . import const
from ._compat import iterkeys
from .importer import require_version, get_required_version
from .codegen import set_backend
from . import foreign


require_version = require_version
get_required_version = get_required_version
set_backend = set_backend

version_info = const.VERSION
__version__ = ".".join(map(str, version_info))


def check_foreign(namespace, name):
    return foreign.get_foreign(namespace, name) is not None


def check_version(version):
    if isinstance(version, basestring):
        version = tuple(map(int, version.split(".")))

    if version > version_info:
        raise ValueError


def install_as_gi():
    """Call before the first gi import to redirect gi imports to pgi"""

    import sys

    # check if gi has already been replaces
    if "gi.repository" in const.PREFIX:
        return

    # make sure gi isn't loaded first
    for mod in iterkeys(sys.modules):
        if mod == "gi" or mod.startswith("gi."):
            raise AssertionError("pgi has to be imported before gi")

    # replace and tell the import hook
    import pgi
    import pgi.repository
    sys.modules["gi"] = pgi
    sys.modules["gi.repository"] = pgi.repository
    const.PREFIX.append("gi.repository")


class PGIDeprecationWarning(RuntimeWarning):
    pass
