# Copyright 2012 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

"""Provides a custom PEP-302 import hook to load GI libraries"""

import sys
from ctypes import c_char_p, byref, CDLL

from .clib.gir import GIRepositoryPtr
from .clib.glib import GErrorPtr
from . import const, module, util, overrides

_versions = {}


def require_version(namespace, version):
    """Set a version for the namespace to be loaded.
    This needs to be called before importing the namespace or any
    namespace that depends on it.
    """

    global _versions

    repo = GIRepositoryPtr()

    namespace = util.encode(namespace)
    version = util.encode(version)
    namespaces = util.array_to_list(repo.get_loaded_namespaces())

    if namespace in namespaces:
        loaded_version = repo.get_version(namespace)
        if loaded_version != version:
            raise ValueError('Namespace %s is already loaded with version %s' %
                             (namespace, loaded_version))

    if namespace in _versions and _versions[namespace] != version:
        raise ValueError('Namespace %s already requires version %s' %
                         (namespace, _versions[namespace]))

    version_glist = repo.enumerate_versions(namespace)
    available_versions = util.glist_to_list(version_glist, c_char_p)
    if not available_versions:
        raise ValueError('Namespace %s not available' % namespace)

    if version not in available_versions:
        raise ValueError('Namespace %s not available for version %s' %
                         (namespace, version))

    _versions[namespace] = version


def get_required_version(namespace):
    """Returns the version string for the namespace that was previously
    required through 'require_version' or None
    """

    global _versions

    return _versions.get(namespace, None)


def extract_namespace(fullname):
    for prefix in const.PREFIX:
        if fullname.startswith(prefix):
            return fullname[len(prefix) + 1:]


def install_import_hook():
    sys.meta_path.append(Importer())


class Importer(object):
    """Import hook according to http://www.python.org/dev/peps/pep-0302/"""

    def find_module(self, fullname, path):
        namespace = extract_namespace(fullname)
        if namespace:
            namespace = util.encode(namespace)
            if GIRepositoryPtr().enumerate_versions(namespace):
                return self

    @util.no_jit
    def load_module(self, fullname):
        global _versions

        namespace = util.encode(extract_namespace(fullname))
        repository = GIRepositoryPtr()

        if namespace in _versions:
            version = _versions[namespace]
        else:
            version = None

        # Dependency already loaded, skip
        if fullname in sys.modules:
            return sys.modules[fullname]

        error = GErrorPtr()
        repository.require(namespace, version, 0, byref(error))
        if error:
            try:
                raise ImportError(error.contents.message)
            finally:
                error.free()

        # No strictly needed here, but most things will fail during use
        library = repository.get_shared_library(namespace)
        if library:
            library = library.split(b",")[0]
            try:
                CDLL(library)
            except OSError:
                raise ImportError("Couldn't load shared library %r" % library)

        # Generate bindings, set up lazy attributes
        instance = module.Module(repository, namespace)
        instance.__path__ = repository.get_typelib_path(namespace)
        instance.__loader__ = self
        instance.__package__ = const.PREFIX[0]
        instance.__file__ = "<%s.%s>" % (const.PREFIX[0], namespace)
        instance._version = version or repository.get_version(namespace)

        # add to module and sys.modules
        for prefix in const.PREFIX:
            setattr(__import__(prefix, fromlist=[""]), namespace, instance)
            sys.modules[prefix + "." + namespace] = instance

        # Import a override module if available.
        overrides.load(namespace, instance)

        return instance
