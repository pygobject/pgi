#!/usr/bin/python
# Copyright 2012,2013 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

from __future__ import print_function

import os
import sys
import glob
import subprocess
import re

from distutils.core import setup, Command
import pgi


class CoverageCommand(Command):
    description = "generate coverage"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        set_test_environ()

        # Wipe existing modules, to make sure coverage data is properly
        # generated for them.
        for key in list(sys.modules.keys()):
            if key.startswith('pgi'):
                del(sys.modules[key])

        try:
            from coverage import coverage
        except ImportError:
            print("Missing 'coverage' module. See "
                  "https://pypi.python.org/pypi/coverage or try "
                  "`apt-get install python-coverage`")
            return

        cov = coverage()
        cov.start()

        import tests
        tests.test(False, "cffi")

        dest = os.path.join(os.getcwd(), "coverage")

        cov.stop()
        cov.html_report(
            directory=dest,
            ignore_errors=True,
            include=["pgi/*"])

        print("Coverage summary: file://%s/index.html" % dest)


def set_test_environ():
    """Sets LD_LIBRARY_PATH for dlopen and GI_TYPELIB_PATH for gi"""

    ld_path = os.path.join(os.path.dirname(__file__), "tests", "libs")

    paths = os.environ.get("LD_LIBRARY_PATH", "")
    if ld_path not in paths.split(os.pathsep):
        print("Testlibs not in LD_LIBRARY_PATH: exec self with new environ")
        paths = ld_path + os.pathsep + paths
        os.environ["LD_LIBRARY_PATH"] = paths
        # restart the interpreter so dlopen gets te right environ
        exit(subprocess.call([sys.executable] + sys.argv))

    typelib_paths = os.environ.get("GI_TYPELIB_PATH", "")
    if ld_path not in typelib_paths.split(os.pathsep):
        print("Adding %r to GI_TYPELIB_PATH" % ld_path)
        typelib_paths = ld_path + os.pathsep + typelib_paths
        os.environ["GI_TYPELIB_PATH"] = typelib_paths


class TestCommand(Command):
    description = "run unit tests"
    user_options = [
        ("pgi-only", None, "only run pgi"),
        ("gi-only", None, "only run gi"),
        ("backend=", None, "backend"),
        ("strict", None, "make glib warnings/errors fatal"),
        ("filter=", None, "regexp for filter classes"),
        ("exitfirst", "x", "exit instantly on first error or failed test"),
    ]

    def initialize_options(self):
        self.pgi_only = False
        self.gi_only = False
        self.backend = ""
        self.filter = ""
        self.strict = False
        self.exitfirst = False

    def finalize_options(self):
        self.pgi_only = bool(self.pgi_only)
        self.gi_only = bool(self.gi_only)
        self.backend = str(self.backend)
        self.strict = bool(self.strict)
        self.filter = str(self.filter)
        self.exitfirst = bool(self.exitfirst)

    def run(self):
        import tests
        import os
        import platform

        set_test_environ()

        if os.name == "nt":
            self.pgi_only = True
            self.backend = "ctypes"
            self.gi_only = False

        if platform.python_implementation() != "CPython":
            self.pgi_only = True
            self.gi_only = False

        if self.pgi_only and self.gi_only:
            raise ValueError("You can't set both pgi-only and gi-only")

        if self.backend and self.gi_only :
            raise ValueError("Backend selection only works with pgi")

        filtered_runs = []
        runs =  [(False, "ctypes"), (False, "cffi"), (True, None)]
        for (run_gi, backend) in runs:
            if run_gi and self.pgi_only:
                continue
            if not run_gi and self.gi_only:
                continue
            if self.backend and self.backend != backend:
                continue
            filtered_runs.append((run_gi, backend))

        # create a filter function for selecting tests by regexp
        if self.filter:
            def filter_tests(name):
                return re.search(self.filter, name) is not None
        else:
            filter_tests = None

        # don't fork with one run
        if len(filtered_runs) == 1:
            run_gi, backend = filtered_runs[0]
            exit(tests.test(
                run_gi, backend, self.strict, filter_tests, self.exitfirst))

        for is_gi, backend in filtered_runs:
            pid = os.fork()
            if pid != 0:
                pid, status = os.waitpid(pid, 0)
                kill_signal = (status & 0xff)
                returncode = (status >> 8) & 0xff
                if not kill_signal:
                    if returncode:
                        exit(returncode)
                else:
                    exit(1)
            else:
                exit(tests.test(
                    is_gi, backend, self.strict, filter_tests, self.exitfirst))


class QualityCommand(Command):
    description = "run pep8 pyflakes"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import tests

        exit(tests.test_pep8() != 0)


class BenchmarkCommand(Command):
    description = "run benchmarks"
    user_options = [
        ("pgi-only", None, "only run pgi"),
    ]

    def initialize_options(self):
        self.pgi_only = False

    def finalize_options(self):
        self.pgi_only = bool(self.pgi_only)

    def run(self):
        import benchmarks
        import os
        import platform

        if os.name == "nt":
            exit(benchmarks.run(False, "ctypes"))

        set_test_environ()

        is_cpython = platform.python_implementation() == "CPython"
        runs = [(False, "ctypes"), (False, "cffi"), (True, None)]

        for is_gi, backend in runs:
            if is_gi and (self.pgi_only or not is_cpython):
                continue

            pid = os.fork()
            if pid != 0:
                pid, status = os.waitpid(pid, 0)
                if status:
                    exit(status)
            else:
                exit(benchmarks.run(is_gi, backend))


setup(name='pgi',
      version=pgi.__version__,
      description='Pure Python GObject Introspection Bindings',
      author='Christoph Reiter',
      author_email='reiter.christoph@gmail.com',
      url='https://github.com/lazka/pgi',
      packages=[
         'pgi',
         'pgi.clib',
         'pgi.clib.gir',
         'pgi.cffilib',
         'pgi.cffilib.gir',
         'pgi.cffilib.glib',
         'pgi.cffilib.gobject',
         'pgi.foreign',
         'pgi.overrides',
         'pgi.repository',
         'pgi.codegen',
         'pgi.codegen.ctypes_backend',
      ],
      license='LGPL-2.1+',
      classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
      ],
      cmdclass={
            'test': TestCommand,
            'coverage': CoverageCommand,
            'benchmark': BenchmarkCommand,
            'quality': QualityCommand,
      }
     )
