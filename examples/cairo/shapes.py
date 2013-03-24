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


from gi.repository import Gtk


class cv(object):

    points = (
        ( 0, 85 ),
        ( 75, 75 ),
        ( 100, 10 ),
        ( 125, 75 ),
        ( 200, 85 ),
        ( 150, 125 ),
        ( 160, 190 ),
        ( 100, 150 ),
        ( 40, 190 ),
        ( 50, 125 ),
        ( 0, 85 )
    )


class Example(Gtk.Window):

    def __init__(self):
        super(Example, self).__init__()

        self.init_ui()


    def init_ui(self):

        darea = Gtk.DrawingArea()
        darea.connect("draw", self.on_draw)
        self.add(darea)

        self.set_title("Complex shapes")
        self.resize(460, 240)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.connect("delete-event", Gtk.main_quit)
        self.show_all()


    def on_draw(self, wid, cr):

        cr.set_source_rgb(0.6, 0.6, 0.6)
        cr.set_line_width(1)

        for i in range(10):
            cr.line_to(cv.points[i][0], cv.points[i][1])

        cr.fill()

        cr.move_to(240, 40)
        cr.line_to(240, 160)
        cr.line_to(350, 160)
        cr.fill()

        cr.move_to(380, 40)
        cr.line_to(380, 160)
        cr.line_to(450, 160)
        cr.curve_to(440, 155, 380, 145, 380, 40)
        cr.fill()


def main():

    app = Example()
    Gtk.main()


if __name__ == "__main__":
    main()
