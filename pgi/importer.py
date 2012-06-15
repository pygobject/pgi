# Copyright 2012 Christoph Reiter
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

import sys
from ctypes import c_char_p, byref, CDLL

from gitypes import GIRepository, GErrorPtr, GIRepositoryLoadFlags
from gitypes import check_gerror, gi_init, gobject

import const
import module
import util


gi_init()
repository = GIRepository.get_default()


class Importer(object):
    PATH = const.PREFIX + "."

    def find_module(self, fullname, path):
        name = self.__get_name(fullname)
        if not name:
            return

        if not repository.enumerate_versions(name):
            return

        return self

    def load_module(self, fullname):
        namespace = self.__get_name(fullname)

        glist = repository.enumerate_versions(namespace)
        if not glist:
            raise ImportError

        versions = util.glist_get_all(glist, c_char_p)
        glist.free()

        versions.sort()
        version = versions[-1]

        return self.__require(namespace, version)

    def __get_name(self, fullname):
        if not fullname.startswith(self.PATH):
            return

        return fullname[len(self.PATH):]

    def __get_fullname(self, namespace):
        return self.PATH + namespace

    def __require_dependencies(self, namespace):
        array = repository.get_dependencies(namespace)
        if not array:
            return

        i = 0
        dep = array[i]
        while dep:
            # FIXME: free dep
            depns, version = dep.split("-", 1)
            self.__require(depns, version)
            i += 1
            dep = array[i]

        gobject.free(array)

    def __require(self, namespace, version):
        fullname = self.__get_fullname(namespace)

        # Dependency already loaded, skip
        if fullname in sys.modules:
            return sys.modules[fullname]

        error = GErrorPtr()
        typelib = repository.require(namespace, version,
                                     GIRepositoryLoadFlags.LAZY,
                                     byref(error))
        if not typelib:
            check_gerror(error)
            error.free()

        # Load all dependencies
        self.__require_dependencies(namespace)

        library = repository.get_shared_library(namespace)
        # FIXME: I guess ignore those?
        if not library:
            return

        # FIXME: Sometimes returns a comma separated list
        library = CDLL(library.split(",")[0])

        # Generate bindings, set up lazy attributes
        instance = module.Module(repository, namespace, library)

        # add to module and sys.modules
        setattr(__import__(const.PREFIX), namespace, instance)
        sys.modules[fullname] = instance

        return instance
