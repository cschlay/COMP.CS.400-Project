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

### Defining Rules

### PLY Processing

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

