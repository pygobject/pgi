#!/usr/bin/python

'''
ZetCode PyCairo tutorial

This code example draws another
three shapes in PyCairo.

author: Jan Bodnar
website: zetcode.com
last edited: August 2012
'''

import sys
sys.path.insert(0, '../..')
import pgi
pgi.install_as_gi()
import cairocffi
cairocffi.install_as_pycairo()


from gi.repository import Gtk
import cairo


class Example(Gtk.Window):

    def __init__(self):
        super(Example, self).__init__()

        self.init_ui()


    def init_ui(self):

        darea = Gtk.DrawingArea()
        darea.connect("draw", self.on_draw)
        self.add(darea)

        self.set_title("Text filled with gradient")
        self.resize(460, 240)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.connect("delete-event", Gtk.main_quit)
        self.show_all()


    def on_draw(self, wid, cr):
        cr.set_source_rgb(0.2, 0.2, 0.2)
        cr.paint()

        h = 90

        cr.select_font_face("Serif", cairo.FONT_SLANT_ITALIC,
            cairo.FONT_WEIGHT_BOLD)
        cr.set_font_size(h)

        lg = cairo.LinearGradient(0, 15, 0, h*0.8)
        lg.set_extend(cairo.EXTEND_REPEAT)
        lg.add_color_stop_rgb(0.0, 1, 0.6, 0)
        lg.add_color_stop_rgb(0.5, 1, 0.3, 0)

        cr.move_to(15, 80)
        cr.text_path("ZetCode")
        cr.set_source(lg)
        cr.fill()


def main():

    app = Example()
    Gtk.main()


if __name__ == "__main__":
    main()
