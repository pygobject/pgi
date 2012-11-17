#!/usr/bin/python
# Copyright 2012 Christoph Reiter
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

import os
import sys
import glob

from distutils.core import setup, Command
import pgi


class CoverageCommand(Command):
    description = "generaqte coverage"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import trace
        tracer = trace.Trace(
            count=True, trace=False,
            ignoredirs=[sys.prefix, sys.exec_prefix])

        def run_tests():
            try:
                 # we don't want to fork and use PyGObject
                cmd = self.reinitialize_command("test")
                cmd.pgi_only = True
                cmd.ensure_finalized()
                cmd.run()
            except:
                pass

        tracer.runfunc(run_tests)
        results = tracer.results()
        coverage = os.path.join(os.path.dirname(__file__), "coverage")
        results.write_results(show_missing=True, coverdir=coverage)

        # remove coverage we don't want
        for f in os.listdir(coverage):
            if not f.startswith("pgi."):
                os.unlink(os.path.join(coverage, f))
                continue
            if f.startswith("pgi.overrides") and \
                    not os.path.basename(f).startswith("_"):
                os.unlink(os.path.join(coverage, f))
                continue

        # compute coverage
        stats = []
        for filename in glob.glob(os.path.join(coverage, "*.cover")):
            lines = file(filename, "rU").readlines()
            lines = filter(None, map(str.strip, lines))
            total_lines = len(lines)
            bad_lines = len([l for l in lines if l.startswith(">>>>>>")])
            percent = 100.0 * (total_lines - bad_lines) / float(total_lines)
            stats.append((percent, filename, total_lines, bad_lines))
        stats.sort(reverse=True)
        print "#" * 80
        print "COVERAGE"
        print "#" * 80
        total_sum = 0
        bad_sum = 0
        for s in stats:
            p, f, t, b = s
            total_sum += t
            bad_sum += b
            print "%6.2f%% %s" % (p, os.path.basename(f))
        print "-" * 80
        print "Coverage data written to", coverage, "(%d/%d, %0.2f%%)" % (
            total_sum - bad_sum, total_sum,
            100.0 * (total_sum - bad_sum) / float(total_sum))
        print "#" * 80


class TestCommand(Command):
    description = "run unit tests"
    user_options = [
        ("pgi-only", None, "only run pgi"),
    ]

    def initialize_options(self):
        self.pgi_only = False

    def finalize_options(self):
        self.pgi_only = bool(self.pgi_only)

    def run(self):
        import tests
        import os
        import platform

        is_cpython = platform.python_implementation() == "CPython"

        # Run with both bindings, PGI first
        # Skip the second run if the first one fails
        if not is_cpython or self.pgi_only:
            pid = 0
        else:
            pid = os.fork()
        if pid != 0:
            pid, status = os.waitpid(pid, 0)
            if status:
                exit(status)
        exit(tests.test(pid != 0))


setup(name='pgi',
      version=".".join(map(str, pgi.version)),
      description='Pure Python GObject Introspection Bindings',
      author='Christoph Reiter',
      author_email='reiter.christoph@gmail.com',
      url='https://github.com/lazka/pgi',
      packages=['pgi', 'pgi.gir', 'pgi.glib', 'pgi.gobject',
                'pgi.overrides', 'pgi.repository'],
      license='GPLv2',
      cmdclass={
            'test': TestCommand,
            'coverage': CoverageCommand,
      }
     )
