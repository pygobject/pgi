PGI - Pure Python GObject Introspection Bindings
================================================

GObject Introspection bindings written in pure Python using ctypes_
and cffi_ (optional). API compatible with PyGObject_.

**License:** LGPL 2.1+

**Requirements:**

- CPython_ 2.7 or PyPy_ 1.9
- libgirepository_ 1.0
- cffi_ 0.6+ (optional)
- cairocffi_ 0.4+ (optional, for cairo support)

**Development Status:**

See the 'examples' directory for working examples.
Anything else will probably not work.

.. _ctypes: http://docs.python.org/2/library/ctypes.html
.. _cffi: http://cffi.readthedocs.org/en/latest/
.. _cairocffi: http://pythonhosted.org/cairocffi/
.. _PyGObject: http://git.gnome.org/browse/pygobject/
.. _libgirepository: http://git.gnome.org/browse/gobject-introspection/
.. _CPython: http://www.python.org/
.. _PyPy: http://pypy.org/

Usage
-----

::

    from pgi.repository import Gtk, GObject

or (preferred)

::

    import pgi
    pgi.install_as_gi()
    from gi.repository import Gtk, GObject

Backends
~~~~~~~~

There are two code generation backends for ctypes and cffi. You can set
the preferred backend before importing modules:

::

    import pgi
    pgi.set_backend('ctypes')
    pgi.set_backend('cffi')

If the backend doesn't support an operation it will fall back to the other one.

Search paths
~~~~~~~~~~~~

Typelibs will be loaded from paths in the environment variable
`GI_TYPELIB_PATH` and `/usr/lib/girepository-1.0/`.

Shared libraries from paths in `LD_LIBRARY_PATH` and the default system
search paths (see dlopen(3)).

Documentation
-------------

https://github.com/lazka/pgi-docgen

http://lazka.github.io/pgi-docs

Tests
-----

- `./setup.py test` will run unit tests using PGI and PyGObject
- `./setup.py test --pgi-only` to skip PyGObject tests
- `./setup.py test --filter=StructTest` to run tests which include
  `StructTest` (regexp)

`./tests/libs/` includes additional libraries that will be used for testing
if present. Call `make` in `./tests/libs/` to build them.
