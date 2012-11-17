# Copyright 2012 Christoph Reiter
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

from pgi import const
from pgi.importer import require_version, get_required_version

version = const.VERSION
require_version = require_version
get_required_version = get_required_version


def replace_gi():
    """Call before the first gi import to redirect gi imports to pgi"""

    import sys

    # check if gi is already replaces
    if sys.modules.get("gi") is sys.modules[__name__]:
        return

    # make sure gi isn't loaded first
    for mod in sys.modules.iterkeys():
        if mod == "gi" or mod.startswith("gi."):
            raise AssertionError("pgi has to be imported before gi")

    # replace and tell the import hook
    sys.modules["gi"] = sys.modules[__name__]
    const.PREFIX = "gi.repository"


class PGIDeprecationWarning(RuntimeWarning):
    pass
