# Copyright 2012 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

from ctypes import byref
import sys
sys.path.insert(0, '..')

from pgi.clib.ctypesutil import gicast
from pgi.clib.gir import GIRepository, GIRepositoryLoadFlags, GIFunctionInfoPtr
from pgi.clib.gir import GIArgument
from pgi.clib.glib import GErrorPtr
from pgi.clib.gobject import g_type_init

g_type_init()

repo = GIRepository.get_default()

error = GErrorPtr()
repo.require("GLib", "2.0", GIRepositoryLoadFlags.LAZY, byref(error))
if error:
    raise Exception(error.contents.message)

base_info = repo.find_by_name("GLib", "warn_message")
if not base_info:
    raise Exception

function_info = gicast(base_info, GIFunctionInfoPtr)

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
