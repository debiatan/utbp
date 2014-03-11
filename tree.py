#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Tree(object):
    def __init__(self, id):
        self.id = id
        self.parent = None
        self.children = []

    def add_child(self, node):
        self.children.append(node)
        node.parent = self

    def find(self, id):
        if self.id == id:
            return self
        for child in self.children:
            res = child.find(id)
            if res: return res

        return None

    def ascendants(self):
        res = []
        if self.parent:
            res += self.parent.ascendants()
        res += [self.id]
        return res

    def descendants(self):
        res = [self.id]
        for child in self.children:
            for des in child.descendants():
                res.append(des)

        return res

    @staticmethod 
    def from_tuple(tuple_tree):
        name = tuple_tree[0]
        root = Tree(name)
        for node in tuple_tree[1:]:
            root.add_child(Tree.from_tuple(node))

        return root

    @staticmethod 
    def from_code(code_tree):
        # FIXME: I just wanted to use the __str__ method of this class for code
        # objects, so I forced this function here
        if isinstance(code_tree, tuple):
            if code_tree == ():
                name = ()
            else:
                name = code_tree[0]

            root = Tree(name)
            if name == 'lambda':
                child = Tree(' '.join(str(e) for e in code_tree[1]))
                root.add_child(child)
                for node in code_tree[2:]:
                    root.add_child(Tree.from_code(node))
            else:
                for node in code_tree[1:]:
                    root.add_child(Tree.from_code(node))
        else:
            root = Tree(code_tree)

        return root

    def __str__(self):
        return '\n'.join(self._tree_lines())

    def _tree_lines(self):
        """
        Adapted from: http://www.acooke.org/cute/ASCIIDispl0.html
        Tue Sep 24 08:07:25 CEST 2013 - Code was listed as public domain
        """
        yield str(self.id)

        last = self.children[-1] if self.children else None
        for child in self.children:
            prefix = '└── ' if child is last else '├── '
            for line in child._tree_lines():
                yield prefix + line
                prefix = '    ' if child is last else '│   '

    def code(self):
        if self.id[:5] == 'cond_':
            return '(if {} {} {})'.format(self.children[0].code(),
                                          self.children[1].code(),
                                          self.children[2].code())

        res = self.id
        if self.children:
            res = '('+res+' ' + \
                    ' '.join([child.code() for child in self.children])+ ')'
            
        return res

if __name__ == '__main__':
    type_tree = ('S-expression', 
                 ('list',), 
                 ('atom', 
                  ('string',), ('number',), ('bool',)))

    t = Tree.from_tuple(type_tree)
    print(t)

    print("\nLooking for 'atom':")
    node = t.find('atom')
    print('id:', node.id)
    print('ascendants:', node.ascendants())
    print('descendants:', node.descendants())
