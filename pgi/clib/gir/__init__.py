# Copyright 2012 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

from .giargument import *
from .gibaseinfo import *
from .gicallableinfo import *
from .giconstantinfo import *
from .gienuminfo import *
from .gifieldinfo import *
from .giinterfaceinfo import *
from .giobjectinfo import *
from .giregisteredtypeinfo import *
from .girepository import *
from .gistructinfo import *
from .gitypeinfo import *
from .gitypelib import *
from .giunioninfo import *
from .giarginfo import *
from .gipropertyinfo import *

from ..ctypesutil import wrap_setup

wrap_setup()
