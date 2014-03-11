#!/usr/bin/env python
# -*- coding: utf-8 -*-

def factorial(n):
    """
    Returns the factorial of n

    int -> int

    >>> factorial(2)
    2
    >>> factorial(3)
    6
    """
    if n:
        return n*factorial(n-1)
    else:
        return 1

print(factorial(1))
print(factorial(2))
print(factorial(3))
print(factorial(4))
