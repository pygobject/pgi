PGI - Pure Python GObject Introspection Bindings
================================================

 GObject Introspection bindings written in pure python using ctypes_
 and cffi_ (optional).

 See the 'examples' directory for working examples.

 License: LGPL 2.1+

.. _ctypes: http://docs.python.org/2/library/ctypes.html
.. _cffi: http://cffi.readthedocs.org/en/latest/

Goals
-----

 - PyGObject compatibility
 - Python 2.7 / PyPy 1.9

Usage
-----

::

    from pgi.repository import Gtk, GObject

or (preferred)

::

    import pgi
    pgi.install_as_gi()
    from gi.repository import Gtk, GObject

There are two code generation backends for ctypes and cffi. You can set
the preferred backend before importing any modules:

::

    import pgi
    pgi.set_backend('ctypes')
    pgi.set_backend('cffi')

If the backend doesn't support an operation it will fall back to the other one.

Tests
-----

 - `./setup.py test` will run unit tests using PGI and PyGObject
 - `./setup.py test --pgi-only` to skip PyGObject tests

`./tests/libs/` includes additional libraries that will be used for testing
if present. Call `make` in `./tests/libs/` to build them.
