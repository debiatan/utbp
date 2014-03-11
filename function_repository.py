#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import collections
import copy
import itertools
import time

import ground
import topology
import tree
import lis

def contains(expression, variables):
    for element in expression:
        if isinstance(element, tuple):
            if contains(element, variables):
                return True
        else:
            if element in variables:
                return True
    return False

class FunctionRepository(object):
    def __init__(self, fname):
        self.primitives = {}
        self.arities = collections.defaultdict(set)
        self.in_types = collections.defaultdict(set)
        self.out_types = collections.defaultdict(set)

        self.extended_primitives = None
        self.extended_arities = None
        self.extended_in_types = None
        self.extended_out_types = None

        self.target_function_name = None

        self.returned_constants = {}

        self.fname = fname 
        if os.path.exists(self.fname):
            self.derived = self.load()
        else:
            # name: (input_types, output_type, code)
            self.derived = collections.OrderedDict()

        self.interpreter = lis.Interpreter()

        self.consider('if', 'car', 'cdr', 'cons', 'succ', 'pred', 0, 'list?',
                      ('quote', ()))

        for func_name, desc in self.derived.items():
            _, _, code = desc
            self.interpreter.interpret(code)

    def load(self):
        def tokenize(case):
            return case.replace('(',' ( ').replace(')',' ) ').split()

        def read_from(tokens):
            reserved_words = ('quote', 'if', 'define', 'lambda')

            token = tokens.pop(0)
            if '(' == token:
                L = []
                while tokens[0] != ')':
                    L.append(read_from(tokens))
                tokens.pop(0) # pop off ')'
                return L
            else:
                if token.isdigit():
                    return int(token)
                if token in reserved_words:
                    return token
                return lis.Symbol(token)

        def to_tuple(l):
            if isinstance(l, list) or isinstance(l, tuple):
                return tuple([to_tuple(e) for e in l])
            else:
                return l

        def parse(case):
            return to_tuple(read_from(tokenize(case)))

        res = collections.OrderedDict()
        with open(self.fname) as f:
            for line in f:
                name, desc = [e.strip() for e in line.split(':')]
                tuple_desc = parse(desc)
                res[name] = tuple_desc
        return res

    def save(self):
        def to_tuple_string(l):
            if isinstance(l, list) or isinstance(l, tuple):
                res = ' '.join([to_tuple_string(e) for e in l])
                return '('+res+')'
            else:
                return str(l)

        with open(self.fname, 'w') as f:
            for func_name, description in self.derived.items():
                desc_string = to_tuple_string(description)
                f.write(func_name+': '+str(desc_string)+'\n')

    def consider(self, *func_names):
        for func_name in func_names:
            assert func_name in self.derived or func_name in ground.primitives
            if func_name in self.derived:
                in_types, out_type, code = self.derived[func_name]
                self.interpreter.interpret(code)
                self.teach_primitive(func_name, (in_types, out_type))
            elif func_name in ground.primitives:
                self.teach_primitive(func_name, ground.primitives[func_name])

    def _reset(self):
        self.primitives.clear()
        self.arities.clear()
        self.in_types.clear()
        self.out_types.clear()

    def teach_primitive(self, func_name, f):
        self.primitives[func_name] = f
        in_types, out_type = f

        self.arities[len(in_types)].add(func_name)

        self.in_types[in_types].add(func_name)

        # Find all ascendant and descendant output types
        for typ in ground.type_tree.find(out_type).ascendants():
            self.out_types[typ].add(func_name)
        for typ in ground.type_tree.find(out_type).descendants():
            self.out_types[typ].add(func_name)

    def available_functions(self):
        return tuple(self.primitives.keys())

    def _check(self, name, code, examples):
        res = self.interpreter.interpret(code)
        if res != None:
            # Sanity check
            import ipdb; ipdb.set_trace() # EVIL_DEBUG

        for question, answer in examples:
            # TODO: If I ever get to implement functions as first-class objects,
            # I'll have to make sure to assign Symbol status to some arguments
            q = (lis.Symbol(name),)+question

            try:
                interpreter_answer = self.interpreter.interpret(q)
            except:
                return False

            if interpreter_answer != answer:
                return False

        return True

    def fit(self, name, in_names, in_types, out_type, examples, debug=False):
        """
        self.typed_trees.func.reset() # Forget previous runs 
                                      # (functools.partial gets in the way)
        """
        self.returned_constants = {}

        if (debug and name in self.derived and 
            self._check(name, self.derived[name][2], examples)):
            if debug:
                print("Definition of '{}' already computed.".format(name))
            return

        self.target_function_name = name

        # Update the dictionaries of available operations with those provided by
        # the parameters of this particular problem
        self.extended_primitives = copy.deepcopy(self.primitives)
        self.extended_arities = copy.deepcopy(self.arities)
        self.extended_in_types = copy.deepcopy(self.in_types)
        self.extended_out_types = copy.deepcopy(self.out_types)

        for param_name, param_type in zip(in_names, in_types):
            self.extended_arities[0].add(param_name)
            self.extended_in_types[()].add(param_name)

            for asc_par_type in ground.type_tree.find(param_type).ascendants():
                self.extended_out_types[asc_par_type].add(param_name)
            for asc_par_type in ground.type_tree.find(param_type).descendants():
                self.extended_out_types[asc_par_type].add(param_name)

        # Include the possibility of recursion
        self.extended_arities[len(in_names)].add(name)
        self.extended_primitives[name] = (in_types, out_type)

        # Find all descendant type combinations that match our types
        for tc in ground.descendant_combinations(in_types):
            self.extended_in_types[tc].add(name)

        for asc_par_type in ground.type_tree.find(out_type).ascendants():
            self.extended_out_types[asc_par_type].add(name)

        # Restrict possible shapes of trees to those with present arities
        n_nodes = 1
        found = False

        while not found:
            if debug: print('Nodes:', n_nodes)
            t0 = time.time()
            n_evaluations = 0
            for t in self.typed_trees(n_nodes, out_type, in_names,
                                      verbose=False):
                code = ('define', name, ('lambda', in_names, t))

                n_evaluations += 1
                found = self._check(name, code, examples)
                if found: break

            n_nodes += 1
            t1 = time.time()
            if debug:
                print('%d evals, %.2f seconds, %g s/eval'%(n_evaluations, 
                                                           t1-t0,
                                                           (t1-t0)/\
                                                           (n_evaluations+1)))

        if debug:
            print('Found!')
            print(code)
            t = tree.Tree.from_code(code)
            print(t)

        self.derived[name] = (in_types, out_type, code)
        self.save()

        self.target_function_name = None

        return code

    #@Memo
    def typed_trees(self, n_nodes, out_type, var_names, verbose = False):
        if n_nodes == 1:
            compatible_fs = (self.extended_arities[0] & 
                             self.extended_out_types[out_type])
            for f in compatible_fs:
                if isinstance(f, int) or f == ('quote', ()):
                    if f not in self.returned_constants:
                        self.returned_constants[f] = (n_nodes, f)
                        if verbose: print('--->', f)
                        yield f
                    elif self.returned_constants[f] == (n_nodes, f):
                        if verbose: print('--->', f)
                        yield f
                    # else: this constant should have been returned earlier
                else:
                    if verbose: print('--->', f)
                    yield lis.Symbol(f) 
        else:
            arities = sorted([arity for arity in self.extended_arities.keys() 
                              if arity>0 and arity<n_nodes], reverse=True)
            for arity in arities:
                compatible_fs = (self.extended_out_types[out_type] &
                                 self.extended_arities[arity])
                for f in compatible_fs:
                    inputs = self.extended_primitives[f][0]
                    # Find all the possible combinations of arities that sum
                    # up to the target arity-1. Then find the typed_trees
                    # with those arities and plug them to the candidate
                    # function for evaluation
                    # This is going to get ugly fast
                    for part in topology.limited_partitions(n_nodes-1, arity):
                        parametrizations = [list(e)+[var_names] 
                                            for e in zip(part, inputs)]

                        for children in itertools.product(
                            *(self.typed_trees(*parametrization)
                              for parametrization in parametrizations)):
                            if (self.target_function_name != f and
                                not contains(children, var_names)):
                                # Constant
                                try:
                                    code = (lis.Symbol(f),)+children
                                    k = self.interpreter.interpret(code)
                                except:
                                    k=None

                                if k != None:
                                    if k not in self.returned_constants:
                                        self.returned_constants[k] = (n_nodes,
                                                                      code)
                                        if verbose: print('--->', k)
                                        yield k
                                    elif self.returned_constants[k] == (n_nodes,
                                                                        code):
                                        if verbose: print('--->', k)
                                        yield k
                                    # else: this constant should have been 
                                    #   returned earlier. Don't return anything
                            else:
                                if verbose: print('--->', f, children)
                                yield (lis.Symbol(f),)+children
