#!/usr/bin/env python
# -*- coding: utf-8 -*-

################ Lispy: Scheme Interpreter in Python
## (c) Peter Norvig, 2010; See http://norvig.com/lispy.html
################ 
# And some changes by Miguel Lechón (2013 and 2014)

#import memoize

class Symbol(str):
    ''' Subclass of string that makes sure no indexing or slicing happens '''
    def __getitem__(self, *args):
        raise TypeError
    def __getslice__(self, *args):
        raise TypeError

def atom(token):
    ''' Numbers become numbers; every other token is a symbol '''
    if token.isdigit():
        return int(token)
    else:
        return Symbol(token)

class Interpreter(object):
    def __init__(self):
        self.env = {'cons':lambda x,y:[x]+y, 'car':lambda x:x[0], 
                    'cdr':lambda x:x[1:], 
                    'list?':lambda x: 1 if isinstance(x, tuple) else 0,
                    'succ':lambda x:x+1, 'pred':lambda x:x-1}

        self.limits = {}

    def interpret(self, s):
        return self.eval(s, self.env)

    #@memoize.Memo
    def eval(self, x, env):
        '''Evaluate an expression in an environment.'''

        if isinstance(x, Symbol):             # variable reference
            return env[x]
        elif not isinstance(x, tuple):         # constant literal
            return x                
        elif x[0] == 'quote':          # (quote exp)
            (_, exp) = x
            return exp
        elif x[0] == 'if':             # (if test conseq alt)
            (_, test, conseq, alt) = x
            return self.eval((conseq if self.eval(test, env) else alt), env)
        elif x[0] == 'define':         # (define var exp)
            (_, var, exp) = x
            env[var] = self.eval(exp, env)
        elif x[0] == 'lambda':         # (lambda (var*) exp)
            (_, vars, exp) = x

            def lamba_factory(*args):
                env_with_bindings = dict(env)
                env_with_bindings.update(zip(vars, args))
                return self.eval(exp, env_with_bindings)

            return lamba_factory

        else:                          # (proc exp*)
            exps = tuple([self.eval(exp, env) for exp in x])

            proc = exps[0]
            proc_name = x[0]

            def nested_tuple_len(t):
                '''
                Returns the sum of the total number of elements and the total 
                numbers of nested tuples 
                '''
                count = 0
                for e in t:
                    count += 1
                    if isinstance(e, list):            
                        count += nested_tuple_len(e)
                return count

            magnitudes = [nested_tuple_len(e) if isinstance(e, tuple) 
                          else abs(e) for e in exps[1:]]
            if proc_name not in self.limits:
                self.limits[proc_name] = magnitudes
                try:
                    res = proc(*exps[1:])
                except:
                    del self.limits[proc_name]
                    raise RuntimeError # Should raise caught exception
                del self.limits[proc_name]
            else:
                allow = False
                for limit, current in zip(self.limits[proc_name], magnitudes):
                    # At least one of the parameters has to decrease in length
                    # or magnitude (will be problematic once functions are
                    # first-class) TODO
                    if current<limit: 
                        allow = True
                        break
                
                self.limits[proc_name] = [min(pair) for pair in 
                                          zip(self.limits[proc_name], 
                                              magnitudes)]
                if allow:
                    try:
                        res = proc(*exps[1:])
                    except:
                        del self.limits[proc_name]
                        raise RuntimeError # Should raise exception caught
                else:
                    del self.limits[proc_name]
                    raise RuntimeError # Something more explicit?

            return res
