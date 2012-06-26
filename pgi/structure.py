# Copyright 2012 Christoph Reiter
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

from ctypes import cast
from gitypes import GIStructInfoPtr, GIRegisteredTypeInfoPtr


def StructureAttribute(info, namespace, name, lib):
    cast(info, GIRegisteredTypeInfoPtr)
    cast(info, GIStructInfoPtr)
