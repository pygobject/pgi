# Copyright 2012 Christoph Reiter
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

from pgi.const import VERSION as version
from pgi.importer import require_version, get_required_version

version = version
require_version = require_version
get_required_version = get_required_version


def _replace_gi():
    """Call before the first gi import to redirect gi imports to pgi"""
    import sys
    import pgi
    import const
    for mod in sys.modules.iterkeys():
        if mod == "gi" or mod.startswith("gi."):
            raise AssertionError(
                "pgi has to be imported before gi")
    sys.modules["gi"] = pgi
    const.PREFIX = "gi.repository"

_replace_gi()


class PGIDeprecationWarning(RuntimeWarning):
    pass
