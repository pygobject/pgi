# coding=utf-8
# Copyright 2013 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

# most tests here taken from pygobject "tests/test_everything.py"

import sys
import unittest

from gi.repository import Gtk

try:
    from gi.repository import Regress as Everything
    Everything
except ImportError:
    Everything = None


@unittest.skipUnless(Everything, "no Regress")
class TestNullableArgs(unittest.TestCase):
    @unittest.skip("FIXME")
    def test_in_nullable_hash(self):
        Everything.test_ghash_null_in(None)

    @unittest.skip("FIXME")
    def test_in_nullable_list(self):
        Everything.test_gslist_null_in(None)
        Everything.test_glist_null_in(None)
        Everything.test_gslist_null_in([])
        Everything.test_glist_null_in([])

    @unittest.skip("FIXME")
    def test_in_nullable_array(self):
        Everything.test_array_int_null_in(None)
        Everything.test_array_int_null_in([])

    def test_in_nullable_string(self):
        Everything.test_utf8_null_in(None)

    def test_in_nullable_object(self):
        Everything.func_obj_null_in(None)

    @unittest.skip("FIXME")
    def test_out_nullable_hash(self):
        self.assertEqual(None, Everything.test_ghash_null_out())

    @unittest.skip("FIXME")
    def test_out_nullable_list(self):
        self.assertEqual([], Everything.test_gslist_null_out())
        self.assertEqual([], Everything.test_glist_null_out())

    def test_out_nullable_array(self):
        self.assertEqual([], Everything.test_array_int_null_out())

    def test_out_nullable_string(self):
        self.assertEqual(None, Everything.test_utf8_null_out())

    def test_out_nullable_object(self):
        self.assertEqual(None, Everything.TestObj.null_out())


@unittest.skipUnless(Everything, "no Regress")
class TestTortureProfile(unittest.TestCase):
    def test_torture_profile(self):
        import time
        total_time = 0
        print("")
        object_ = Everything.TestObj()
        sys.stdout.write("\ttorture test 1 (10000 iterations): ")

        start_time = time.clock()
        for i in range(10000):
            (y, z, q) = object_.torture_signature_0(5000,
                                                    "Torture Test 1",
                                                    12345)

        end_time = time.clock()
        delta_time = end_time - start_time
        total_time += delta_time
        print("%f secs" % delta_time)

        sys.stdout.write("\ttorture test 2 (10000 iterations): ")

        start_time = time.clock()
        for i in range(10000):
            (y, z, q) = Everything.TestObj().torture_signature_0(
                5000, "Torture Test 2", 12345)

        end_time = time.clock()
        delta_time = end_time - start_time
        total_time += delta_time
        print("%f secs" % delta_time)

        sys.stdout.write("\ttorture test 3 (10000 iterations): ")
        start_time = time.clock()
        for i in range(10000):
            try:
                (y, z, q) = object_.torture_signature_1(
                    5000, "Torture Test 3", 12345)
            except:
                pass
        end_time = time.clock()
        delta_time = end_time - start_time
        total_time += delta_time
        print("%f secs" % delta_time)

        # FIXME
        """sys.stdout.write("\ttorture test 4 (10000 iterations): ")

        def callback(userdata):
            pass

        userdata = [1, 2, 3, 4]
        start_time = time.clock()
        for i in range(10000):
            (y, z, q) = Everything.test_torture_signature_2(
                5000, callback, userdata, "Torture Test 4", 12345)
        end_time = time.clock()
        delta_time = end_time - start_time
        total_time += delta_time"""
        print("%f secs" % delta_time)
        print("\t====")
        print("\tTotal: %f sec" % total_time)
