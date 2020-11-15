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

## 3. Tree structure

Notice that `TYPE_` prefixed are constants defined in `sssyntax.py` and referred here as such.

### a) Variable definitions

In my implementation I think it could have been reduced because the `p_variable_definition` only
had one child that referred to `scalar_definition`, `range_definition`, and `sheet_definition`.

So in this answer I we take a closer look to those three.

In scalar definition I have a nodetype called `TYPE_SCALAR_DEFINITION` that has two possible structure
the node has name `child_name` which is the variable name. Then optionally `child_scalar_expr` if expression
is given. In short, it should look something like:

```
scalar_definition:
    name: scalar (THE_IDENT)
    expression: THE_EXPRESSION
```

For range definition we have similar structure and the result should be similar

```
range_definition:
    name: RANGE_IDENT (THE_IDENT)
    expression: THE_EXPRESSION```
```

The sheet_init has mostly same structure except there isn't expression. 
Instead of `expression` there is `child_sheet_init`.

```
range_definition:
    name: SHEET_INIT (THE_IDENT)
    sheet_init: THE_SHEET```
```

### b) For loop

The for loop is only defined inside `p_statement`. In there I defined
nodetype `TYPE_FOR`. As the thing between `FOR range_list DO statement_list DONE` the
keywords there can be multiple of those so they return lists and they get passed as children
`chilren_range_list` and `children_statement_list` to make it easier to iterate later.

The end result should be something like:

```
for:
    range_list[0]: 
        ...
    range_list[n]:
        ...
    statement_list[0]:
        ...
    statement_list[m]:
        ...
```

The list arguments printed in the tree with the number is just the order of range is written and statements are also ordered.
We can be sure that statement `0` writen before `m` can be iterated in that order.

### c) Function call

TODO

## 4.

## 5.

## 6.
