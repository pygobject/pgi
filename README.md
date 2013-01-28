PGI - Pure Python GObject Introspection Bindings
================================================

 GObject Introspection bindings written in pure python using [ctypes] [1]
 and [cffi] [2] (optional).

 See the 'examples' directory for working examples.

 License: LGPL 2.1+

[1]: http://docs.python.org/2/library/ctypes.html   "ctypes"
[2]: http://cffi.readthedocs.org/en/latest/         "cffi"

Goals
-----

 - PyGObject compatibility
 - Python 2.7 / PyPy 1.9

Usage
-----

```python
from pgi.repository import Gtk, GObject
```

or

```python
import pgi
pgi.install_as_gi()
from gi.repository import Gtk, GObject
```

There are two code generation backends for ctypes and cffi. You can set
the preferred backend before importing any modules:

```python
import pgi
pgi.set_backend('ctypes')
pgi.set_backend('cffi')
```

If the backend doesn't support an operation it will fall back to the other one.

Tests
-----

 - `./setup.py test` will run unit tests using PGI and PyGObject
 - `./setup.py test --pgi-only` to skip PyGObject tests
