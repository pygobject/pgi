# -*- coding: utf8 -*-
# taken from https://github.com/cubicool/clutter-pygobject-examples

import sys
sys.path.insert(0, '../..')
import pgi
pgi.install_as_gi()

import sys

from gi.repository import Clutter

RUNES = """
ᚠᛇᚻ᛫ᛒᛦᚦ᛫ᚠᚱᚩᚠᚢᚱ᛫ᚠᛁᚱᚪ᛫ᚷᛖᚻᚹᛦᛚᚳᚢᛗ
ᛋᚳᛖᚪᛚ᛫ᚦᛖᚪᚻ᛫ᛗᚪᚾᚾᚪ᛫ᚷᛖᚻᚹᛦᛚᚳ᛫ᛗᛁᚳᛚᚢᚾ᛫ᚻᛦᛏ᛫ᛞᚫᛚᚪᚾ
ᚷᛁᚠ᛫ᚻᛖ᛫ᚹᛁᛚᛖ᛫ᚠᚩᚱ᛫ᛞᚱᛁᚻᛏᚾᛖ᛫ᛞᚩᛗᛖᛋ᛫ᚻᛚᛇᛏᚪᚾ᛬
"""

if __name__ == "__main__":
    stage = Clutter.Stage()

    stage.set_color(Clutter.Color.from_string("#000000"))
    stage.set_size(1024, 768)
    stage.set_title("Text Editing")
    stage.connect("destroy", Clutter.main_quit)

    text = Clutter.Text("Mono Bold 24px", "", Clutter.Color.from_string("#33FF33"))

    text.set_position(40, 30)
    text.set_width(1024)
    text.set_line_wrap(True)
    text.set_reactive(True)
    text.set_editable(True)
    text.set_selectable(True)
    text.set_cursor_color(Clutter.Color.from_string("#FF33FF"))
    text.set_selected_text_color(Clutter.Color.from_string("#0000FF"))

    if len(sys.argv) >= 2:
        with open(sys.argv[1], "r") as c:
            contents = c.read()

        text.set_text(contents)
    
    else:
        text.set_text(RUNES)

    stage.add(text)
    stage.set_key_focus(text)
    stage.show_all()

    Clutter.main()

