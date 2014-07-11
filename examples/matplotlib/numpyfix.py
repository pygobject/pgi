# Copyright 2014 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

"""Basic Python implementation of numpy.linalg.inv/det"""

import numpy as np


def _det(a, *args, **kwargs):
    if args or kwargs:
        raise NotImplementedError("args")

    a = np.array(a)
    if a.shape == (1, 1):
        return a[0,0]
    elif a.shape == (2, 2):
        return a[0,0] * a[1,1] - a[0,1] * a[1,0]
    elif a.shape == (3, 3):
        det = a[0,0] * (a[1,1] * a[2,2] - a[1,2] * a[2,1])
        det -= a[0,1] * (a[1,0] * a[2,2] - a[1,2] * a[2,0])
        det += a[0,2] * (a[1,0] * a[2,1] - a[1,1] * a[2,0])
        return det
    else:
        raise NotImplementedError("shape")


def _inv(a, *args, **kwargs):
    if args or kwargs:
        raise NotImplementedError("args")

    a = np.array(a)
    if a.shape == (1, 1):
        return a
    elif a.shape == (2, 2):
        r = np.zeros(a.shape)

        r[0,0] = a[1,1]
        r[0,1] = -a[0,1]
        r[1,0] = -a[1,0]
        r[1,1] = a[0,0]
        return (1.0 / np.linalg.det(a)) * r
    elif a.shape == (3, 3):
        r = np.zeros(a.shape)

        r[0,0] = a[2,2] * a[1,1] - a[2,1] * a[1,2]
        r[0,1] = -(a[2,2] * a[0,1] - a[2,1] * a[0,2])
        r[0,2] = a[1,2] * a[0,1] - a[1,1] * a[0,2]

        r[1,0] = -(a[2,2] * a[1,0] - a[2,0] * a[1,2])
        r[1,1] = a[2,2] * a[0,0] - a[2,0] * a[0,2]
        r[1,2] = -(a[1,2] * a[0,0] - a[1,0] * a[0,2])

        r[2,0] = a[2,1] * a[1,0] - a[2,0] * a[1,1]
        r[2,1] = -(a[2,1] * a[0,0] - a[2,0] * a[0,1])
        r[2,2] = a[1,1] * a[0,0] - a[1,0] * a[0,1]

        return (1.0 / np.linalg.det(a)) * r
    else:
        raise NotImplementedError("shape")


def fix():
    try:
        np.linalg.inv(np.identity(1))
    except AttributeError:
        # nppy
        np.linalg.det = _det
        np.linalg.inv = _inv


if __name__ == "__main__":
    fix()

    # Tests
    # 0x0, 1x1
    assert np.linalg.det([[1]]) == 1
    assert np.array_equal(np.linalg.inv([[1]]), [[1]])

    # 2x2
    a = np.array([[1, 2], [3, 4]])
    assert np.linalg.det(a) - -2.0 < 0.0001
    assert np.allclose(np.linalg.inv(a), [[-2., 1.], [1.5, -0.5]])

    # 3x3
    assert np.linalg.det(np.identity(3)) == 1.0
    assert np.linalg.det([[10,2,3],[4,5,6],[7,8,9]]) == -27

    a = [[1,0,0],[-5, 1, 0],[0, 0, 1]]
    b = [[1, 0, 0],[5, 1, 0],[0, 0, 1]]
    assert np.linalg.det(a) == 1.0
    assert np.array_equal(np.linalg.inv(a), b)
    assert np.array_equal(np.dot(np.linalg.inv(a), a), np.identity(3))
