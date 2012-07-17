# Copyright 2012 Christoph Reiter
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

from ctypes import byref, POINTER, cast
import sys
sys.path.insert(0, '..')

from pgi.gitypes import *

gi_init()

repo = GIRepository.get_default()

error = POINTER(GError)()
repo.require("GLib", "2.0", GIRepositoryLoadFlags.LAZY, byref(error))
check_gerror(error)

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

error = POINTER(GError)()
function_info.invoke(in_args, 5, None, 0, byref(retval), byref(error))
check_gerror(error)

base_info.unref()
