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

### b) Arithmetics with integers

### c) Range variable with decimals

### d) Validity of `xx--yy` and `--xx`

### e) Comparison in sheet init

### f) Addition/Subscription after multiplication/division

### g) Statement and definition endings

## 5. Other remarks

## 6. Thoughts

