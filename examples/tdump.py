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
import json
import argparse
from collections import OrderedDict

from pgi.clib.gir import GITypelib, GIRepository, \
    GICallableInfo, GIBaseInfo, GIFunctionInfo, GIArgInfo, GIObjectInfo, \
    GIStructInfo, GIEnumInfo, GIInterfaceInfo, GIConstantInfo, GIUnionInfo, \
    GIValueInfo, GIFieldInfo, GISignalInfo, GIInfoType, GITypeInfo, \
    GICallbackInfo, GIVFuncInfo, GIRegisteredTypeInfo, GIPropertyInfo, \
    GITypeTag
from pgi._compat import print_, integer_types


def sort_infos(infos):
    return sorted(infos, key=lambda i: i.name)


def handle_list(infos, skip_abi=False):
    l = []
    for info in sort_infos(infos):
        obj = OrderedDict()
        handle(info, obj, skip_abi=skip_abi)
        l.append(obj)
    return l


def handle(info, obj, skip_abi=False, minimal=False):

    def show(name, value):
        if type(value) not in integer_types:
            value = str(value)
        obj[name] = value

    def showt(type_):
        obj["type"] = type_.__name__

    def sub(name, info, minimal=False):
        new = OrderedDict()
        obj[name] = new
        handle(info, new, skip_abi=skip_abi, minimal=minimal)

    def abi(value):
        if skip_abi:
            return "(SKIP_ABI)"
        return value

    def sublist(name, info, minimal=False):
        l = []
        obj[name] = l
        func = getattr(info, "get_%s" % name)
        for child in sort_infos(func()):
            new = OrderedDict()
            handle(child, new, skip_abi=skip_abi, minimal=minimal)
            l.append(new)

    if not info:
        return

    assert isinstance(info, GIBaseInfo)

    if int(info.type) != GIInfoType.TYPE:
        showt(GIBaseInfo)
        show("namespace", info.namespace)
        show("name", info.name)
        show("type", info.type)
        if minimal:
            return
        show("is_deprecated", info.is_deprecated)
        for name, value in sorted(info.iterate_attributes()):
            show("attribute", "%s=%s" % (name, value))

    if isinstance(info, GICallableInfo):
        showt(GICallableInfo)

        show("can_throw_gerror", info.can_throw_gerror)
        show("may_return_null", info.may_return_null)
        show("skip_return", info.skip_return)
        show("caller_owns", info.caller_owns)
        for name, value in sorted(info.iterate_return_attributes()):
            show("return_attribute", "%s=%s" % (name, value))
        sublist("args", info)
        sub("return_type", info.get_return_type())

        if isinstance(info, GIFunctionInfo):
            showt(GIFunctionInfo)
            show("flags", info.flags)
            show("symbol", info.symbol)
            # if isinstance(info.get_container(), GIInterfaceInfo):
            #     sub("property", info.get_property())
        elif isinstance(info, GICallbackInfo):
            showt(GICallbackInfo)
        elif isinstance(info, GISignalInfo):
            showt(GISignalInfo)
            show("flags", info.flags)
            show("true_stops_emit", info.true_stops_emit)
            sub("class_closure", info.get_class_closure())
        elif isinstance(info, GIVFuncInfo):
            showt(GIVFuncInfo)
            show("flags", info.flags)
            show("offset", abi(info.offset))
            sub("signal", info.get_signal())
            sub("invoker", info.get_invoker(), minimal=True)
        else:
            assert 0
    elif isinstance(info, GIRegisteredTypeInfo):
        showt(GIRegisteredTypeInfo)
        show("type_name", info.type_name)
        show("type_init ", info.type_init)

        if isinstance(info, GIEnumInfo):
            showt(GIEnumInfo)
            show("storage_type ", info.storage_type)
            sublist("values", info)
            show("error_domain", info.error_domain)
        elif isinstance(info, GIInterfaceInfo):
            showt(GIInterfaceInfo)
            sub("iface_struct", info.get_iface_struct())
            sublist("prerequisites", info, minimal=True)
            sublist("properties", info)
            sublist("methods", info)
            sublist("signals", info)
            sublist("vfuncs", info)
            sublist("constants", info)
        elif isinstance(info, GIObjectInfo):
            showt(GIObjectInfo)
            show("abstract", info.abstract)
            show("fundamental", info.fundamental)
            show("type_name", info.type_name)
            show("type_init", info.type_init)
            sublist("constants", info)
            sublist("fields", info)
            sublist("interfaces", info)
            sublist("methods", info)
            sublist("properties", info)
            sublist("signals", info)
            sublist("vfuncs", info)
            sub("class_struct", info.get_class_struct())
            show("ref_function", info.ref_function)
            show("unref_function", info.unref_function)
            show("set_value_function", info.set_value_function)
            show("get_value_function ", info.get_value_function)
        elif isinstance(info, GIStructInfo):
            showt(GIStructInfo)
            show("size", abi(info.size))
            show("alignment", abi(info.alignment))
            show("is_gtype_struct", info.is_gtype_struct)
            show("is_foreign", info.is_foreign)
            sublist("fields", info)
            sublist("methods", info)
        elif isinstance(info, GIUnionInfo):
            showt(GIUnionInfo)
            show("size", abi(info.size))
            show("alignment", abi(info.alignment))
            show("is_discriminated", info.is_discriminated)
            show("discriminator_offset", info.discriminator_offset)
            sub("discriminator_type", info.get_discriminator_type())
            sublist("fields", info)
            sublist("methods", info)
        else:
            assert 0
    elif isinstance(info, GIArgInfo):
        showt(GIArgInfo)
        show("closure", info.closure)
        show("destroy", info.destroy)
        show("direction", info.direction)
        show("ownership_transfer", info.ownership_transfer)
        show("scope", info.scope)
        sub("type", info.get_type())
        show("may_be_null", info.may_be_null)
        show("is_caller_allocates", info.is_caller_allocates)
        show("is_optional", info.is_optional)
        show("is_return_value", info.is_return_value)
        show("is_skip", info.is_skip)
    elif isinstance(info, GIConstantInfo):
        showt(GIConstantInfo)
        sub("type", info.get_type())
    elif isinstance(info, GIFieldInfo):
        showt(GIFieldInfo)
        show("flags", info.flags)
        show("offset", abi(info.offset))
        show("size", abi(info.size))
        sub("type", info.get_type())
    elif isinstance(info, GIPropertyInfo):
        showt(GIPropertyInfo)
        show("flags", info.flags)
        show("ownership_transfer", info.ownership_transfer)
        sub("type", info.get_type())
    elif isinstance(info, GITypeInfo):
        showt(GITypeInfo)
        show("is_pointer", info.is_pointer)
        show("tag", info.tag)
        sub("interface", info.get_interface(), minimal=True)
        show("array_length", info.array_length)
        show("array_fixed_size", info.array_fixed_size)
        show("is_zero_terminated", info.is_zero_terminated)
        if int(info.tag) == GITypeTag.ARRAY:
            show("array_type", info.array_type)
    elif isinstance(info, GIValueInfo):
        showt(GIValueInfo)
        show("value", info.value_)
    else:
        assert 0, info.type


def get_dump(typelib_path, skip_abi):
    with open(typelib_path, "rb") as h:
        data = h.read()

    typelib = GITypelib.new_from_memory(data)
    repo = GIRepository.get_default()
    namespace = repo.load_typelib(typelib, 0)
    infos = repo.get_infos(namespace)
    l = handle_list(infos, skip_abi=skip_abi)
    return json.dumps(l, indent=2)


def main(argv):
    parser = argparse.ArgumentParser(
        description='Dump typelibs')
    parser.add_argument('typelib', help='Path to typelib')
    parser.add_argument('--skip-abi', action='store_true',
                        help='Don\'t print info depending on the C ABI')
    args = parser.parse_args(argv[1:])

    print_(get_dump(args.typelib, args.skip_abi))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
