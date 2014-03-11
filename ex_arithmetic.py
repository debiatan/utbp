#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utbp import UTBP

@UTBP
def add(a, b):
    """
    add(2, 2) == 4
    add(3, 3) == 6
    """

@UTBP
def mul(a, b):
    """
    mul(2, 2) == 4
    mul(3, 5) == 15
    """

@UTBP
def power(a, b):
    """
    power(1, 1) == 1
    power(2, 3) == 8
    power(5, 3) == 125
    power(5, 2) == 25
    power(5, 0) == 1
    """

@UTBP
def factorial(n):
    """
    factorial(0) ==  1
    factorial(1) ==  1
    factorial(2) ==  2
    factorial(3) ==  6
    """

if __name__ == '__main__':
    assert add(23, 23) == 46
    assert mul(8, 8) == 64
    assert power(2, 4) == 16
    print(factorial(4))
