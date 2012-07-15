# Copyright 2012 Christoph Reiter
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

from giargument import *
from gibaseinfo import *
from gicallableinfo import *
from giconstantinfo import *
from gienuminfo import *
from gifieldinfo import *
from giinterfaceinfo import *
from giobjectinfo import *
from giregisteredtypeinfo import *
from girepository import *
from gistructinfo import *
from gitypeinfo import *
from gitypelib import *
from giunioninfo import *
from glib import *
from gobject import *


def gi_init():
    from _util import wrap_setup
    wrap_setup()
    g_type_init()
