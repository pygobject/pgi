# Copyright 2012 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

from pgi import const
from pgi.importer import require_version, get_required_version

version = const.VERSION
require_version = require_version
get_required_version = get_required_version


def install_as_gi():
    """Call before the first gi import to redirect gi imports to pgi"""

    import sys

    # check if gi has already been replaces
    if "gi.repository" in const.PREFIX:
        return

    # make sure gi isn't loaded first
    for mod in sys.modules.iterkeys():
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
