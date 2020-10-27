# Document for Phase 2

The unittest can be run in this directory with:

```
python -m unittest
```

To process a file run:

```
python main.py -f FILENAME
```

## 1. Syntax analysis

Syntax analysis checks the code that was previously run through
lexical analysis. At this phase comments and other ignored tokens are
removed. In this phase, the tokens are assumed to be correct.

The purpose is to check that the syntax is correct and perhaps build an _abstract syntax tree_ (AST).
After the AST is built, the code can be interpret or compiled to intermediate language.

In the PLY docs, some tokens were converted to Python objects and e.g. math operations were performed.
So some optimization can be done with syntax analysis too.


## 2. Syntactic Structure in PLY

One need to mostly define the grammar, the structure of processing
is quite similar as in phase 1 where lex was used.

### Defining Rules

The rules are defined simply by defining a function as

```python
def p_rulename(p):
    """rulename : tokens or other rules as sequence
                | tokens or other rules as sequence
    """
    p[0] = p[1]
```

The `p[0]` need to always be assigned otherwise we are unable
to access it from other rules. The PLY recommended two approach putting
it as `Tuple` or constructing objects. I preferred to use
objects because I think it is hard to use array or tuple indices.

### PLY Processing

After the rules are defined the overall structure of program would be.

```python
import ply.yacc
import sslexer
from typing import List
P = [ply.yacc.YaccProduction]


tokens: List[str] = sslexer.tokens

def p_rulename(p: P):
    """rulename : the grammar here
    """
    p[0] = p[1]  # Need to assign something to pass forward


def p_error(p: P):
    pass


parser: ply.yacc.LRParser = ply.yacc.yacc()


def parse_data(data: str):
    parser.parse(data, lexer=sslexer.lexer, debug=False)
```

The tokens need to be imported from the lexer module.
After that the grammar rules need to be defined and possibly the error rule too.
Finally the parse need to be invoked and feed some data.
The lexer from phase 1 need to be passed as argument.


## 3. Syntax of Elements

### a) Sheet variable definition

The specification of sheet variable is

```
sheet_definition ::= SHEET SHEET_IDENT [sheet_init]
```

As I undershoot it the concrete use is something like `sheet NAME` and `sheet SH = 2 * 2` or `sheet SH = {2.0 * 2.0}`.
The first rule without the optional `sheet_init` seem to be just
a declaration of a variable.
When we do use `sheet_init` we have another rules that defines the `=` symbol which might be
assignment for sheet variables. However, there exist a different assignment token.

And the value can be either and integer multiplication or
a set-like structure `{elem1, elem2}`, where elements can be a valid `simple_expr` (arithmetic) or another variable. 

### b) Function call

The function call is specified as

```
function_call ::= FUNC_IDENT LSQUARE [ arguments ] RSQUARE
```

which means the first token must be `FUNC_IDENT` a valid function name.
Then we have `LSQUARE` and `RSQUARE` so we have something like 

```
Eat_ice_cream[]
```

as a function call if no arguments are given. And they are given they
are defined in `arguments`. Which is specifies as

```
arguments  ::= arg_expr { COMMA arg_expr }
```

and that just means `arg_expr` things can be given separated by `COMMA`, `,`.

The an argument must be `scalar_expr`, `range_expr` or `SHEET_IDENT`.
Scalar expression allows arithmetics and range expressions range for example:

```
Sell_ice_cream[1.0+1.0, range CELL_REF_HERE .. CELL_REF_HERE]
```

### c) Sheet variable with initialization list

As mentioned in a) I think the sheet with initialization list a set-like structure.
If we take a look at what elements can be put there it has
`simple_expr` which can be `term` itself which means it can be `atom` a decimal or a variable name or function call or
other expressions. Atom was specifies such that it can reach `simple_expr` again which defines more valid syntax.

It looks like it accepts a boolean-like values because it and have equality comparison as value.
It can also have arithmetic operations with other expressions. This allows complex sheets such as

```
sheet SH = {2+4/6, variable1 <= variable2}
sheet HH = {2+4+6*12, variable1 <= 9}
```

## 4. Syntax Definition

### a) Nested functions

It doesn't seem to be possible to define nested functions because the only reference to
`function_definition` is `function_or_variable_definition` and 
only the definition of `program` uses it. It doesn't have any way to reach
the `function_definition` again because the only possibilities
are `variable_definition` or `statement_list` but neither rule allows
`function_definition`.

### b) Arithmetics with integers

I don't think it is possible, and it didn't work when I checked it.
That is because the specification doesn't include a rule that
could have `INT_LITERAL` as `atom`, which is required to form `term` which is further 
required for `simple_expr` which defines the plus operation.

### c) Range variable with decimals

It doesn't seem to be possible because the plus operation is defined in
`simple_expr` but `range_expr` cannot reach it.

First it attempt to evaluate

```
range_definition ::= RANGE RANGE_IDENT EQ range_expr
```

and then it goes to `range_expr` and then it refers to another `RANGE_IDENT` or cells or range expression.


### d) Validity of `xx--yy` and `--xx`

I think `xx--yy` might be possible because it would evaluate
as follows:

```
ATOM = xx
ATOM = yy
FACTOR = xx
FACTOR = -yy
TERM = xx
TERM = -yy
SIMPLE_EXPR = xx--yy
```

However, the `--xx` isn't possible because `factor` only defines
one minus an it cannot refer to itself. The `simple_expr` that would add 
another minus cannot do it because it doesn't have another `term`.

### e) Comparison in sheet init

It is not possible to do comparison in `sheet_init_list`.
There reason is that the `sheet_init_list` uses `sheet_row` but
it uses `simple_expr` which doesn't reach to `scalar_expr` which has
all equality comparison operators.

### f) Addition/Subscription after multiplication/division

The definition ensures this by having rule `term` which does
the multiplication and division.
Only after the `term` is constructed the `simple_expr` uses
the `terms` so at this point they have already evaluated terms
so plus and minus operations are applied after.

### g) Statement and definition endings

A statement has unique start symbol such as `FOR`, `IF`, and idents.
Some have `DONE` and `ENDIF` as the ending mark.

The ident tokens also have unique syntax so when it starts with one of them
we know it is an assignment and that is the most complex one. But
there is no conflicts so it can be thought that only assignment can do stuff the specific
statements can't. Variable definitions can be detected by `scalar`, `range`, `sheet` keywords and their lengths
are known so that limits the conflicts.

## 5. Other remarks

## 6. Thoughts

I think this phase had much more work, but the similar 
program structure as in phase 1 was possible.

I also found out I had missed `SHEET` keyword in lexer.
But the parser was still quite straightforward except that
I wasn't sure what should be assigned to `p[0]`.

I think the difficulties was in the beginning and not being sure 
what should be assigned to `p[0]`. I decided to create objects as 
the docs recommended it as another way. However, I mostly skipped constructing objects with functions and subroutines
because I wasn't sure how it will be used and it might be more of later phase thing AST construction
where the use is better known.

I think defining rules in general is easy if the language is already specified.
But I think defining multiple and optional things in syntax is hard because
it required recursive thinking.

Unlike in the first phase I found it impossible to test the thing properly using unittest and assert
console outputs.

I learned more about language processing, and I think I can write
a mini-interpreter with the knowledge of these two first phases.
