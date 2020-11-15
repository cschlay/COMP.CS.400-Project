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

## 4. About implementation
   
### a) Empty childs

I think it shouldn't be possible to happen anywhere unless there are errors in the code
such as invalid `len(p)` checks. I found some of those that were incorrectly set in phase 2.

I have purposely set those length checks so that they construct slightly different nodes based on 
the syntax. So if e.g. `p_program` doesn't have variable definitions then the only child constructed is `children_statement_list` and
that cannot be `None` or `[]` because it would be syntax error as the further rules require it to have a valid `statement`.

### b) Simplifications

Yes, there are I list them below by rule name. Mostly the purpose is that I can pass list as `children_` or
I think there is no purpose for it e.g. single child, helpers, and syntactical (brackets or so).
I denoted them as such below.

- `p_multiple_function_or_variable_definition`, list
- `p_function_or_variable_definition`, single
- `p_variable_definition`, single
- `p_scalar_or_range`, helper
- `p_multiple_variable_definition`, helper, list
- `p_formal_arg`, list
- `p_sheet_init_list`, brackets
- `p_multiple_sheet_row`, list
- `p_statement_list`, list
- `p_statement`, only `assignment` and `subroutine_call`, single
- `p_range_list`, list
- `p_arguments`, list
- `p_arg_expr`, only for `scalar_expr` and `range_expr`, single
- `p_scalar_expr`, only for the single `simple_expr`
- `p_scalar_op`, helper
- `p_simple_expr`, only for single `term`
- `p_term`, only for single `factor`
- `p_factor`, only for single `atom`
- `p_atom`, only for `range_expr` and `scalar_expr` because don't know if number sign is necessary for `range_expr`. The `scalar_expr` because of brackets.

## 5.

## 6.

I think it took some time think and wonder how the tree should look like.
I attempted to follow the example output but didn't do so in for every rule because it was
easier to define them other way.

The difficulty I had was that there are nodes printed as

```
sheet_init: sheet_init
```

which were hard to resolve to look better but I did what I could.

Another hard thing was how to name things properly because in the public examples
they looked like the names followed the concept of the syntax such as idents are all childs named `name` but
when it is not obvious I resorted to just the child same as rule name.

The easiest part was that things could be converted from phase 2 which was quite clear.

I learned more about constructing the tree although some primitive attempt was done in phase 2 to make it print the rule calls.
So a great improvement happened.
