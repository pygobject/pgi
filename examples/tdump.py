#!/usr/bin/python
# Copyright 2015 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

"""
Utility to print the content of a GObject Introspection typelib file in a 
diff friendly fashion.

Can be used for looking things up in the typelib, or compare two different
typelibs.

The --skip-abi flag can be used to compare typelibs for different 
architectures / compiler versions.
"""

import sys
import argparse

from pgi.cffilib.gir import GITypelib, GIRepository, GIRepositoryLoadFlags, \
    GICallableInfo, GIBaseInfo, GIFunctionInfo, GIArgInfo, GIObjectInfo, \
    GIStructInfo, GIEnumInfo, GIInterfaceInfo, GIConstantInfo, GIUnionInfo, \
    GIValueInfo, GIFieldInfo, GISignalInfo, GIInfoType, GITypeInfo
from pgi._compat import print_, StringIO


def sort_infos(infos):
    return sorted(infos, key=lambda i: i.name)


def handle(info, indent=-1, file_=None, skip_abi=False):
    # TODO: this is far from complete

    def show(name, *values):
        print_("   " * indent + name, *values, file=file_)

    def showt(type_):
        show("[%s]" % type_.__name__)

    def sub(info):
        handle(info, indent=indent, file_=file_, skip_abi=skip_abi)

    def abi(value):
        if skip_abi:
            return "<SKIP_ABI>"
        return value

    assert isinstance(info, GIBaseInfo)
    indent += 1
    file_.write("\n")
    showt(GIBaseInfo)
    if int(info.type) == GIInfoType.TYPE:
        show("name")
    else:
        show("name", info.name)

    show("is_deprecated", info.is_deprecated)
    for name, value in sorted(info.iterate_attributes()):
        show("attribute", "%s=%s" % (name, value))

    if isinstance(info, GICallableInfo):
        indent += 1
        showt(GICallableInfo)
        show("may_return_null", info.may_return_null)
        show("return_type:")
        sub(info.get_return_type())
        for name, value in sorted(info.iterate_return_attributes()):
            show("return_attribute", "%s=%s" % (name, value))

        if isinstance(info, GIFunctionInfo):
            indent += 1
            showt(GIFunctionInfo)
            show("flags", info.flags)
            show("symbol", info.symbol)
            show("can_throw_gerror", info.can_throw_gerror)
            show("caller_owns", info.caller_owns)
            show("args:")
            for arg in sort_infos(info.get_args()):
                sub(arg)
        elif isinstance(info, GISignalInfo):
            indent += 1
            showt(GISignalInfo)
            show("flags", info.flags)
            show("true_stops_emit", info.true_stops_emit)
    elif isinstance(info, GIArgInfo):
        indent += 1
        showt(GIArgInfo)
        show("direction", info.direction)
        show("ownership_transfer", info.ownership_transfer)
    elif isinstance(info, GIObjectInfo):
        indent += 1
        showt(GIObjectInfo)
        show("abstract", info.abstract)
        show("fundamental", info.fundamental)
        show("type_name", info.type_name)
        show("type_init", info.type_init)
        for signal in sort_infos(info.get_signals()):
            sub(signal)
    elif isinstance(info, GIStructInfo):
        indent += 1
        showt(GIStructInfo)
        show("size", abi(info.size))
        show("alignment", abi(info.alignment))
        show("is_gtype_struct", info.is_gtype_struct)
        show("is_foreign", info.is_foreign)
        show("fields:")
        for field in sort_infos(info.get_fields()):
            sub(field)
    elif isinstance(info, GIEnumInfo):
        indent += 1
        showt(GIEnumInfo)
        show("storage_type ", info.storage_type)
        show("values:")
        for value in sort_infos(info.get_values()):
            sub(value)
    elif isinstance(info, GIInterfaceInfo):
        indent += 1
        showt(GIInterfaceInfo)
    elif isinstance(info, GIConstantInfo):
        indent += 1
        showt(GIConstantInfo)
    elif isinstance(info, GIUnionInfo):
        indent += 1
        showt(GIUnionInfo)
        show("size", abi(info.size))
        show("alignment", abi(info.alignment))
        show("fields:")
        for field in sort_infos(info.get_fields()):
            sub(field)
    elif isinstance(info, GIValueInfo):
        indent += 1
        showt(GIValueInfo)
        show("value", info.value_)
    elif isinstance(info, GIFieldInfo):
        indent += 1
        showt(GIFieldInfo)
        show("flags", info.flags)
        show("offset", abi(info.offset))
        show("size", abi(info.size))
    elif isinstance(info, GITypeInfo):
        indent += 1
        showt(GITypeInfo)
        #~ show("is_pointer", info.is_pointer)
        #~ show("tag", info.tag)
    else:
        assert 0, info.type


def get_dump(typelib_path, skip_abi):
    with open(typelib_path, "rb") as h:
        data = h.read()
    file_ = StringIO()
    typelib = GITypelib.new_from_memory(data)
    repo = GIRepository.get_default()
    namespace = repo.load_typelib(typelib, 0)
    for info in sort_infos(repo.get_infos(namespace)):
        handle(info, file_=file_, skip_abi=skip_abi)
    return file_.getvalue()



def main(argv):
    parser = argparse.ArgumentParser(
        description='Dump typelibs')
    parser.add_argument('typelib', help='Path to typelib')
    parser.add_argument('--skip-abi', action='store_true',
                        help='Don\'t print info depending on the C ABI')
    args = parser.parse_args(argv[1:])

    print_(get_dump(args.typelib, args.skip_abi))
    return 0


if __name__== "__main__":
    sys.exit(main(sys.argv))
