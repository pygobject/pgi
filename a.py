# -*- coding: utf8 -*-
import sys

from pgi.repository import Gtk, Gdk, GObject
print "#"*80

color = Gdk.Color(10, 2, 3)
print repr(color)
#Gdk.Color.red._getter._code.pprint()
#Gdk.Color.red._setter._code.pprint()
print color.red
color.pixel = 3
print color.pixel

print Gdk.Event()

v = GObject.Value()
v.init(GObject.TYPE_INT)
v.set_int(3)

print [a for a in dir(v) if a.startswith("set_")]
