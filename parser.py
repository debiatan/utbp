#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ast

def parse_arg(arg):
    t = type(arg).__name__

    if t == 'Num':
        return arg.n
    elif t == 'Str':
        return arg.s
    elif t == 'Tuple':
        return tuple([parse_arg(e) for e in arg.elts])
    elif t == 'Name' and arg.id in ('True', 'False'):
        return arg.id == 'True'
    elif t == 'UnaryOp' and type(arg.op).__name__ == 'USub':
        # Necessary for python 3.2
        return -arg.operand.n
    else:
        print('Unexpected problem parsing expression')
        import ipdb; ipdb.set_trace() # EVIL_DEBUG

class CallParser(ast.NodeVisitor):
    def __init__(self):
        self.name = None
        self.values = []

    def visit_Call(self, node):
        self.name = node.func.id
        self.values = tuple([parse_arg(arg) for arg in node.args])

def parse_call(exp):
    visitor = CallParser()
    visitor.visit(ast.parse(exp))
    return visitor.name, visitor.values

class ExprParser(ast.NodeVisitor):
    def __init__(self):
        self.v = None

    def visit_Expr(self, node):
        self.v = parse_arg(node.value)

def parse_expression(exp):
    visitor = ExprParser()
    visitor.visit(ast.parse(exp))
    return visitor.v
