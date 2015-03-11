# Copyright 2012,2015 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

import sys
sys.path.insert(0, '..')

from pgi.clib.glib import gerror
from pgi.clib.gobject import g_type_init
from pgi.clib.gir import GIRepository, GIRepositoryLoadFlags, GIArgument

g_type_init()

repo = GIRepository.get_default()
repo.require("GLib", "2.0", GIRepositoryLoadFlags.LAZY)

function_info = repo.find_by_name("GLib", "warn_message")
assert function_info

in_args = [
    GIArgument(v_string="GITYPES"),
    GIArgument(v_string=__file__),
    GIArgument(v_uint=42),
    GIArgument(v_string="main"),
    GIArgument(v_string="hello world"),
]

retval = GIArgument()

function_info.invoke(in_args, None, retval)
