# Copyright 2012 Christoph Reiter
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

from pgi.const import VERSION as version
from pgi.importer import require_version, get_required_version

version = version

def replace_gi():
    """Call before the first gi import to redirect gi imports to pgi"""
    import sys
    import pgi
    import const
    sys.modules["gi"] = pgi
    const.PREFIX = "gi.repository"


class PGIDeprecationWarning(RuntimeWarning):
    pass
