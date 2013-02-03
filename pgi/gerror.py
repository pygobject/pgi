# Copyright 2013 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.


class PGError(Exception):

    def __init__(self, error):
        self.__error = error

    @property
    def domain(self):
        return self.__error.domain.string

    @property
    def code(self):
        return self.__error.code

    @property
    def message(self):
        return self.__error.message

PGError.__name__ = "GError"
