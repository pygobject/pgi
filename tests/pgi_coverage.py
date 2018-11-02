# -*- coding: utf-8 -*-

from __future__ import print_function

"""
Display API coverage of pgi vs gi.

To work you you need to have access to both 'gi' and 'pgi' in the current python
environment.

Instructions to run from a virtualenv:

Install pgi
$ python setup.py install

Grant access to gi.repository (not needed if outside virtualenv)
$ pip install vext.gi

Find missing coverage
$ python tests/pgi_coverage.py -m

Show all coverage
$ python tests/pgi_coverage.py
"""

TYPELIB_DIR="/usr/lib/girepository-1.0"

import os

from os.path import basename
from glob import glob
from textwrap import dedent

STATUS_OK = '✅'
STATUS_FAIL = '❌'

# Define a context manager to suppress stdout and stderr.
class suppress_stdout_stderr(object):
    '''
    A context manager for doing a "deep suppression" of stdout and stderr in 
    Python, i.e. will suppress all print, even if the print originates in a 
    compiled C/Fortran sub-function.
       This will not suppress raised exceptions, since exceptions are printed
    to stderr just before a script exits, and after the context manager has
    exited (at least, I think that is why it lets exceptions through).      

    '''
    # from https://stackoverflow.com/questions/11130156/suppress-stdout-stderr-print-from-python-functions
    def __init__(self):
        # Open a pair of null files
        self.null_fds =  [os.open(os.devnull,os.O_RDWR) for x in range(2)]
        # Save the actual stdout (1) and stderr (2) file descriptors.
        self.save_fds = [os.dup(1), os.dup(2)]

    def __enter__(self):
        # Assign the null pointers to stdout and stderr.
        os.dup2(self.null_fds[0],1)
        os.dup2(self.null_fds[1],2)

    def __exit__(self, *_):
        # Re-assign the real stdout/stderr back to (1) and (2)
        os.dup2(self.save_fds[0],1)
        os.dup2(self.save_fds[1],2)
        # Close all file descriptors
        for fd in self.null_fds + self.save_fds:
            os.close(fd)

def test_pgi_coverage(gi_module, pgi_module, show_success=True):
    name_width = len(max(dir(gi_module), key=len))
    print('  {}:'.format(gi_module.__name__))
    name_count = 0
    success_count = 0
    for name in dir(gi_module):
        if name.startswith('_'):
            continue
        name_count += 1
        try:
            getattr(pgi_module, name)
            success_count +=1
            status = STATUS_OK
            reason = ""
            if not show_success:
                continue
        except NotImplementedError as e:
            status = STATUS_FAIL
            errlines = str(e).splitlines()
            reason = errlines[0].strip()
            for line in errlines:
                if line.startswith('NotImplementedError:'):
                    reason = line[20:].strip()
                    break
        print("    {} {} \t{}".format(status, name, reason))
    print("  Implements [{}/{}]".format(success_count, name_count))
    print('')

def test_coverage(libname, show_success=True):
    try:
        with suppress_stdout_stderr():
            pgi_lib = __import__('pgi.repository.{libname}'.format(libname=libname), fromlist=[libname])
            gi_lib = __import__('gi.repository.{libname}'.format(libname=libname), fromlist=[libname])
            print("{libname}:".format(libname=libname))
        test_pgi_coverage(gi_lib, pgi_lib, show_success)
    except Exception as e:
        raise
        #print("Skipped because of %s during test" % str(e))

def get_typelibs():
    typelibs = []

    for typelib in glob(TYPELIB_DIR + "/*.typelib"):
        fn = basename(typelib).partition("-")[0]
        typelibs.append(fn)
    return sorted(typelibs)

if __name__=='__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument( '-m', '--mismatches', action='store_true')
    args = parser.parse_args()
    typelibs = get_typelibs()
    for typelib in typelibs:
        test_coverage(typelib, show_success = not args.mismatches)
