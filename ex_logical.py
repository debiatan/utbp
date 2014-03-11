#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utbp import UTBP

@UTBP
def logical_not(a):
    """
    logical_not(1) == 0
    logical_not(0) == 1
    """

@UTBP
def logical_or(a, b):
    """
    logical_or(0, 0) == 0
    logical_or(0, 1) == 1
    logical_or(1, 0) == 1
    logical_or(1, 1) == 1
    """

@UTBP
def logical_and(a, b):
    """
    logical_and(0, 0) == 0
    logical_and(0, 1) == 0
    logical_and(1, 0) == 0
    logical_and(1, 1) == 1
    """

@UTBP
def logical_nand(a, b):
    """
    logical_nand(0, 0) == 1
    logical_nand(0, 1) == 1
    logical_nand(1, 0) == 1
    logical_nand(1, 1) == 0
    """

@UTBP
def logical_xor(a, b):
    """
    logical_xor(0, 0) == 0
    logical_xor(0, 1) == 1
    logical_xor(1, 0) == 1
    logical_xor(1, 1) == 0
    """

@UTBP
def logical_parity(l):
    """
    logical_parity((0,)) == 0
    logical_parity((1,)) == 1
    logical_parity((0, 0)) == 0
    logical_parity((0, 1)) == 1
    logical_parity((0, 0, 0)) == 0
    logical_parity((0, 0, 1)) == 1
    logical_parity((0, 1, 1)) == 0
    """

if __name__ == '__main__':
    assert logical_not(1) == 0
    assert logical_or(1, 1) == 1
    assert logical_and(1, 1) == 1
    assert logical_nand(1, 1) == 0
    assert logical_xor(1, 1) == 0
    assert logical_parity((1, 1, 1, 1, 0, 0, 1, 1)) == 0
