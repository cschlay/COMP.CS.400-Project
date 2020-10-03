# Document for Phase 1

This is the attachment document to be submitted for phase 1 of course project.
The unittest can be run in this directory with

```
python -m unittest
```

## 1. Lexical analysis

Lexical analysis creates tokens from source code.
The program used for analysis doesn't know anything about how the code is used.
It only knows the keywords and token structures and attempts to find them.

When all text in the source can be matched to a token, the other phases can process the tokens.
The tokens in other compilation steps will be further processed them such as
checking that the tokens appear in proper order e.g. not performing addition of integer and string or group the code 
based on parenthesis.

Running lexical analysis before further processing makes it easier to access each
token and not needing to check that they are correct later. It also prevents unnecessary compilation steps
when the most trivial errors in e.g. keyword typos are found in the first step.

## 2. Lexical structure in PLY

### Defining tokens

To use PLY tool we need to define a list or tuple of token names.
They are UPPERCASE strings  that we use to identify the "category" they belong to.
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
    # Or customize the validation
    return t
```

The first line function need to be regular expression, so docstring do not work!


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

# I think it is better to put these as function
# So that functions can be given as arguments to do something with token or 
# return the list for further observations.
def tokenize_data(data: str) ->  List[ply.lex.LexToken]:
    lexer.input(data)
    for token in lexer:
        ...
```

Enforcing the naming conventions and having minimal parts for other
functionality makes lexical analysis programs mostly same.

It should noted that the lexer can be fed data with `input()` after it has been already 
have some data. It seems that after the iteration we cannot iterate it again.
We can get it as list of tokens and process the list later with `list(lexer)`.

## 3. Code Explanation

### a. Keywords

They are done as PLY documentation recommended in section 4.3.

They are defined as dictionary.
Every token that can be lowercase only is defined as function and the
type is changed to keywords type if it is found in the dictionary. 

E.g. `IDENT` can be all lowercase so it is defined as

```
def t_IDENT(t):
    r"[a-z]{1}[0-9A-Za-z_]+"
    t.type = reserved.get(t.value, "IDENT")
    return t
```

If any other token specification may conflict with keywords they will be
need to be defined as function and the type checked as above.

### b. Comments

The comment are defined as ignored token, the ignore prefix is PLY definition
for the token to be ignored so it won't show up in token list.

```
t_ignore_COMMENT: str = r"\.\.\..*\.\.\."
```

In regular expression dot `.` has specified use case so it needs
to be defined to be taken as dot character `\.`.

The dot `.` in the middle is to defined that anything except newlines 
can be in comment. The asterisk `*` after dot `.` (`.*`) means that any number
of characters except newline is valid for regular expression.

So the definition is that between three dots any combination of characters except newline is
matches.

### c. Whitespaces

PLY has a special definition for ignored characters `t_ignore`.
It is a string of characters we want to ignore.

In the assignment we needed whitespace to be excluded
so it is done by adding space ` ` to the string.

In addition to that the `\r` character needed to be ignored so the final definition is:

```
t_ignore: str = " \r"
```

### d. Operators & delimiters

This section explains operators and delimiters as groups because they are defined similarly.

The operators:

```
t_EQ: str = r"="
t_NOTEQ: str = r"!="
t_LT: str = r"<"
t_LTEQ: str = r"<="
t_GT: str = r">"
t_GTEQ: str = r">="
t_PLUS: str = r"\+"
t_MINUS: str = r"-"
t_MULT: str = r"\*"
t_DIV: str = r"/"
```

Almost all operators can be defined to be matched exactly,
there is no need to add quantifier because they don't take from a set of characters.
The exceptions are `\+` and `\*`, which have meaning in regular expressions so they need the backslash.

And delimiters:

```
t_LPAREN: str = r"\("
t_RPAREN: str = r"\)"
t_LSQUARE: str = r"\["
t_RSQUARE: str = r"\]"
t_LCURLY: str = r"\{"
t_RCURLY: str = r"\}"
t_COMMA: str = r","
t_DOTDOT: str = r"\.\."
t_SQUOTE: str = r"\'"
t_COLON: str = r"\:"
t_DOLLAR: str = r"\$"
t_NUMBER_SIGN: str = r"\#"
```

The same exact definitions apply to delimiters.

They do not have meaning at the moment, however when
they are part of some other token the other would the
precedence over these because they have longer definitions.

### e. Decimal literals

The decimal literal is defined as follows:

```
t_DECIMAL_LITERAL: str =  r"(-?0\.[0-9]{1})|(-?[1-9]{1}[0-9]*\.[0-9]{1})"
```

The definition uses two regular expressions separated by `|` and grouped by parentheses the first
defines the range of -0.9 to 0.9. The other numbers are defined in the latter.
This is required because a single definition would allow `000000.0` to be decimals.

The first regex `-?0\.[0-9]{1}` has the following parts:

- `-?`, zero or one minus `-`
- `\.`, the literal dot between the numbers
- `[0-9]{1}`, one of the numbers between 0 and 9 

The second regex `-?[1-9]{1}[0-9]*\.[0-9]{1}`:

- `-?` zero or one minus `-`
- `[1-9]{1}`, one from 1-9 because zero range is handled in the first regex 
- `[0-9]*`, none or more numbers from 0-9 this allows numbers greater than 10
- `\.`, the literal dot between the numbers
- `[0-9]{1}`, one of the numbers 0-9 as the decimal

### f. String literals

Assuming that string literals mean 
`INFO_STRING`, `COORDINATE_IDENT`, `IDENT`,
`RANGE_IDENT` and `SHEET_IDENT`.

```
t_INFO_STRING: str = r"!.*!"
```

In info string `!` are taken as is so any number of characters `.*` except newline is 
allowed to be between the `!` character.

```
def t_COORDINATE_IDENT(t):
    r"[A-Z]{1,2}[0-9]{1,3}"
    return t
```

The coordinate ident had to be defined as function to have precedence (described below).
The regular expression needed to be in the docstring comment's place
and it has the parts of

- `[A-Z]{1,2}`,  which requires it to have one or two chars from A-Z.
- `[0-9]{1,3}`, one, two or three numbers from 0-9

The definition would limit the length of it to 2-5 characters.


```
def t_IDENT(t):
    r"[a-z]{1}[0-9A-Za-z_]+"
    t.type = reserved.get(t.value, "IDENT")
    return t
```

The ident is also defined as function but it need to check for conflicts with keywords (described above)
because it allows all characters to be lowercased.
It has the parts of

- `[a-z]{1}`, one lowercase letter from a-z
- `[0-9A-Za-z_]+`, at least one character from 0-9, A-Z, a-z or `_`.

This make it to have min length of 2 characters.

```
t_RANGE_IDENT: str = r"_[0-9A-Za-z_]+"
```

- `_`, the first character need to be _
- `[0-9A-Za-z_]+`, at least one character from 0-9, A-Z, a-z or `_`.

The range ident would also have min length of 2 chars.

```
t_SHEET_IDENT: str = r"[A-Z]+"
```

This is obvious that at least one character from A-Z.


### g. Function names

```
t_FUNC_IDENT: str = r"[A-Z]{1}[0-9a-z_]+"
```

The function name has the following parts:

- `[A-Z]{1}`, one upper case letter between A-Z alphabets
- `[0-9a-z_]+`, at least one number from 0-9 or letter between a-z or `_`, this disallow one character function names

The above the first require one character and the other at least one so the min length is 2.


## 4. Distinguishing elements

### a. Function & variable names

As defined in the instructions functions starts with uppercase letter
and variable has to be lowercase so defining this into a regular expression distinguishes them.

```
Function: r"[A-Z]{1}[0-9a-z_]+" 
Variable: r"[a-z]{1}[0-9A-Za-z_]+"
```

The relevant parts are `[A-Z]{1}` and `[a-z]{1}`.

### b. Keywords & variable names

Keywords are checked after variable is matched.
If after the pattern matches the value is same as a keyword then the type is changed to keywords.
This is done by checking if it is in `reserved` variable, which is a dict of reserved keywords.

Simply put, we define the all variable tokens that may conflict with keywords, those that can 
be all lower case by using the structure of

```
def t_TOKEN_NAME(t):
    r"" # <- PATTERN HERE
    ... # other operations
    t.type = reserved.get(t.value, "TOKEN_NAME")
    return t
```

With the current information about SheetScript, only `IDENT` may conflict.

### c. Operators > and >=

The operators are defined as exact regex patterns

```
t_GT: str = r">"
t_GTEQ: str = r">="
```

I have preserved the order given in the instructions.
This turns to be possible because PLY sorts the longest regex to be matched first according to documentation section 
4.3., if they are not defined as functions.

The same rule applies to other similar tokens such as `LT` and `LTE`.

### d. String literals and variable names

The string literals has distinguishable definitions compared to variable names.
Variables `IDENT` had to start with lowercase letter.
`INFO_STRING` has exclamation marks `!`, `RANGE_IDENT` has underscore `_` as first character
and `SHEET_IDENT` starts with uppercase letter.

Thus, using regex for the first characters makes them different.

```
IDENT: r"[a-z]{1}[0-9A-Za-z_]+"
INFO_STRING: r"!.*!"
RANGE_IDENT: r"_[0-9A-Za-z_]+"
SHEET_IDENT: r"[A-Z]{1}[0-9a-z_]+"
```

To repeat the parts in the beginning are different: `[a-z]{1}`, `!`, `_`, and `[A-Z]{1}`.
As there are quantifiers (one) first  and exact first characters they should never
allow strings that conflict.

I defined that there must be one of the characters in the begging that are from
different set of characters so this distinguishes them.

As it is mentioned in the instructions that `COORDINATE_IDENT` and `IDENT`
may conflict.
This is resolved by defining the token as function and putting the `COORDINATE_IDENT` above the
`IDENT` definition. This should make it to take over in priority according to 4.3. in the PLY docs.


### e. Comments and other code



### f. Integer literals and decimal literals

As in GT and GTE literals the sorted lengths of regex differentiates the decimal and integers.
The dot `.` and required one digit in regex is what truly distinguishes them.

```
DECIMAL: r"(0\.0)|(-?[0-9^0]+\.[0-9]{1})"
INT: r"0|-?[0-9^0]+"
```
The or condition for zero values and exclusion of 0 is required because 
otherwise it accepts `000000.0` and `00000` for decimals and integers.

## 5. Extras

Not yet.

## 6. Thoughts

I think this phase was quite mechanical and the code should be 
mostly similar to PLY documentation.
There wasn't much room for creativity.

After some tests and writing README, I think I naively trusted the documentation's example on how
to define tokens and just hardcoded the token names.
A small change that would be make testing and referring to tokens is
always define token as "constant" so that it can be referred with `sslexer.TOKEN_IDENT`.

```
# sslexer.py

TOKEN_IDENT: Final[str] = "IDENT"
tokens: List[str] = [TOKEN_IDENT]
```

The implementation might need changes for other phases.
