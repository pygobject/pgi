# Copyright 2012 Christoph Reiter
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

import sys
from ctypes import c_char_p, byref, CDLL

from gitypes import GIRepositoryPtr, GErrorPtr, check_gerror

import const
import module
import util
import overrides

_versions = {}

class Importer(object):
    PATH = const.PREFIX + "."

    def find_module(self, fullname, path):
        name = self.__get_name(fullname)
        if not name:
            return

        repository = GIRepositoryPtr()
        if not repository.enumerate_versions(name):
            return

        return self

    def load_module(self, fullname):
        namespace = self.__get_name(fullname)
        repository = GIRepositoryPtr()

        glist = repository.enumerate_versions(namespace)
        if not glist:
            raise ImportError

        if namespace in _versions:
            version = _versions[namespace]
        else:
            versions = sorted(util.glist_to_list(glist, c_char_p))
            if not versions:
                raise ImportError
            version = versions[-1]

        # Dependency already loaded, skip
        if fullname in sys.modules:
            return sys.modules[fullname]

        error = GErrorPtr()
        typelib = repository.require(namespace, version, 0, byref(error))
        if not typelib:
            check_gerror(error)
            error.free()

        library = repository.get_shared_library(namespace)
        # FIXME: I guess ignore those?
        if not library:
            return

        # FIXME: Sometimes returns a comma separated list
        library = CDLL(library.split(",")[0])

        # Generate bindings, set up lazy attributes
        instance = module.Module(repository, namespace, library)
        instance._version = version

        # add to module and sys.modules
        setattr(__import__(const.PREFIX), namespace, instance)
        sys.modules[fullname] = instance

        # Import a override module if available.
        overrides.load(namespace, instance)

        return instance

    def __get_name(self, fullname):
        if not fullname.startswith(self.PATH):
            return

        return fullname[len(self.PATH):]
