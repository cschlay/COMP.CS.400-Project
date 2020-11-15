# Document for Phase 3

## 1. Abstract Syntax Tree

_Abstract syntax tree_ is based on the syntax rules we have defined.
It follows a data structure called _tree_, not necessarily binary one.
At least in this assignment we have more than two child nodes.

The idea of constructing AST is to ease the interpretation or compilation because
the data structure is tree we can traverse it easily can have clear meaning for each child nodes.

The AST is constructed after syntax analysis (phase 2). 

## 2. Syntax tree with AST

We need the code base for syntax analysis first (done in phase 2).
In PLY the rule is something like

```
def p_rule(p):
    """rule | rule1 rule 2"""
    p[0] = nodes.Node()
```

And we only need to assign something to `p[0]`, in this exercise it
is the `Node` object which has to comfort the properties we were given.
The purpose is for those limitations are because we wanted to print it.

If we were to write something else we could assign anything else to it.

The most important is to have root node which in our case in `p_program`.
The call `parser.parse(data, lexer=sslexer.lexer, debug=False)` returns the
root node.

Each rule need to assign a node and we can construct new nodes from nodes e.g. 

```
p[0] = nodes.Node(nodetype="node1", child_left=p[1], child_right=p[2]
```

In this case we use the node that was assigned in other rules.

