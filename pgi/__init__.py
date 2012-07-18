# Copyright 2012 Christoph Reiter
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

from ctypes import c_char_p
from gitypes import GIRepositoryPtr, gi_init
from const import VERSION as version
import util
from importer import _versions

version = version

gi_init()

def require_version(namespace, version):
    """Set a version for the namespace to be loaded.
    This needs to be called before importing the namespace or any
    namespace that depends on it."""
    global _versions

    repo = GIRepositoryPtr()

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
    required through 'require_version' or None"""
    global _versions

    return _versions.get(namespace, None)
