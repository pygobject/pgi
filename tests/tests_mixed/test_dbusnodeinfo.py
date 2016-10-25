# Copyright 2016 Linus Lewandowski
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

import unittest

from gi.repository import Gio

xml = """<node>
    <interface name='net.lvht.Foo1'>
        <method name='HelloWorld'>
            <arg type='s' name='a' direction='in'/>
            <arg type='i' name='b' direction='in'/>
            <arg type='s' name='response' direction='out'/>
        </method>
    </interface>
</node>"""


class DBusNodeInfoTest(unittest.TestCase):

    def test_interfaces(self):
        ni = Gio.DBusNodeInfo.new_for_xml(xml)
        assert(isinstance(ni, Gio.DBusNodeInfo))
        interface = ni.lookup_interface("net.lvht.Foo1")
        assert(isinstance(interface, Gio.DBusInterfaceInfo))
        assert(len(ni.interfaces) == 1)
        #assert(ni.interfaces[0] == interface)
        assert(ni.interfaces[0].name == interface.name)
