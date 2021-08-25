#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 21 16:59:09 2021

@author: simone
"""

import functools
import itertools
import numpy
import operator
from pandas.core.common import flatten


c = [[1, 2],
 [[70, 16],
  [74, 9],
  [87, 18],
  [85, 52],
  [55, 81],
  [49, 28],
  [58, 91],
  [82, 83],
  [82, 23],
  [60, 10]]]


def functools_reduce_iconcat(a):
    return functools.reduce(operator.iconcat, a, [])


def numpy_flat(a):
    return list(numpy.array(a).flat)


#res = functools_reduce_iconcat(c)
#res = numpy_flat(c)
#res = functools.reduce(operator.concat, c)
res = list(flatten(c))
res = np.array(res).reshape(-1,2)
print(res)
