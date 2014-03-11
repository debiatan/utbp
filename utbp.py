#!/usr/bin/env python
# -*- coding: utf-8 -*-

import parser
import inspect
from function_repository import FunctionRepository
import lis
import tree

frep = FunctionRepository('defs.exh')

class UTBP(object):
    def __init__(self, f):
        self.f = f
        self.name = f.__name__
        #self.fname = inspect.getfile(f)
        self.ready = False

    def _prepare(self):
        f = self.f
        self.arg_names = tuple(inspect.getargspec(f).args)
        self.n_args = len(self.arg_names)
        self.use_cases = self._parse_use_cases(f.__doc__)

        self.arg_types = tuple([self._type_signature([use_case[0][i] 
                                                      for use_case in
                                                      self.use_cases]) 
                                for i in range(self.n_args)])
        self.return_type = self._type_signature([use_case[1] for use_case 
                                                 in self.use_cases])

        lisp_use_cases = tuple([self._lisp_use_case(use_case)
                                for use_case in self.use_cases])

        frep.fit(self.name, self.arg_names, self.arg_types,
                 self.return_type, lisp_use_cases, debug=True)
        frep.consider(self.name)
        self.ready = True

    def _parse_use_cases(self, docstring):
        examples = [[e.strip() for e in l.split('==')] 
                    for l in docstring.strip().split('\n')]

        use_cases = []
        for exp, outcome_exp in examples:
            name, args = parser.parse_call(exp)
            assert name == self.name
            assert len(args) == self.n_args
            outcome = parser.parse_expression(outcome_exp)
            use_cases.append((args, outcome))

        return use_cases

    def _lisp_use_case(self, use_case):
        args, outcome = use_case
        res_arg = []
        for arg in args:
            res_arg.append(self._to_lisp_syntax(arg, quote=True))

        # Arguments as tuples, outcome value as ints and tuples
        return (tuple(res_arg), outcome)

    def _to_lisp_syntax(self, a, quote=False):
        if type(a).__name__ == 'int':
            return a
        elif type(a).__name__ == 'tuple':
            res = tuple(self._to_lisp_syntax(e) for e in a)
            if quote:
                res = ('quote', res)
            return res
        else:
            assert False

    def _type_signature(self, values):
        types = [type(v).__name__ for v in values]
        d = {'int':'number', 'tuple':'list'}

        assert types[0] in ('int', 'tuple')
        if len(set(types)) == 1:
            return d[types[0]]
        else:
            return 'S-expression'

    def __str__(self):
        if not self.ready:
            self._prepare()
        t = tree.Tree.from_code(frep.derived[self.name][2])
        return str(t)

    def __call__(self, *args):
        if not self.ready:
            self._prepare()

        res_arg = []
        for arg in args:
            res_arg.append(self._to_lisp_syntax(arg, quote=True))

        # TODO: arguments could also be symbols in the case of functions as
        # first-class objects
        q = (lis.Symbol(self.name),) + tuple(res_arg)
        res = frep.interpreter.interpret(q)
        return res
