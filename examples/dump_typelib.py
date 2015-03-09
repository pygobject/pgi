#!/usr/bin/python
# Copyright 2015 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

import sys
import argparse

from pgi.clib.gir import GITypelib, GIRepository, GIRepositoryLoadFlags, \
    GICallableInfo, GIBaseInfo, GIFunctionInfo, GIArgInfo
from pgi._compat import print_


def handle(info, indent=-1):
    # TODO: this is far from complete

    def show(name, value=""):
        print_("   " * indent + name, value)

    assert isinstance(info, GIBaseInfo)
    indent += 1
    show("type", "GIBaseInfo")
    show("name", info.name)

    if isinstance(info, GICallableInfo):
        indent += 1
        show("type", "GICallableInfo")
        show("may_return_null",  info.may_return_null)

        if isinstance(info, GIFunctionInfo):
            indent += 1
            show("type", "GIFunctionInfo")
            show("flags", info.flags)
            show("symbol", info.symbol)
            show("args:")
            for arg in info.get_args():
                handle(arg, indent)
    elif isinstance(info, GIArgInfo):
        indent += 1
        show("type", "GIArgInfo")
        show("direction", info.direction)
        show("ownership_transfer", info.ownership_transfer)


def main(argv):
    parser = argparse.ArgumentParser(
        description='Dump typelibs')
    parser.add_argument('typelib', help='Pyth to typelib')
    args = parser.parse_args(argv[1:])

    with open(args.typelib, "rb") as h:
        data = h.read()

    typelib = GITypelib.new_from_memory(data)
    repo = GIRepository.get_default()
    namespace = repo.load_typelib(typelib, 0)
    for info in repo.get_infos(namespace):
        handle(info)


if __name__== "__main__":
    sys.exit(main(sys.argv))
