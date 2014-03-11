#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utbp import UTBP

@UTBP
def add(a, b):
    """
    add(2, 2) == 4
    add(3, 3) == 6
    """

assert add(23, 23) == 46


