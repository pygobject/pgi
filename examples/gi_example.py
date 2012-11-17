# Copyright 2012 Christoph Reiter
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

from ctypes import byref, cast
import sys
sys.path.insert(0, '..')

from pgi.gir import *
from pgi.glib import *
from pgi.gobject import *

g_type_init()

repo = GIRepository.get_default()

error = GErrorPtr()
repo.require("GLib", "2.0", GIRepositoryLoadFlags.LAZY, byref(error))
if error:
    raise Exception(error.contents.message)

base_info = repo.find_by_name("GLib", "warn_message")
if not base_info:
    raise Exception

function_info = cast(base_info, GIFunctionInfoPtr)

in_args_type = GIArgument * 5
in_args = in_args_type(GIArgument(v_string="GITYPES"),
                       GIArgument(v_string=__file__),
                       GIArgument(v_uint=42),
                       GIArgument(v_string="main"),
                       GIArgument(v_string="hello world"),
)
retval = GIArgument()

error = GErrorPtr()
function_info.invoke(in_args, 5, None, 0, byref(retval), byref(error))
if error:
    raise Exception(error.contents.message)

base_info.unref()
