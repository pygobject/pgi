# Copyright 2013 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

import sys
sys.path.insert(0, '../..')

# FIXME... :)
import gc
gc.disable()

import cairocffi
cairocffi.install_as_pycairo()

import pgi
pgi.install_as_gi()

import matplotlib
matplotlib.use('GTK3Cairo')
from matplotlib import pyplot

import math


pyplot.plot([math.sin(x / 100.0) for x in range(1000)])
pyplot.show()
