# Document for Phase 1

This is the attachment document to be submitted for phase 1 of course project.

## 1. Lexical analysis

Lexical analysis creates tokens from source code.
The program used for analysis doesn't know anything about how the code is used.
It only knows the keywords and token structures and attempts to find them.

When all text in the source can be matched to a token.
The tokens in other compilation steps will be further processed such as
checking that the tokens appear in proper order e.g. not performing addition of integer and string.

Running lexical analysis before further processing makes it easier to access each
token and not needing to check that they are correct later. It also prevents unnecessary compilation steps
when the most trivial errors in e.g. keyword typos are found in the first step.

## 2. Lexical structure in PLY

### Defining tokens

To use PLY tool we need to define a list or tuple of token names.
They are UPPERCASE strings  that we use to identify the "categor" they belong to.
It has to be declared as module-level variable named `tokens`.

```
tokens: List[str] = ["TOKEN_NAME"]
```

The token itself then need to be defined using regular expression.
It has to start with `t_` prefix e.g.

```
t_INT = r"-?[0-9]+"
```

The special tokens for PLY are `t_ignore` and `t_ignore_` prefixed tokens.
They do not become tokenized. We also need to define `t_newline` if we want line numbering.

The tokens can be defined as functions too but it has to strictly follow the structure of

```
def t_INT(t):
    r"-?[0-9]+"
    # Do someting else like changing types or or values.
    return t
```

The first line function need to be regular expression!


### Defining keywords

In addition we may be _reserved keywords_, which has special
meaning in the language that user shouldn't use as variables.
Those are also defined as tokens but according to PLY documentation, they
should be defined as dictionary because it improves efficiency.

The documentation has recommends using the structure of

```
reserved: Dict[str, str] = {
    "keyword": "KEYWORD"
}
```

Although the keyword is identical but uppercase it may vary and 
such as being case sensitive the string token need to be different and unique.
The uppercase part need to be appended to tokens list. 
Python has convenient function `Dict.values` which can just be called.

Then we need to remember that when we validate the keywords for some tokens
they need to be defined as functions and validate them by replacing the
type

```
t.type = reserved.get("keyword", "TOKEN_TYPE_TO_VALIDATE")
```

This is not specific to PLY, but the easiest way to validate because
`.get` function in Python  attempts to find the token type in reserved dict and if it doesn't find
then the token is not a keyword and thus the type is the default given as second argument.
The lexer doesn't know about types so the token definition itself doesn't define its type
so it can be changed.

### PLY Processing

All above was just defining the tokenization rules.
That which patterns are valid tokens and what gets matched to which token.

A token is expressed by having two important parts _type_ and _value_.
The analysed tokens are returned as `LexToken` object instances that has the attributes `type` and `value`.

The processing structure need to call three parts:

```
lexer: ply.lex.Lexer = ply.lex.lex()
lexer.input(data)
for token in lexer:
    # Do something
```

Thus, the final program PLY program for lexical analysis should have a structure

```
reserved: Dict[str, str] = {}
tokens: List[str] = [TOKEN_NAME]

# Token definitions
t_TOKEN_NAME: str = r""
t_ignore: str = ""


def t_newline(t):
    r"\n"
    ...


lexer: ply.lex.Lexer = ply.lex.lex()
lexer.input(data)
for token in lexer:
    ...
```

Enforcing the naming conventions and having minimal parts for other
functionality makes lexical analysis programs mostly same.

