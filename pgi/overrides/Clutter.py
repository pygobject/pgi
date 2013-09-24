# -*- Mode: Python; py-indent-offset: 4 -*-
# vim: tabstop=4 shiftwidth=4 expandtab
#
# Copyright (C) 2009 Johan Dahlin <johan@gnome.org>
#               2010 Simon van der Linden <svdlinden@src.gnome.org>
#               2011 Bastian Winkler <buz@netbuz.org>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301
# USA

import sys
from contextlib import contextmanager

from pgi.repository import GObject
from pgi.overrides import override, get_introspection_module


Clutter = get_introspection_module('Clutter')

__all__ = []


if sys.version_info >= (3, 0):
    _basestring = str
    _callable = lambda c: hasattr(c, '__call__')
else:
    _basestring = basestring
    _callable = callable


clutter_version = (Clutter.MAJOR_VERSION, Clutter.MINOR_VERSION,
                   Clutter.MICRO_VERSION)
__all__.append('clutter_version')


def _gvalue_from_python(value_type, v):
    # XXX: A similar function is also in Gtk.py, but IMHO this should
    # live in a GObject.Value override. Either as a GValue classmethod
    # or the GValue constructor.
    value = GObject.Value()
    value.init(value_type)
    if value_type == GObject.TYPE_INT:
        value.set_int(int(v))
    elif value_type == GObject.TYPE_UINT:
        value.set_uint(int(v))
    elif value_type == GObject.TYPE_CHAR:
        value.set_char(int(v))
    elif value_type == GObject.TYPE_UCHAR:
        value.set_uint(int(v))
    elif value_type == GObject.TYPE_FLOAT:
        value.set_float(float(v))
    elif value_type == GObject.TYPE_DOUBLE:
        value.set_double(float(v))
    elif value_type == GObject.TYPE_LONG:
        value.set_long(long(v))
    elif value_type == GObject.TYPE_ULONG:
        value.set_ulong(long(v))
    elif value_type == GObject.TYPE_INT64:
        value.set_int64(long(v))
    elif value_type == GObject.TYPE_UINT64:
        value.set_uint64(long(v))
    elif value_type == GObject.TYPE_BOOLEAN:
        value.set_boolean(bool(v))
    elif value_type == GObject.TYPE_STRING:
        if isinstance(v, str):
            v = str(v)
        elif sys.version_info < (3, 0):
            if isinstance(v, unicode):
                v = v.encode('UTF-8')
            else:
                raise ValueError("Expected string or unicode " \
                        "but got %s%s" % (v, type(v)))
        else:
            raise ValueError("Expected string or unicode " \
                    "but got %s%s" % (v, type(v)))
        value.set_string(str(v))
    else:
        return v
    return value


class Color(Clutter.Color):
    def __new__(cls, *args, **kwargs):
        return Clutter.Color.__new__(cls)

    def __init__(self, red=0, green=0, blue=0, alpha=0):
        Clutter.Color.__init__(self)
        self.red = red
        self.green = green
        self.blue = blue
        self.alpha = alpha

    def __repr__(self):
        return '<Clutter.Color(red=%d, green=%d, blue=%d, alpha=%s)>' % (
            self.red, self.green, self.blue, self.alpha)

    def __len__(self):
        return 4

    def __getitem__(self, key):
        if isinstance(key, int):
            if key == 0:
                return self.red
            elif key == 1:
                return self.green
            elif key == 2:
                return self.blue
            elif key == 3:
                return self.alpha
            else:
                raise IndexError("index out of range")
        else:
            raise TypeError("sequence index must be integer")

    def __setitem__(self, key, value):
        if isinstance(key, int):
            if key == 0:
                self.red = value
            elif key == 1:
                self.green = value
            elif key == 2:
                self.blue = value
            elif key == 3:
                self.alpha = value
            else:
                raise IndexError("index out of range")
        else:
            raise TypeError("sequence index must be integer")

    def __eq__(self, other):
        return self.red == other.red and self.green == other.green and \
                self.blue == other.blue and self.alpha == other.alpha

    def __ne__(self, other):
        return self.red != other.red or self.green != other.green or \
                self.blue != other.blue or self.alpha != other.alpha

    @classmethod
    def from_string(cls, string):
        ok, instance = Clutter.Color.from_string(string)
        if ok:
            return instance

    @classmethod
    def from_hls(cls, hue, luminance, saturation):
        self = cls()
        Clutter.Color.from_hls(self, hue, luminance, saturation)
        return self

    @classmethod
    def from_pixel(cls, pixel):
        self = cls()
        Clutter.Color.from_pixel(self, pixel)
        return self

Color = override(Color)
__all__.append('Color')


class ActorBox(Clutter.ActorBox):
    def __new__(cls, *args, **kwargs):
        return Clutter.ActorBox.__new__(cls)

    def __init__(self, x1=0.0, y1=0.0, x2=0.0, y2=0.0):
        Clutter.ActorBox.__init__(self)
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def __repr__(self):
        return '<Clutter.ActorBox(x1=%f, y1=%f, x2=%f y2=%f)>' % (
            self.x1, self.y1, self.x2, self.y2)

    def __len__(self):
        return 4

    def __getitem__(self, key):
        if isinstance(key, int):
            if key == 0:
                return self.x1
            elif key == 1:
                return self.y1
            elif key == 2:
                return self.x2
            elif key == 3:
                return self.y2
            else:
                raise IndexError("index out of range")
        else:
            raise TypeError("sequence index must be integer")

    def __setitem__(self, key, value):
        if isinstance(key, int):
            if key == 0:
                self.x1 = value
            elif key == 1:
                self.y1 = value
            elif key == 2:
                self.x2 = value
            elif key == 3:
                self.y2 = value
            else:
                raise IndexError("index out of range")
        else:
            raise TypeError("sequence index must be integer")

    def __eq__(self, other):
        if isinstance(other, list):
            return list(self) == other
        elif isinstance(other, tuple):
            return tuple(self) == other
        elif isinstance(other, ActorBox):
            return self.equal(other)
        return False

    def __ne__(self, other):
        if isinstance(other, list):
            return list(self) != other
        elif isinstance(other, tuple):
            return tuple(self) != other
        elif isinstance(other, ActorBox):
            return self.equal(other)
        return False

    x = property(Clutter.ActorBox.get_x)

    y = property(Clutter.ActorBox.get_y)

    @property
    def size(self):
        return (self.x2 - self.x1, self.y2 - self.y1)

    @property
    def width(self):
        return self.x2 - self.x1

    @property
    def height(self):
        return self.y2 - self.y1

ActorBox = override(ActorBox)
__all__.append('ActorBox')


class Vertex(Clutter.Vertex):
    def __new__(cls, *args, **kwargs):
        return Clutter.Vertex.__new__(cls)

    def __init__(self, x=0.0, y=0.0, z=0.0):
        Clutter.Vertex.__init__(self)
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return '<Clutter.Vertex(x=%f, y=%f, z=%f)>' % (self.x, self.y, self.z)

    def __len__(self):
        return 3

    def __getitem__(self, key):
        if isinstance(key, int):
            if key == 0:
                return self.x
            elif key == 1:
                return self.y
            elif key == 2:
                return self.z
            else:
                raise IndexError("index out of range")
        else:
            raise TypeError("sequence index must be integer")

    def __setitem__(self, key, value):
        if isinstance(key, int):
            if key == 0:
                self.x = value
            elif key == 1:
                self.y = value
            elif key == 2:
                self.y = value
            else:
                raise IndexError("index out of range")
        else:
            raise TypeError("sequence index must be integer")

    def __eq__(self, other):
        if isinstance(other, list):
            return list(self) == other
        elif isinstance(other, tuple):
            return tuple(self) == other
        elif isinstance(other, Vertex):
            return self.equal(other)
        return False

    def __ne__(self, other):
        if isinstance(other, list):
            return list(self) != other
        elif isinstance(other, tuple):
            return tuple(self) != other
        elif isinstance(other, Vertex):
            return not self.equal(other)
        return False

Vertex = override(Vertex)
__all__.append('Vertex')


class Geometry(Clutter.Geometry):
    def __new__(cls, *args, **kwargs):
        return Clutter.Geometry.__new__(cls)

    def __init__(self, x=0, y=0, width=0, height=0):
        Clutter.Geometry.__init__(self)
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def __repr__(self):
        return '<Clutter.Geometry(x=%d, y=%d, width=%d, height=%d)>' % (
            self.x, self.y, self.width, self.height)

    def __len__(self):
        return 4

    def __getitem__(self, key):
        if isinstance(key, int):
            if key == 0:
                return self.x
            elif key == 1:
                return self.y
            elif key == 2:
                return self.width
            elif key == 3:
                return self.height
            else:
                raise IndexError("index out of range")
        else:
            raise TypeError("sequence index must be integer")

    def __setitem__(self, key, value):
        if isinstance(key, int):
            if key == 0:
                self.x = value
            elif key == 1:
                self.y = value
            elif key == 2:
                self.width = value
            elif key == 3:
                self.height = value
            else:
                raise IndexError("index out of range")
        else:
            raise TypeError("sequence index must be integer")

    def __eq__(self, other):
        if isinstance(other, list):
            return list(self) == other
        elif isinstance(other, tuple):
            return tuple(self) == other
        elif isinstance(other, Geometry):
            return (self.x == other.x and self.y == other.y and
                    self.width == other.width and self.height == other.height)
        else:
            return False

    def __ne__(self, other):
        return self.x != other.x or self.y != other.y or \
                self.width != other.width or self.height != other.height

Geometry = override(Geometry)
__all__.append('Geometry')


class Knot(Clutter.Knot):
    def __new__(cls, *args, **kwargs):
        return Clutter.Knot.__new__(cls)

    def __init__(self, x=0, y=0):
        Clutter.Knot.__init__(self)
        self.x = x
        self.y = y

    def __repr__(self):
        return '<Clutter.Knot(x=%d, y=%d)>' % (self.x, self.y)

    def __len__(self):
        return 2

    def __getitem__(self, key):
        if isinstance(key, int):
            if key == 0:
                return self.x
            elif key == 1:
                return self.y
            else:
                raise IndexError("index out of range")
        else:
            raise TypeError("sequence index must be integer")

    def __setitem__(self, key, value):
        if isinstance(key, int):
            if key == 0:
                self.x = value
            elif key == 1:
                self.y = value
            else:
                raise IndexError("index out of range")
        else:
            raise TypeError("sequence index must be integer")

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return self.x != other.x or self.y != other.y

Knot = override(Knot)
__all__.append('Knot')


class Event(Clutter.Event):
    _UNION_MEMBERS = {
        Clutter.EventType.KEY_PRESS: 'key',
        Clutter.EventType.KEY_RELEASE: 'key',
        Clutter.EventType.MOTION: 'motion',
        Clutter.EventType.ENTER: 'crossing',
        Clutter.EventType.LEAVE: 'crossing',
        Clutter.EventType.BUTTON_PRESS: 'button',
        Clutter.EventType.BUTTON_RELEASE: 'button',
        Clutter.EventType.SCROLL: 'scroll',
        Clutter.EventType.STAGE_STATE: 'stage_state'
    }
    if clutter_version >= (1, 10, 0):
        _UNION_MEMBERS.update({
            Clutter.EventType.TOUCH_BEGIN: 'touch',
            Clutter.EventType.TOUCH_END: 'touch',
            Clutter.EventType.TOUCH_UPDATE: 'touch',
            Clutter.EventType.TOUCH_CANCEL: 'touch'
        })

    def __new__(cls, *args, **kwargs):
        return Clutter.Event.__new__(cls)

    def __getattr__(self, name):
        real_event = getattr(self, '_UNION_MEMBERS').get(self.type())
        if real_event:
            return getattr(getattr(self, real_event), name)
        else:
            raise AttributeError("'%s' object has no attribute '%s'" %
                                 (self.__class__.__name__, name))

    def __str__(self):
        def get_key():
            from gi.overrides import keysyms
            for name in dir(keysyms):
                if self.keyval == getattr(keysyms, name):
                    return name
            if sys.version_info < (3, 0):
                return unichr(self.get_key_unicode()).encode('UTF-8')
            else:
                return chr(self.get_key_unicode())

        def actor_name(actor):
            if not actor:
                return 'None'
            if actor.get_name():
                return actor.get_name()
            return actor.__class__.__name__

        def get_state():
            if self.get_state():
                return 'modifier: %s; ' % str(self.get_state())
            return ''

        if self.type() == Clutter.EventType.BUTTON_PRESS:
            return ('<Button Press at (%d,%d); button: %d; count: %d; %s' +
                    'time: %d; source: %s>') % (self.button.x, self.button.y,
                            self.button.button, self.button.click_count,
                            get_state(), self.get_time(),
                            actor_name(self.get_source()))
        elif self.type() == Clutter.EventType.BUTTON_RELEASE:
            return ('<Button Release at (%d,%d); button: %d; count: %d; %s' +
                    'time: i%d; source: %s>') % (self.button.x, self.button.y,
                            self.button.button, self.button.click_count,
                            get_state(), self.get_time(),
                            actor_name(self.get_source()))
        elif self.type() == Clutter.EventType.KEY_PRESS:
            return "<Key Press '%s'; %stime: %d; source %s>" % (
                    get_key(), get_state(), self.get_time(),
                    actor_name(self.get_source()))
        elif self.type() == Clutter.EventType.KEY_RELEASE:
            return "<Key Release '%s'; %stime: %d; source %s>" % (
                    get_key(), get_state(), self.get_time(),
                    actor_name(self.get_source()))
        elif self.type() == Clutter.EventType.MOTION:
            return "<Motion at (%d,%d); time: %d; source %s>" % (
                    self.motion.x, self.motion.y, self.get_time(),
                    actor_name(self.get_source()))
        elif self.type() == Clutter.EventType.ENTER:
            return "<Entering actor %s related to actor %s; time %d>" % (
                    actor_name(self.get_source()),
                    actor_name(self.get_related()), self.get_time())
        elif self.type() == Clutter.EventType.LEAVE:
            return "<Leaving actor %s related to actor %s; time %d>" % (
                    actor_name(self.get_source()),
                    actor_name(self.get_related()), self.get_time())
        elif self.type() == Clutter.EventType.SCROLL:
            return ("<Scroll %d at (%d,%d); modifier: %s; time: %d; " +
                    "source: %s>") % (self.scroll.direction.value_nick,
                            self.scroll.x, self.scroll.y, self.get_time(),
                            actor_name(self.get_source()))
        elif self.type() == Clutter.EventType.STAGE_STATE:
            return '<Stage state %s on %s>' % (self.get_flags(),
                    actor_name(self.get_stage()))
        elif self.type() == Clutter.EventType.NOTHING:
            return '<Nothing>'
        elif clutter_version >= (1, 10, 0) and \
                self.type() == Clutter.EventType.TOUCH_BEGIN:
            return ('<TouchBegin at (%d,%d); sequence: %s; modifier: %s; ' +
                    'time: %d; source: %s>') % (self.touch.x, self.touch.y,
                        str(self.touch.sequence), self.get_time(),
                        actor_name(self.get_source()))
        elif clutter_version >= (1, 10, 0) and \
                self.type() == Clutter.EventType.TOUCH_UPDATE:
            return ('<TouchUpdate at (%d,%d); sequence: %s; modifier: %s; ' +
                    'time: %d; source: %s>') % (self.touch.x, self.touch.y,
                        str(self.touch.sequence), self.get_time(),
                        actor_name(self.get_source()))
        elif clutter_version >= (1, 10, 0) and \
                self.type() == Clutter.EventType.TOUCH_END:
            return ('<TouchEnd at (%d,%d); sequence: %s; modifier: %s; ' +
                    'time: %d; source: %s>') % (self.touch.x, self.touch.y,
                        str(self.touch.sequence), self.get_time(),
                        actor_name(self.get_source()))
        elif clutter_version >= (1, 10, 0) and \
                self.type() == Clutter.EventType.TOUCH_CANCEL:
            return ('<TouchCancel at (%d,%d); sequence: %s; modifier: %s; ' +
                    'time: %d; source: %s>') % (self.touch.x, self.touch.y,
                        str(self.touch.sequence), self.get_time(),
                        actor_name(self.get_source()))
        else:
            return '<Unkown event>'


Event = override(Event)
__all__.append('Event')


class Actor(Clutter.Actor):
    def _update_animation(self, *args, **kwargs):
        def _detach_animation(animation):
            delattr(self, '_animation')
            del animation

        # check if we already have a running animation
        if hasattr(self, '_animation'):
            animation = getattr(self, '_animation')
        else:
            animation = Clutter.Animation()
            animation.set_object(self)
            animation.connect('completed', _detach_animation)
            setattr(self, '_animation', animation)

        # check arguments
        if len(args) == 1 and isinstance(args[0], dict):
            properties = args[0].items()
        elif len(args) == 2 and isinstance(args[0], (tuple, list)) and \
                isinstance(args[1], (tuple, list)):
            properties = zip(args[0], args[1])
        elif len(args) >= 2 and not 2 % 2:
            properties = zip(args[::2], args[1::2])
        elif kwargs:
            properties = kwargs.items()
        else:
            raise TypeError('The arguments must be: ' +
                    '"property", value, "property", value, ... or ' +
                    '("property", "property", ...), (value, value, ...) ' +
                    'or {"property": value, "property", value}')

        for prop, value in properties:
            pspec = getattr(self.__class__.props, prop)
            value = _gvalue_from_python(pspec.value_type, value)
            if not isinstance(prop, str):
                raise TypeError('A property must be a string, got %s' %
                        type(prop))
            elif prop.startswith("fixed::"):
                prop = prop[7:]
                self.set_property(prop, value)
            elif animation.has_property(prop):
                animation.update(prop, value)
            else:
                animation.bind(prop, value)
        return animation

    def animate(self, mode, duration, *args, **kwargs):
        """
        The animate() method is a convenience method to create or update a
        Clutter.Animation. The animation properties can be specified in
        multiple ways:

        Property/value pairs
        >>> actor.animate(Clutter.AnimationMode.LINEAR, 1000,
        ...     "x", 200.0, "y", 200.0)

        A keyword list
        >>> actor.animate(Clutter.AnimationMode.LINEAR, 1000,
        ...     x=200.0, y=200.0)

        A tuple with properties and a tuple with values
        >>> actor.animate(Clutter.AnimationMode.LINEAR, 1000,
        ...     ("x", "y"), (200.0, 200.0))

        A single dictionary
        >>> actor.animate(Clutter.ANimationMode.LINEAR, 1000,
        ...     {"x": 200.0, "y", 200.0})
        """
        animation = self._update_animation(*args, **kwargs)
        animation.set_mode(mode)
        animation.set_duration(duration)
        animation.get_timeline().start()
        return animation

    def animate_with_timeline(self, mode, timeline, *args, **kwargs):
        animation = self._update_animation(*args, **kwargs)
        animation.set_mode(mode)
        animation.set_timeline(timeline)
        animation.get_timeline().start()
        return animation

    def animate_with_alpha(self, alpha, *args, **kwargs):
        animation = self._update_animation(*args, **kwargs)
        animation.set_alpha(alpha)
        animation.get_timeline().start()
        return animation

    def raise_actor(self, below):
        parent = self.get_parent()
        if not parent:
            return
        parent.raise_child(self, below)

    def lower_actor(self, above):
        parent = self.get_parent()
        if not parent:
            return
        parent.lower_child(self, above)

    def transform_stage_point(self, x, y):
        success, x_out, y_out = super(Actor, self).transform_stage_point(x, y)
        if success:
            return (x_out, y_out)

    def get_paint_box(self):
        success, box = super(Actor, self).get_paint_box()
        if success:
            return box

    if clutter_version >= (1, 10, 0):
        def __iter__(self):
            return iter(self.get_children())

        @contextmanager
        def easing_state(self, duration=None, mode=None, delay=None):
            """
            @duration: The optional easing duration in ms
            @mode: The optional easing mode
            @delay: An optional delay in ms

            The easing_state() method allows a simple usage of Clutters
            implicit animation API using a Python contextmanager.

            To set an actors position to 100,100 and move it to 200,200 in 2s
            using a linear animation you can call:
            >>> my_actor.set_position(100, 100)
            >>> with my_actor.easing_state(2000, Clutter.AnimationMode.LINEAR):
            ...     my_actor.set_position(200, 200)

            Instead of:
            >>> my_actor.set_position(100, 100)
            >>> my_actor.save_easing_state()
            >>> my_actor.set_easing_duration(2000)
            >>> my_actor.set_easing_mode(Clutter.AnimationMode.LINEAR)
            >>> my_actor.set_position(200, 200)
            >>> my_actor.restore_easing_state()
            """
            self.save_easing_state()
            if duration is not None:
                self.set_easing_duration(duration)
            if mode is not None:
                self.set_easing_mode(mode)
            if delay is not None:
                self.set_easing_delay(delay)
            yield
            self.restore_easing_state()

Actor = override(Actor)
__all__.append('Actor')


class Container(Clutter.Container):
    def __len__(self):
        return len(self.get_children())

    def __bool__(self):
        return True

    # alias for Python 2.x object protocol
    __nonzero__ = __bool__

    def __contains__(self, actor):
        return actor in self.get_children()

    def __iter__(self):
        return iter(self.get_children())

    def __getitem__(self, key):
        children = self.get_children()
        n_children = len(children)
        if isinstance(key, int):
            if key < 0:
                key += n_children
            if key < 0 or key >= n_children:
                raise IndexError("index out of range: %d" % key)
            return children[key]
        elif isinstance(key, slice):
            start, stop, step = key.indices(n_children)
            ret = []
            for i in range(start, stop, step):
                ret.append(children[i])
            return ret
        else:
            raise TypeError("indices must be integer or slice")

    def __setitem__(self, key, value):
        children = self.get_children()
        n_children = len(children)
        if isinstance(key, int):
            if key < 0:
                key += n_children
            if key >= n_children:
                raise IndexError("index out of range: %d" % key)
            old = children[key]
            if key < n_children:
                silbing = children[key + 1]
            else:
                silbing = None
            self.remove(old)
            self.add(value)
            if silbing:
                self.lower_child(value, silbing)
        else:
            raise TypeError("indices must be integer")

    def add(self, *actors):
        for actor in actors:
            Clutter.Container.add_actor(self, actor)

    def remove(self, *actors):
        for actor in actors:
            Clutter.Container.remove_actor(self, actor)

    def child_get_property(self, child, property_name):
        meta = self.get_child_meta(child)
        return meta.get_property(property_name)

    def child_set_property(self, child, property_name, value):
        meta = self.get_child_meta(child)
        meta.set_property(property_name, value)

Container = override(Container)
__all__.append('Container')


class Texture(Clutter.Texture, Actor):
    def __init__(self, filename=None, **kwargs):
        if filename is not None:
            kwargs['filename'] = filename
        Clutter.Texture.__init__(self, **kwargs)

Texture = override(Texture)
__all__.append('Texture')


class Rectangle(Clutter.Rectangle, Actor):
    def __init__(self, color=None, **kwargs):
        if color is not None:
            kwargs['color'] = color
        Clutter.Rectangle.__init__(self, **kwargs)

Rectangle = override(Rectangle)
__all__.append('Rectangle')


class Text(Clutter.Text, Actor):
    def __init__(self, font_name=None, text=None, color=None, **kwargs):
        if font_name is not None:
            kwargs['font_name'] = font_name
        if text is not None:
            kwargs['text'] = text
        if color is not None:
            kwargs['color'] = color
        Clutter.Text.__init__(self, **kwargs)

    def position_to_coords(self, position):
        success, x, y, lh = Clutter.Text.position_to_coords(self, position)
        if success:
            return (x, y, lh)

Text = override(Text)
__all__.append('Text')


class CairoTexture(Clutter.CairoTexture):
    def __init__(self, surface_width=1, surface_height=1, **kwargs):
        Clutter.CairoTexture.__init__(self, surface_width=surface_width,
                                      surface_height=surface_height, **kwargs)

CairoTexture = override(CairoTexture)
__all__.append('CairoTexture')


class Clone(Clutter.Clone):
    def __init__(self, source=None, **kwargs):
        if source is not None:
            kwargs['source'] = source
        Clutter.Clone.__init__(self, **kwargs)

Clone = override(Clone)
__all__.append('Clone')


class LayoutManager(Clutter.LayoutManager):
    def child_set_property(self, container, child, property_name, value):
        meta = self.get_child_meta(container, child)
        meta.set_property(property_name, value)

    def child_get_property(self, container, child, property_name):
        meta = self.get_child_meta(container, child)
        return meta.get_property(property_name)

LayoutManager = override(LayoutManager)
__all__.append('LayoutManager')


class BinLayout(Clutter.BinLayout):
    def __init__(self, x_align=None, y_align=None, **kwargs):
        if x_align is not None:
            kwargs['x_align'] = x_align
        if y_align is not None:
            kwargs['y_align'] = y_align
        Clutter.BinLayout.__init__(self, **kwargs)

BinLayout = override(BinLayout)
__all__.append('BinLayout')


class FlowLayout(Clutter.FlowLayout):
    def __init__(self, orientation=None, **kwargs):
        if orientation is not None:
            kwargs['orientation'] = orientation
        Clutter.FlowLayout.__init__(self, **kwargs)

FlowLayout = override(FlowLayout)
__all__.append('FlowLayout')


class Box(Clutter.Box, Actor):
    def __init__(self, layout_manager=None, **kwargs):
        Clutter.Box.__init__(self, layout_manager=layout_manager, **kwargs)

    def pack(self, actor, **kwargs):
        self.add_actor(actor)
        layout_manager = self.get_layout_manager()
        if layout_manager:
            for k, v in kwargs.items():
                layout_manager.child_set_property(self, actor, k, v)

    def pack_after(self, actor, silbing, **kwargs):
        self.add_actor(actor)
        self.raise_child(actor, silbing)
        layout_manager = self.get_layout_manager()
        if layout_manager:
            for k, v in kwargs.items():
                layout_manager.child_set_property(self, actor, k, v)

    def pack_before(self, actor, silbing, **kwargs):
        self.add_actor(actor)
        self.lower_child(actor, silbing)
        layout_manager = self.get_layout_manager()
        if layout_manager:
            for k, v in kwargs.items():
                layout_manager.child_set_property(self, actor, k, v)

Box = override(Box)
__all__.append('Box')


class Model(Clutter.Model):
    def insert(self, row, *args):
        if len(args) < 2 or len(args) % 2:
            raise ValueError("Clutter.Model.insert needs at least one " +
                    "column / value pair")
        for column, value in zip(args[::2], args[1::2]):
            value = _gvalue_from_python(self.get_column_type(column), value)
            self.insert_value(row, column, value)

    def append(self, *args):
        if len(args) < 2 or len(args) % 2:
            raise ValueError("Clutter.Model.append needs at least one " +
                    "column / value pair")
        row = self.get_n_rows()
        self.insert(row, *args)

    def prepend(self, *args):
        if len(args) < 2 or len(args) % 2:
            raise ValueError("Clutter.Model.prepend needs at least one " +
                    "column / value pair")
        columns = []
        values = []
        for column, value in zip(args[::2], args[1::2]):
            value = _gvalue_from_python(self.get_column_type(column), value)
            columns.append(column)
            values.append(value)
        self.prependv(columns, values)

    def __repr__(self):
        return '<Clutter.%s rows: %d; columns: %d>' % (self.__class__.__name__,
                self.get_n_rows(), self.get_n_columns())

    def __len__(self):
        return self.get_n_rows()

    def __bool__(self):
        return True

    # alias for Python 2.x object protocol
    __nonzero__ = __bool__

    def __getitem__(self, key):
        n_rows = self.get_n_rows()
        if isinstance(key, int):
            if key < 0:
                key += n_rows
            if key < 0 or key >= n_rows:
                raise IndexError("Row index is out of bounds: %d" % key)
            return self.get_iter_at_row(key)
        elif isinstance(key, slice):
            start, stop, step = key.indices(n_rows)
            ret = []
            for i in range(start, stop, step):
                ret.append(self.get_iter_at_row(i))
            return ret
        else:
            raise TypeError("indices must be integer or slice")

Model = override(Model)
__all__.append('Model')


class ModelIter(Clutter.ModelIter):
    def __len__(self):
        return self.get_model().get_n_columns()

    def __str__(self):
        values = ''
        for i in range(self.get_model().get_n_columns()):
            values += '%d=%s; ' % (i, self.get_value(i))
        return '<Clutter.ModelIter row %d; %s>' % (self.get_row(), values)

    def __getitem__(self, key):
        if isinstance(key, int):
            return self.get_value(key)
        elif isinstance(key, slice):
            model = self.get_model()
            start, stop, step = key.indices(model.get_n_columns())
            ret = []
            for i in range(start, stop, step):
                ret.append(self.get_value(i))
            return ret
        elif isinstance(key, str):
            model = self.get_model()
            for i in range(model.get_n_columns()):
                name = model.get_column_name(i)
                if key == name:
                    return self.get_value(i)
            raise KeyError("no column named '%s'" % key)
        else:
            raise TypeError("index must be value or slice")

    def __setitem__(self, key, value):
        if isinstance(key, int):
            self.set_value(key, value)
        elif isinstance(key, slice):
            model = self.get_model()
            start, stop, step = key.indices(model.get_n_columns())
            for i in range(start, stop, step):
                self.set_value(i, value)
        elif isinstance(key, str):
            model = self.get_model()
            for i in range(model.get_n_columns()):
                name = model.get_column_name(i)
                if key == name:
                    self.set_value(i, value)
                    return
            raise KeyError("no column named '%s'" % key)
        else:
            raise TypeError("index must be int, slice or string")

    @property
    def model(self):
        return self.get_model()

ModelIter = override(ModelIter)
__all__.append('ModelIter')


class ListModel(Clutter.ListModel, Model):
    def __init__(self, *args):
        Clutter.ListModel.__init__(self)
        if len(args) < 2 or len(args) % 2:
            raise TypeError("Clutter.ListModel requires at least one " +
                            "type / name pair")
        self.set_types(args[::2])
        self.set_names(args[1::2])

ListModel = override(ListModel)
__all__.append('ListModel')


class Timeline(Clutter.Timeline):
    def __init__(self, duration=None, **kwargs):
        if duration is not None:
            kwargs['duration'] = duration
        Clutter.Timeline.__init__(self, **kwargs)

    def list_markers(self, position=-1):
        markers, n_markers = Clutter.Timeline.list_markers(self, position)
        return markers

Timeline = override(Timeline)
__all__.append('Timeline')


class Alpha(Clutter.Alpha):
    def __init__(self, timeline=None, mode=Clutter.AnimationMode.LINEAR,
            **kwargs):
        Clutter.Alpha.__init__(self, timeline=timeline, **kwargs)
        # FIXME: Setting :mode doesn't work via properties
        if mode != Clutter.AnimationMode.CUSTOM_MODE:
            self.set_mode(mode)

Alpha = override(Alpha)
__all__.append('Alpha')


class Path(Clutter.Path):
    def __init__(self, description=None, **kwargs):
        Clutter.Path.__init__(self)
        if description:
            self.set_description(description)


Path = override(Path)
__all__.append('Path')


class BehaviourPath(Clutter.BehaviourPath):
    def __init__(self, alpha=None, path=None, description=None):
        Clutter.BehaviourPath.__init__(self)
        self.props.alpha = alpha
        if path:
            self.set_path(path)
        elif description is not None:
            path = Path(description)
            self.set_path(path)

BehaviourPath = override(BehaviourPath)
__all__.append('BehaviourPath')


class Script(Clutter.Script):
    def load_from_data(self, data, length=-1):
        return Clutter.Script.load_from_data(self, data, length)

    def get_objects(self, *objects):
        ret = []
        for name in objects:
            obj = self.get_object(name)
            ret.append(obj)
        return ret

    def connect_signals(self, obj_or_map):
        def _full_callback(builder, gobj, signal_name, handler_name,
                connect_obj, flags, obj_or_map):
            handler = None
            if isinstance(obj_or_map, dict):
                handler = obj_or_map.get(handler_name, None)
            else:
                handler = getattr(obj_or_map, handler_name, None)

            if handler is None:
                raise AttributeError('Handler %s not found' % handler_name)

            if not _callable(handler):
                raise TypeError('Handler %s is not a method or function' %
                        handler_name)

            after = flags or GObject.ConnectFlags.AFTER
            if connect_obj is not None:
                if after:
                    gobj.connect_object_after(signal_name, handler,
                            connect_obj)
                else:
                    gobj.connect_object(signal_name, handler, connect_obj)
            else:
                if after:
                    gobj.connect_after(signal_name, handler)
                else:
                    gobj.connect(signal_name, handler)

        self.connect_signals_full(_full_callback, obj_or_map)

Script = override(Script)
__all__.append('Script')


class BindingPool(Clutter.BindingPool):
    def __init__(self, name, **kwargs):
        Clutter.BindingPool.__init__(self, name=name, **kwargs)

BindingPool = override(BindingPool)
__all__.append('BindingPool')


class Shader(Clutter.Shader):
    def set_vertex_source(self, data, length=-1):
        Clutter.Shader.set_vertex_source(self, data, length)

    def set_fragment_source(self, data, length=-1):
        Clutter.Shader.set_fragment_source(self, data, length)

Shader = override(Shader)
__all__.append('Shader')


class Animator(Clutter.Animator):
    def set_key(self, obj, property_name, mode, progress, value):
        try:
            pspec = getattr(obj.__class__.props, property_name)
        except AttributeError:
            raise AttributeError(("Objects of type '%s' don't have a " +
                "property '%s'") % (type(obj), property_name))
        return Clutter.Animator.set_key(self, obj, property_name, mode,
                progress, _gvalue_from_python(pspec.value_type, value))


Animator = override(Animator)
__all__.append('Animator')


class State(Clutter.State):
    def set_key(self, source_state, target_state, obj, property_name, mode,
                value, pre_delay=0.0, post_delay=0.0):
        try:
            pspec = getattr(obj.__class__.props, property_name)
        except AttributeError:
            raise AttributeError(("Objects of type '%s' don't have a " +
                "property '%s'") % (type(obj), property_name))
        return Clutter.State.set_key(self, source_state, target_state, obj,
                property_name, mode,
                _gvalue_from_python(pspec.value_type, value),
                pre_delay, post_delay)

State = override(State)
__all__.append('State')


class Interval(Clutter.Interval):
    def __init__(self, value_type, initial=None, final=None):
        Clutter.Interval.__init__(self, value_type=value_type)
        if initial is not None:
            self.set_initial(initial)
        if final is not None:
            self.set_final(final)

    def set_initial(self, value):
        Clutter.Interval.set_initial(self,
                _gvalue_from_python(self.props.value_type, value))

    def get_initial(self):
        try:
            return self.peek_initial_value()
        except TypeError:
            return None

    initial = property(get_initial, set_initial)

    def set_final(self, value):
        Clutter.Interval.set_final(self,
                _gvalue_from_python(self.props.value_type, value))

    def get_final(self):
        try:
            return self.peek_final_value()
        except TypeError:
            return None

    final = property(get_final, set_final)

Interval = override(Interval)
__all__.append('Interval')


class AlignConstraint(Clutter.AlignConstraint):
    def __init__(self, source=None, align_axis=None, factor=None, **kwargs):
        if source is not None:
            kwargs['source'] = source
        if align_axis is not None:
            kwargs['align_axis'] = align_axis
        if factor is not None:
            kwargs['factor'] = factor
        Clutter.AlignConstraint.__init__(self, **kwargs)

AlignConstraint = override(AlignConstraint)
__all__.append('AlignConstraint')


class BindConstraint(Clutter.BindConstraint):
    def __init__(self, source=None, coordinate=None, offset=None, **kwargs):
        if source is not None:
            kwargs['source'] = source
        if coordinate is not None:
            kwargs['coordinate'] = coordinate
        if offset is not None:
            kwargs['offset'] = offset
        Clutter.BindConstraint.__init__(self, **kwargs)

BindConstraint = override(BindConstraint)
__all__.append('BindConstraint')


class SnapConstraint(Clutter.SnapConstraint):
    def __init__(self, source=None, from_edge=None, to_edge=None, offset=None,
            **kwargs):
        if source is not None:
            kwargs['source'] = source
        if from_edge is not None:
            kwargs['from_edge'] = from_edge
        if to_edge is not None:
            kwargs['to_edge'] = to_edge
        if offset is not None:
            kwargs['offset'] = offset
        Clutter.SnapConstraint.__init__(self, **kwargs)

SnapConstraint = override(SnapConstraint)
__all__.append('SnapConstraint')


class PathConstraint(Clutter.PathConstraint):
    def __init__(self, path=None, offset=None, **kwargs):
        if path is not None:
            kwargs['path'] = path
        if offset is not None:
            kwargs['offset'] = offset
        Clutter.PathConstraint.__init__(self, **kwargs)

PathConstraint = override(PathConstraint)
__all__.append('PathConstraint')


class ShaderEffect(Clutter.ShaderEffect):
    def __init__(self, shader_type=None, **kwargs):
        if shader_type is not None:
            kwargs['shader_type'] = shader_type
        Clutter.ShaderEffect.__init__(self, **kwargs)

ShaderEffect = override(ShaderEffect)
__all__.append('ShaderEffect')


class ColorizeEffect(Clutter.ColorizeEffect):
    def __init__(self, tint=None, **kwargs):
        if tint is not None:
            kwargs['tint'] = tint
        Clutter.ColorizeEffect.__init__(self, **kwargs)

ColorizeEffect = override(ColorizeEffect)
__all__.append('ColorizeEffect')


if clutter_version >= (1, 10, 0):
    class Content(Clutter.Content):
        def get_preferred_size(self):
            success, width, height = super(Content, self).get_preferred_size()
            if success:
                return (width, height)

    Content = override(Content)
    __all__.append('Content')


    class Margin(Clutter.Margin):
        def __new__(cls, *args, **kwargs):
            return Clutter.Margin.__new__(cls)

        def __init__(self, *args, **kwargs):
            Clutter.Margin.__init__(self)
            # using css semantics
            if len(args) == 1:
                self.top = self.right = self.bottom = self.left = args[0]
            elif len(args) == 2:
                self.top = self.bottom = args[0]
                self.right = self.left = args[1]
            elif len(args) == 3:
                self.top = args[0]
                self.left = self.right = args[1]
                self.bottom = args[2]
            elif len(args) == 4:
                self.top = args[0]
                self.right = args[1]
                self.bottom = args[2]
                self.left = args[3]
            else:
                self.top = kwargs.get('top', 0.0)
                self.right = kwargs.get('right', 0.0)
                self.bottom = kwargs.get('bottom', 0.0)
                self.left = kwargs.get('left', 0.0)

        def __repr__(self):
            return '<Clutter.Margin(left=%f, right=%f, top=%f, bottom=%f)>' \
                    % (self.left, self.right, self.top, self.bottom)

        def __len__(self):
            return 4

        def __getitem__(self, key):
            if isinstance(key, int):
                if key == 0:
                    return self.top
                elif key == 1:
                    return self.right
                elif key == 2:
                    return self.bottom
                elif key == 3:
                    return self.left
                else:
                    raise IndexError("index out of range")
            else:
                raise TypeError("sequence index must be integer")

        def __setitem__(self, key, value):
            if isinstance(key, int):
                if key == 0:
                    self.top = value
                elif key == 1:
                    self.right = value
                elif key == 2:
                    self.bottom = value
                elif key == 3:
                    self.left = value
                else:
                    raise IndexError("index out of range")
            else:
                raise TypeError("sequence index must be integer")

        def __eq__(self, other):
            return self.top == other.top and \
                    self.right == other.right and \
                    self.bottom == other.bottom and \
                    self.left == other.left

        def __ne__(self, other):
            return not self.__eq__(other)

    Margin = override(Margin)
    __all__.append('Margin')


    class ColorNode(Clutter.ColorNode):
        def __new__(cls, color):
            return Clutter.ColorNode.new(color)

    ColorNode = override(ColorNode)
    __all__.append('ColorNode')


    class TextNode(Clutter.TextNode):
        def __new__(cls, layout, color):
            return Clutter.TextNode.new(layout, color)

    TextNode = override(TextNode)
    __all__.append('TextNode')


    class TextureNode(Clutter.TextureNode):
        def __new__(cls, texture, color, min_filter, mag_filter):
            return Clutter.TextureNode.new(texture, color, min_filter,
                    mag_filter)

    TextureNode = override(TextureNode)
    __all__.append('TextureNode')


    class PipelineNode(Clutter.PipelineNode):
        def __new__(cls, pipeline):
            return Clutter.PipelineNode.new(pipeline)

    PipelineNode = override(PipelineNode)
    __all__.append('PipelineNode')


    class PropertyTransition(Clutter.PropertyTransition):
        def __init__(self, property_name=None, **kwargs):
            if property_name is not None:
                kwargs['property_name'] = property_name
            Clutter.PropertyTransition.__init__(self, **kwargs)

    PropertyTransition = override(PropertyTransition)
    __all__.append('PropertyTransition')



class Settings(Clutter.Settings):
    def __new__(cls, *args, **kwargs):
        return Clutter.Settings.get_default()

Settings = override(Settings)
__all__.append('Settings')

# override the main_quit function to ignore additional arguments. This enables
# common stuff like stage.connect('destroy', Clutter.main_quit)
def main_quit(*args, **kwargs):
    Clutter.main_quit()

__all__.append('main_quit')


# Initialize Clutter directly on import
initialized, argv = Clutter.init(sys.argv)
sys.argv = argv
if not initialized:
    raise RuntimeError("Could not initialize Cluttter")
