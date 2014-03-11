#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tree import Tree
import itertools

"""
Types:                      Constants defined for each type:
    S-expression
    ├── list ------------->     quote ()
    └── number ----------->     0
"""
type_tree = Tree.from_tuple(('S-expression', 
                             ('list',),
                             ('number',))) 

def descendant_combinations(types):
    return itertools.product(*[type_tree.find(e).descendants() for e in types])

# List of primitive functions along with their type contract
primitives = {
    #name           : ((input_types,),                      output_type)
    'list?'         : (('S-expression',),                   'number'),
    'if'            : (('S-expression', 'S-expression', 
                        'S-expression'),                    'S-expression'),
    'car'           : (('list',),                           'S-expression'),
    'cdr'           : (('list',),                           'list'),
    'cons'          : (('S-expression', 'list'),            'list'),
    'succ'          : (('number',),                         'number'),
    'pred'          : (('number',),                         'number'),
    # Literals
    ('quote', ())   : ((),                                  'list'),
    #'(quote ())'    : ((),                                  'list'),
    0               : ((),                                  'number')
    #'0'             : ((),                                  'number')
    # 'auto' : Same inputs and outputs as the function we're defining
    # 'null?': Not explicitly given; the truth value associated to each object
    #          already evaluates to false if it is null
    # 'eq?'  : Can be built around the rest of operations for lists and numbers
}
