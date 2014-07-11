# Copyright 2013,2014 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

import sys
sys.path.insert(0, '../..')

# XXX
import gc
gc.disable()

import cairocffi
cairocffi.install_as_pycairo()

import pgi
pgi.install_as_gi()

import math
import numpyfix
numpyfix.fix()

import matplotlib
matplotlib.use('GTK3Cairo')
from matplotlib.pyplot import *


if __name__ == "__main__":
    subplot(211)
    plot([math.sin(x / 100.0) for x in range(1000)], label="test1")
    plot([math.cos(x / 100.0) for x in range(1000)], label="test2")
    legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
           ncol=2, mode="expand", borderaxespad=0.)

    subplot(223)
    plot([1, 2, 3], label="test1")
    plot([3, 2, 1], label="test2")
    legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

    show()
