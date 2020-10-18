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

### b) Function call

### c) Sheet variable with initialization list

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

