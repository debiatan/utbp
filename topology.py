#!/usr/bin/env python
# -*- coding: utf-8 -*-

import itertools
from memoize import Memo

@Memo
def partitions(total):
    """
    Generates all possible partitions of the strictly positive number _total_
    """
    for taken in range(1, total):
        for p in partitions(total-taken):
            yield (taken,) + p

    yield (total,)          # Base case (total == 1)

@Memo
def limited_partitions(total, n_elems):
    """
    Generates all possible partitions of the strictly positive number _total_
    """
    if n_elems == 1:
        yield (total,)
    else:
        for taken in range(total-1, 0, -1):
            for p in limited_partitions(total-taken, n_elems-1):
                yield (taken,) + p

@Memo
def trees(size, allowed_arity=lambda x: True):
    """
    Generates all unique arbitrary trees of the given strictly positive _size_
    The size of the set is given by the (_size_-1)th Catalan number.
    In case allowed_arity is specified, no node in the generated trees will
    have an arity other than those allowed.
    """
    if size > 1:
        for p in partitions(size-1):
            gen = (trees(e, allowed_arity) for e in p)
            for e in itertools.product(*gen):
                if not allowed_arity(len(e)): continue
                yield tuple(e)
    else:
        yield ()

def catalan(n):
    """
    _n_th Catalan number:
    https://en.wikipedia.org/wiki/Catalan_numbers
    """
    num = 1
    den = 1
    for k in range(2, n+1):
        num *= (n+k)
        den *= k

    return num//den

if __name__ == '__main__':
    for p in limited_partitions(7, 3):
        print(p)

    """
    allowed_arity = lambda x: x in (0, 1, 2, 3)

    results = [0, 1, 1, 2, 5, 13, 36, 104, 309, 939, 2905, 9118, 28964, 
               92940, 300808, 980864] # 3219205, 10626023, 35252867]

    for n_nodes in range(1, len(results)):
        n_trees_experimental = len(list(trees(n_nodes, allowed_arity)))
        print('Number of trees of %2d nodes: %d '%(n_nodes, 
                                                   n_trees_experimental))
        #assert n_trees_experimental == results[n_nodes]
    """
