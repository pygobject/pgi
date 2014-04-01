# -*- Mode: Python -*-

import sys
import gc
import unittest
import warnings

from gi.repository import GObject, GLib

try:
    from gi import PyGIDeprecationWarning
    PyGIDeprecationWarning
except ImportError:
    # older pygobject
    PyGIDeprecationWarning = None

import gi

from tests import FIXME, skipIfPyPy, skipUnlessGIVersionAtLeast, \
    GIOverflowError

testhelper = None
get_introspection_module = None
_gobject = None


class TestGObjectAPI(unittest.TestCase):
    @FIXME
    def test_gobject_inheritance(self):
        # GObject.Object is a class hierarchy as follows:
        # overrides.Object -> introspection.Object -> static.GObject
        GIObjectModule = get_introspection_module('GObject')
        self.assertTrue(issubclass(GObject.Object, GIObjectModule.Object))
        self.assertTrue(issubclass(GIObjectModule.Object, _gobject.GObject))

        self.assertEqual(_gobject.GObject.__gtype__, GObject.TYPE_OBJECT)
        self.assertEqual(GIObjectModule.Object.__gtype__, GObject.TYPE_OBJECT)
        self.assertEqual(GObject.Object.__gtype__, GObject.TYPE_OBJECT)

        # The pytype wrapper should hold the outer most Object class from overrides.
        self.assertEqual(GObject.TYPE_OBJECT.pytype, GObject.Object)

    @FIXME
    def test_gobject_unsupported_overrides(self):
        obj = GObject.Object()

        with self.assertRaisesRegex(RuntimeError, 'Data access methods are unsupported.*'):
            obj.get_data()

        with self.assertRaisesRegex(RuntimeError, 'This method is currently unsupported.*'):
            obj.force_floating()

    @FIXME
    @unittest.skipUnless(PyGIDeprecationWarning, "too old pygi")
    def test_compat_api(self):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter('always')
            # GObject formerly exposed a lot of GLib's functions
            self.assertEqual(GObject.markup_escape_text('foo'), 'foo')

            ml = GObject.MainLoop()
            self.assertFalse(ml.is_running())

            context = GObject.main_context_default()
            self.assertTrue(context.pending() in [False, True])

            context = GObject.MainContext()
            self.assertFalse(context.pending())

            self.assertTrue(issubclass(w[0].category, PyGIDeprecationWarning))
            self.assertTrue('GLib.markup_escape_text' in str(w[0]), str(w[0]))

            self.assertLess(GObject.PRIORITY_HIGH, GObject.PRIORITY_DEFAULT)

    def test_min_max_int(self):
        self.assertEqual(GObject.G_MAXINT16, 2 ** 15 - 1)
        self.assertEqual(GObject.G_MININT16, -2 ** 15)
        self.assertEqual(GObject.G_MAXUINT16, 2 ** 16 - 1)

        self.assertEqual(GObject.G_MAXINT32, 2 ** 31 - 1)
        self.assertEqual(GObject.G_MININT32, -2 ** 31)
        self.assertEqual(GObject.G_MAXUINT32, 2 ** 32 - 1)

        self.assertEqual(GObject.G_MAXINT64, 2 ** 63 - 1)
        self.assertEqual(GObject.G_MININT64, -2 ** 63)
        self.assertEqual(GObject.G_MAXUINT64, 2 ** 64 - 1)


class TestReferenceCounting(unittest.TestCase):
    def test_regular_object(self):
        obj = GObject.GObject()
        self.assertEqual(obj.__grefcount__, 1)

        obj = GObject.new(GObject.GObject)
        self.assertEqual(obj.__grefcount__, 1)

    @FIXME
    def test_floating(self):
        obj = testhelper.Floating()
        self.assertEqual(obj.__grefcount__, 1)

        obj = GObject.new(testhelper.Floating)
        self.assertEqual(obj.__grefcount__, 1)

    @FIXME
    def test_owned_by_library(self):
        # Upon creation, the refcount of the object should be 2:
        # - someone already has a reference on the new object.
        # - the python wrapper should hold its own reference.
        obj = testhelper.OwnedByLibrary()
        self.assertEqual(obj.__grefcount__, 2)

        # We ask the library to release its reference, so the only
        # remaining ref should be our wrapper's. Once the wrapper
        # will run out of scope, the object will get finalized.
        obj.release()
        self.assertEqual(obj.__grefcount__, 1)

    @FIXME
    def test_owned_by_library_out_of_scope(self):
        obj = testhelper.OwnedByLibrary()
        self.assertEqual(obj.__grefcount__, 2)

        # We are manually taking the object out of scope. This means
        # that our wrapper has been freed, and its reference dropped. We
        # cannot check it but the refcount should now be 1 (the ref held
        # by the library is still there, we didn't call release()
        obj = None

        # When we get the object back from the lib, the wrapper is
        # re-created, so our refcount will be 2 once again.
        obj = testhelper.owned_by_library_get_instance_list()[0]
        self.assertEqual(obj.__grefcount__, 2)

        obj.release()
        self.assertEqual(obj.__grefcount__, 1)

    @FIXME
    def test_owned_by_library_using_gobject_new(self):
        # Upon creation, the refcount of the object should be 2:
        # - someone already has a reference on the new object.
        # - the python wrapper should hold its own reference.
        obj = GObject.new(testhelper.OwnedByLibrary)
        self.assertEqual(obj.__grefcount__, 2)

        # We ask the library to release its reference, so the only
        # remaining ref should be our wrapper's. Once the wrapper
        # will run out of scope, the object will get finalized.
        obj.release()
        self.assertEqual(obj.__grefcount__, 1)

    @FIXME
    def test_owned_by_library_out_of_scope_using_gobject_new(self):
        obj = GObject.new(testhelper.OwnedByLibrary)
        self.assertEqual(obj.__grefcount__, 2)

        # We are manually taking the object out of scope. This means
        # that our wrapper has been freed, and its reference dropped. We
        # cannot check it but the refcount should now be 1 (the ref held
        # by the library is still there, we didn't call release()
        obj = None

        # When we get the object back from the lib, the wrapper is
        # re-created, so our refcount will be 2 once again.
        obj = testhelper.owned_by_library_get_instance_list()[0]
        self.assertEqual(obj.__grefcount__, 2)

        obj.release()
        self.assertEqual(obj.__grefcount__, 1)

    @FIXME
    def test_floating_and_sunk(self):
        # Upon creation, the refcount of the object should be 2:
        # - someone already has a reference on the new object.
        # - the python wrapper should hold its own reference.
        obj = testhelper.FloatingAndSunk()
        self.assertEqual(obj.__grefcount__, 2)

        # We ask the library to release its reference, so the only
        # remaining ref should be our wrapper's. Once the wrapper
        # will run out of scope, the object will get finalized.
        obj.release()
        self.assertEqual(obj.__grefcount__, 1)

    @FIXME
    def test_floating_and_sunk_out_of_scope(self):
        obj = testhelper.FloatingAndSunk()
        self.assertEqual(obj.__grefcount__, 2)

        # We are manually taking the object out of scope. This means
        # that our wrapper has been freed, and its reference dropped. We
        # cannot check it but the refcount should now be 1 (the ref held
        # by the library is still there, we didn't call release()
        obj = None

        # When we get the object back from the lib, the wrapper is
        # re-created, so our refcount will be 2 once again.
        obj = testhelper.floating_and_sunk_get_instance_list()[0]
        self.assertEqual(obj.__grefcount__, 2)

        obj.release()
        self.assertEqual(obj.__grefcount__, 1)

    @FIXME
    def test_floating_and_sunk_using_gobject_new(self):
        # Upon creation, the refcount of the object should be 2:
        # - someone already has a reference on the new object.
        # - the python wrapper should hold its own reference.
        obj = GObject.new(testhelper.FloatingAndSunk)
        self.assertEqual(obj.__grefcount__, 2)

        # We ask the library to release its reference, so the only
        # remaining ref should be our wrapper's. Once the wrapper
        # will run out of scope, the object will get finalized.
        obj.release()
        self.assertEqual(obj.__grefcount__, 1)

    @FIXME
    def test_floating_and_sunk_out_of_scope_using_gobject_new(self):
        obj = GObject.new(testhelper.FloatingAndSunk)
        self.assertEqual(obj.__grefcount__, 2)

        # We are manually taking the object out of scope. This means
        # that our wrapper has been freed, and its reference dropped. We
        # cannot check it but the refcount should now be 1 (the ref held
        # by the library is still there, we didn't call release()
        obj = None

        # When we get the object back from the lib, the wrapper is
        # re-created, so our refcount will be 2 once again.
        obj = testhelper.floating_and_sunk_get_instance_list()[0]
        self.assertEqual(obj.__grefcount__, 2)

        obj.release()
        self.assertEqual(obj.__grefcount__, 1)

    @FIXME
    def test_uninitialized_object(self):
        class Obj(GObject.GObject):
            def __init__(self):
                x = self.__grefcount__
                super(Obj, self).__init__()
                assert x >= 0  # quiesce pyflakes

        # Accessing __grefcount__ before the object is initialized is wrong.
        # Ensure we get a proper exception instead of a crash.
        self.assertRaises(TypeError, Obj)


class A(GObject.GObject):
    def __init__(self):
        super(A, self).__init__()


@skipIfPyPy
class TestPythonReferenceCounting(unittest.TestCase):
    # Newly created instances should alwayshave two references: one for
    # the GC, and one for the bound variable in the local scope.

    def test_new_instance_has_two_refs(self):
        obj = GObject.GObject()
        self.assertEqual(sys.getrefcount(obj), 2)

    def test_new_instance_has_two_refs_using_gobject_new(self):
        obj = GObject.new(GObject.GObject)
        self.assertEqual(sys.getrefcount(obj), 2)

    def test_new_subclass_instance_has_two_refs(self):
        obj = A()
        self.assertEqual(sys.getrefcount(obj), 2)

    def test_new_subclass_instance_has_two_refs_using_gobject_new(self):
        obj = GObject.new(A)
        self.assertEqual(sys.getrefcount(obj), 2)


class TestGValue(unittest.TestCase):
    @FIXME
    def test_type_constant(self):
        self.assertEqual(GObject.TYPE_VALUE, GObject.Value.__gtype__)
        self.assertEqual(GObject.type_name(GObject.TYPE_VALUE), 'GValue')

    @skipUnlessGIVersionAtLeast(3, 8)
    def test_no_type(self):
        value = GObject.Value()
        self.assertEqual(value.g_type, GObject.TYPE_INVALID)
        self.assertRaises(TypeError, value.set_value, 23)
        self.assertEqual(value.get_value(), None)

    @skipUnlessGIVersionAtLeast(3, 8)
    def test_int(self):
        value = GObject.Value(GObject.TYPE_UINT)
        self.assertEqual(value.g_type, GObject.TYPE_UINT)
        value.set_value(23)
        self.assertEqual(value.get_value(), 23)
        value.set_value(42.0)
        self.assertEqual(value.get_value(), 42)

    @skipUnlessGIVersionAtLeast(3, 8)
    def test_string(self):
        value = GObject.Value(str, 'foo_bar')
        self.assertEqual(value.g_type, GObject.TYPE_STRING)
        self.assertEqual(value.get_value(), 'foo_bar')

    @skipUnlessGIVersionAtLeast(3, 8)
    def test_float(self):
        # python float is G_TYPE_DOUBLE
        value = GObject.Value(float, 23.4)
        self.assertEqual(value.g_type, GObject.TYPE_DOUBLE)
        value.set_value(1e50)
        self.assertAlmostEqual(value.get_value(), 1e50)

        value = GObject.Value(GObject.TYPE_FLOAT, 23.4)
        self.assertEqual(value.g_type, GObject.TYPE_FLOAT)
        self.assertRaises(TypeError, value.set_value, 'string')
        self.assertRaises(GIOverflowError, value.set_value, 1e50)

    @FIXME  # on pypy only
    def test_float_inf_nan(self):
        nan = float('nan')
        for type_ in [GObject.TYPE_FLOAT, GObject.TYPE_DOUBLE]:
            for x in [float('inf'), float('-inf'), nan]:
                value = GObject.Value(type_, x)
                # assertEqual() is False for (nan, nan)
                if x is nan:
                    self.assertEqual(str(value.get_value()), 'nan')
                else:
                    self.assertEqual(value.get_value(), x)

    @FIXME
    def test_enum(self):
        value = GObject.Value(GLib.FileError, GLib.FileError.FAILED)
        self.assertEqual(value.get_value(), GLib.FileError.FAILED)

    @FIXME
    def test_flags(self):
        value = GObject.Value(GLib.IOFlags, GLib.IOFlags.IS_READABLE)
        self.assertEqual(value.get_value(), GLib.IOFlags.IS_READABLE)

    @skipUnlessGIVersionAtLeast(3, 8)
    def test_object(self):
        class TestObject(GObject.Object):
            pass
        obj = TestObject()
        value = GObject.Value(GObject.TYPE_OBJECT, obj)
        self.assertEqual(value.get_value(), obj)

if __name__ == '__main__':
    unittest.main()
