#!/usr/bin/python
# Copyright 2012 Christoph Reiter
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

from distutils.core import setup, Command


class TestCommand(Command):
    description = "run unit tests"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
      import tests
      import os

      # Run with both bindings, PGI first
      # Skip the second run if the first one fails
      pid = os.fork()
      if pid != 0:
          pid, status = os.waitpid(pid, 0)
          if status:
              exit(status)
      exit(tests.test(pid != 0))


setup(name='PGI',
      version='0.0.1',
      description='Pure Python GObject Introspection Bindings',
      author='Christoph Reiter',
      author_email='reiter.christoph@gmail.com',
      url='https://github.com/lazka/pgi',
      packages=['pgi', 'pgi.gitypes', 'pgi.overrides', 'pgi.repository'],
      license='GPLv2',
      cmdclass={
            'test': TestCommand
      }
     )
