#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utbp import UTBP

@UTBP
def index(l, a):
    """
    index((4, 7, 8), 1) == 7
    index((4, 7, 8), 2) == 8
    index(((4, 7), 8), 0) == (4, 7)
    """

@UTBP
def length(l):
    """
    length(()) == 0
    length((2, 2, 2, 2, 2)) == 5
    """

@UTBP
def add(a, b):
    """
    add(2, 2) == 4
    add(3, 3) == 6
    """

@UTBP
def sum(l):
    """
    sum((2, 2)) == 4
    sum((3, 3, 3)) == 9
    """


if __name__ == '__main__':
    assert index((2, 3, 4), 1) == 3
    assert length((4, 4, 4)) == 3
    assert add(23, 23) == 46
    assert sum((8, 8, 8, 8)) == 32
