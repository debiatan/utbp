#!/usr/bin/env python
# -*- coding: utf-8 -*-

import itertools
import functools
from types import GeneratorType

Tee = itertools.tee([], 1)[0].__class__

class Memo(object):
    def __init__(self, f):
        self.f = f
        functools.update_wrapper(self, f)
        self.cache = {}

    def __get__(self, obj, objtype=None):
        """ Support instance methods """
        if obj is None:
            return self.f
        return functools.partial(self, obj)

    def __call__(self, *args):
        if args not in self.cache:
            self.cache[args]=self.f(*args)

        # Support generators
        if isinstance(self.cache[args], (GeneratorType, Tee)):
            self.cache[args], r = itertools.tee(self.cache[args])
            return r

        res = self.cache[args]
        return res

    def reset(self):
        self.cache = {}
