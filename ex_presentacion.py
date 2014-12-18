#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utbp import UTBP

@UTBP
def length(l):
    """
    length(()) == 0
    """

if __name__ == '__main__':
    l = (4, 4, 4)
    n = length(l)
    print 'La longitud de la lista l es', n, 'porque el código de length es:'
    print length
