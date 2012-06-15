#! /usr/bin/python
# Copyright 2012 Christoph Reiter
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

import tests
import os


# Run with both bindings, PGI first
# Skip the second run if the first one fails
pid = os.fork()
if pid != 0:
    pid, status = os.waitpid(pid, 0)
    if status:
        exit(status)
exit(tests.test(pid != 0))
