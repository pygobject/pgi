#!/usr/bin/python
# Copyright 2015 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

import os
import sys
import json
import argparse
import subprocess

import datadiff


def get_json(typelib_path, skip_abi):
    dir_ = os.path.dirname(os.path.realpath(__file__))
    tdump_path = os.path.join(dir_, "tdump.py")
    args = [sys.executable, tdump_path, typelib_path]
    if skip_abi:
        args.append("--skip-abi")
    json_data = subprocess.check_output(args).decode("utf-8")
    return json.loads(json_data)


def main(argv):
    parser = argparse.ArgumentParser(
        description='Diff typelibs')
    parser.add_argument('typelib_a', help='Path to typelib A')
    parser.add_argument('typelib_b', help='Path to typelib B')
    parser.add_argument('--skip-abi', action='store_true',
                        help='Don\'t diff info depending on the C ABI')
    args = parser.parse_args(argv[1:])

    json_a = get_json(args.typelib_a, args.skip_abi)
    json_b = get_json(args.typelib_b, args.skip_abi)

    print(datadiff.diff(json_a, json_b))

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
