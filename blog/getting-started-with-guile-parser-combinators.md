# 2016/01/01 - Getting started with Guile Parser Combinators

Guile Parser Combinators implement (monadic) parser combinators. What
it means in pratice is that you create procedures that parse most of
the time strings and output a structured data, most likely s-expr. They
are said to be *combinators* because you can compose parser
procedures. The monadic part is an implementation detail mostly.

Say you want to parse some input text something like markdown and turn
it into sxml.

Be aware that guile-parser-combinators (unlike guile-log) doesn't have
an error handling machinery but since you compose small parser to make
a bigger parser it's easy to debug the small units and have a working
parser.

This blog use a [markdown parser](/markdown.scm) implemented using
guile-parser-combinator; it ain't perfect, they are bugs with
workarounds.

The first part of this article introduce guile-parser-combinators
concepts and then apply them to build a csv parser.

### Getting started

Download guile-parser-combinator:

```
$ git clone git://dthompson.us/guile-parser-combinators
```

Fire an REPL inside the created directory:

```
$ cd guile-parser-combinators
guile-parser-combinators $ guile -L `pwd`
scheme@(guile-user)> (use-modules (parser-combinators))
```

We will heavily rely on streams aka.
[srfi 41](https://www.gnu.org/software/guile/manual/html_node/SRFI_002d41-Stream-Library.html),
don't forget to import it:

```
scheme@(guile-user)> (use-modules (srfi srfi-41))
```

You are ready!

### Three kinds of parsers

All parsers can return two kind of values of `<parse-result>` a
`parse-success` or a `parse-failure`. `parse-success` have a `value`
which is the output of the parser and a `stream` which is what remains
to be parsed. `parse-failure` results have no value and no stream.

There is three kind of parsers in guile-parser-combinators. In the
following I described them in the case where the input is strings and
the final output is an s-expr:

- plain parser: `string -> string`. This allows to recognize and split
  input string into small units. This is the most basic parser. Example
  plain parser is `(parse-char #\c)` which will succeed if the input
  stream starts with a `c` char, otherwise it fails. It will return
  `c` as value and return the input stream queue.

- combinator parser: `parser -> parser`. Those takes as input a parser
  and output another parser. This might seem strange. I think it's better
  to call them *control* parsers but the literature says otheriwse.
  Example combinator parser is `(parse-any (parse-char #\a) (parse-char #\b) (parse-char #\c))`
  which will succeed if any of its input parser succeed. Which means in this
  case that the input stream must start with `a` or `b` or `c` char.

- output builder: `s-expr -> s-expr`. Those are not really parser as they never
  consume the input stream but instead shake around `<parse-result>` value.

All those parsers are further explained in what follows.

#### Plain parsers

I lied a little previously, I said that plain parser take as input
string and output string. Actually it's just a (second hand) view to
understand how parser works.  The actual implementation takes as input
a stream and outputs a `parse-result`.

For instance the following is a valid parser, that will return a
`parse-result` that succeed when the first char in the stream is
a `c`:

```
(define (parse-c-char stream)
    (if (eqv? (stream-car stream) #\c)
        (parse-result #\c (stream-cdr stream))))
```

You can test it with the following:

```
scheme@(guile-user)> (list->stream '(#\c #\c #\c))
$3 = #<stream ...>
scheme@(guile-user)> (parse-c-char $3)
$4 = #<<parse-result> value: #\c stream: #<stream ...>>
```

The only problem of this parser is that it doesn't handle the case
where the input stream is empty. Nonetheless start to get the idea.

To parse a `c` char using guile-parser-combinator, you have to use
the `(parse-char char)` procedure which returns a parser that succeed
if the first item of the input stream is a `c` and fails otherwise:

```
scheme@(guile-user)> ((parse-char #\c) (list->stream '(#\c #\c #\c)))
$8 = #<<parse-result> value: #\c stream: #<stream ...>>
scheme@(guile-user)> ((parse-char #\c) (list->stream '(#\a #\b #\c)))
$9 = #<<parse-result> value: #f stream: #f>
```

As you can see in result `$8`, `parse-result`'s value is the `c` char.
You can't check easily that `(parse-char #\c)` consumed the input stream,
you'll have to believe me for now.

Here's the implementation of `parse-char`, as you can see, it return a
`stream -> parse-result` procedure:

```
(define (parse-char char)
  "Create a parser that succeeds when the next character in the stream
   is CHAR."
  (lambda (stream)
    (stream-match stream
      (() %parse-failure)
      ((head . tail)
       (if (equal? head c)
           (parse-result head tail)
           %parse-failure)))))
```


There is various procedure that return plain parsers:

- `(parse-char char)`

- `(parse-char-set char-set)` which parse a char from the provided charset.

- `(parse-string string)` which parse iteratively the list of chars
  that makes up `string` from the input stream.

Let's try the last procedure:

```
scheme@(guile-user)> (define string->stream (compose list->stream string->list))
scheme@(guile-user)> ((parse-string "ccc") (string->stream "ccc means chaos computer club"))
$12 = #<<parse-result> value: "ccc" stream: #<stream ...>>
```

There is also `parse-any-char` which is not a procedure that returns a
parser, but a plain parser. It will consume any char found in the
input stream:

```
scheme@(guile-user)> (parse-any-char (string->stream "scheme is awesome"))
$13 = #<<parse-result> value: #\s stream: #<stream ...>>
scheme@(guile-user)> (parse-any-char (string->stream "\nthis starts with a newline"))
$15 = #<<parse-result> value: #\newline stream: #<stream ...>>
```

At this point, if things are still fuzzy, it's ok because you still
don't know how given only `(parse-string string)`, `(parse-char char)`
and `parse-any-char` plain parsers how you can parse something. Things
will get more interesting once you know about *control parser*!

#### Combinator parsers

Combinator (control?) parsers are procedures similar in principle to
`compose` except they take as input other parser and are tailored to
compose them using semantic useful in the context of parsing.

Here is the full list of control parsers:

- `(parse-any parser ...)` try to parse input stream with each parser
  given as argument and succeed as soon as one of the parser succeed.
  Fails if no parser succeed. (It also called `parse-or`)

- `(parse-each parser ...)` parse input with the parser provided as
  argument feeding each parser with the stream that previous parser
  returned. Succeed only if all parser succeed. This allows to parse a
  sequence of items from the stream otherwise to walk forward in the
  stream.

- `(parse-zero-or-more parser)` and `(parse-one-or-more parser)` will
  apply the parser passed argument zero or one or more times to the
  input stream feeding the result stream of the first iteration to the
  same parser until `parser` can't parse anything from the input
  stream. `parse-zero-or-more` succeed all the time but will return
  the same stream as the input stream if it can't parse even once the
  intput stream. `parse-one-or-more` must at least succeed once to
  parse the input stream. This also allows to walk forward the stream.

Let's try `parse-each`:

```
scheme@(guile-user)> ((parse-each parse-any-char parse-any-char parse-any-char) (string->stream "gnu"))
$17 = #<<parse-result> value: (#\g #\n #\u) stream: #<stream ...>>
scheme@(guile-user)> (define parse-gnu (parse-each (parse-char #\g) (parse-char #\n) (parse-char #\u)))
scheme@(guile-user)> (parse-gnu (string->stream "gnu"))
$18 = #<<parse-result> value: (#\g #\n #\u) stream: #<stream ...>>
scheme@(guile-user)> (parse-gnu (string->stream "ccc"))
$19 = #<<parse-result> value: #f stream: #f>
```

Let's try `parse-any`:

```
scheme@(guile-user)> (define parse-a-or-b (parse-any (parse-char #\a) (parse-char #\b)))
scheme@(guile-user)> (parse-a-or-b (string->stream "a"))
$20 = #<<parse-result> value: #\a stream: #<stream ...>>
scheme@(guile-user)> (parse-a-or-b (string->stream "b"))
$21 = #<<parse-result> value: #\b stream: #<stream ...>>
scheme@(guile-user)> (parse-a-or-b (string->stream "c"))
$22 = #<<parse-result> value: #f stream: #f>
```

I guess now you get the point.

#### Output builder

Output builder parsers are special parser that takes a parser as
argument and process its output before returning. You can use
`(parse-map proc parser)` or `(parse-match parser matcher ...)` to do so.

For instance, here is an example use of `parse-map`:

```
scheme@(guile-user)> (define parse-gnu* (parse-map (lambda (lst) `(b ,(list->string lst))) parse-gnu))
scheme@(guile-user)> (parse-gnu* (string->stream "gnu is awesome"))
$25 = #<<parse-result> value: (b "gnu")) stream: #<stream ...>>
```

As you can see `parse-gnu*` returns `(b "gnu")`.


### wrapping with a csv parser

csv is a notoriously difficult text file format to parse because it
comes in much different flavor. In what follows we will describe a
parser for somekind of csv format that is straightforward.

For our csv parser we want the following two unit tests to pass:

```
(define-syntax test-check
  (syntax-rules ()
    ((_ title tested-expression expected-result)
     (begin
       (format #t "* Checking ~s\n" title)
       (let* ((expected expected-result)
              (produced tested-expression))
         (if (not (equal? expected produced))
             (begin (format #t "Expected: ~s\n" expected)
                    (format #t "Computed: ~s\n" produced))))))))


(when (or (getenv "CHECK") (getenv "CHECK_MARKDOWN"))
  (test-check "single line"
              (csv "a;b;c;")
              (list (list "a" "b" "c")))

  (test-check "multi line"
              (csv "a;b;c;
d;e;f;")
              (list (list "a" "b" "c") (list "d" "e" "f"))))
```

Otherwise said, a csv will be a multiline string with columns
separated by semi-colon chars.

#### `parse-unless`

To be able to parse such a format, we need to introduce another parser
combinator called `(parse-unless predicate parser)`. What it does is
that it only execute `parser` if `predicate` parser fails. This is
useful because a lot of time they are control characters in the input
stream that identifies the start or end of a given text unit. In the
case of the csv parser there is two control chars: the semi-colon and
newlines.

The implementation of `parse-unless` is simple! Here is it:

```
(define (parse-unless predicate parser)
  (lambda (stream)
    (match (predicate stream)
      ((? parse-failure?) (parser stream))
      (_ %parse-failure))))
```

Basically what it does, is that it checks that `predicate` parser
fails on input stream and in that case execute `parser`.

(Otherwise the big picture is that the caller, rewinds the stream
until it can find a branch using `parse-any` that
succeeds... otherwise said, parser combinators try every parser until
it find a parser that succeed or it fails).

Anyway, this allows to check for the presence of control chars before
parsing something. There is an similar `(parse-when predicate parser)`
and you might think that it's equally useful but in practice when
parsing `parse-unless` is much more useful. It has to do with the fact,
that negation allows to capture much more logic that plain equality.
Negation is very powerful.

#### Parsing a column

In csv a column looks like `abc;` where the semi-colon `;` marks the
end of the column. So a column is made of its value in this case `abc`
and its end marker the semi-colon. A such, a column value can be
anything but a semi-colon. This is a first parser:

```
scheme@(guile-user)> (define parse-column-value-char (parse-unless (parse-char #\;) parse-any-char))
scheme@(guile-user)> (parse-column-value-char (string->stream "abc;"))
$1 = #<<parse-result> value: #\a stream: #<stream ...>>
scheme@(guile-user)> (parse-column-value-char (string->stream ";abc"))
$2 = #<<parse-result> value: #f stream: #f>
```

But this parser only parse a single char, let's repeat the same parser
several times, one or more times using `parse-one-or-more` (we
consider that everycolumn has at least one char value).

```
scheme@(guile-user)> ((parse-one-or-more parse-column-value-char) (string->stream "abc;"))
$3 = #<<parse-result> value: (#\a #\b #\c) stream: #<stream #\; ...>>
```

And there we have parsed the first column value "abc" but it's not
properly packed as a string, to fix that we can use `(parse-map proc
parser)` which will lift the `parse-result`'s value with `list->string`:

```
scheme@(guile-user)> ((parse-map list->string (parse-one-or-more parse-column-value-char)) (string->stream "abc;"))
$4 = #<<parse-result> value: "abc" stream: #<stream #\; ...>>
```

We can make of this the first parser unit of our csv parser, as it
really parse a single column value and properly packs it:

```
scheme@(guile-user)> (define parse-column-value (parse-map list->string (parse-one-or-more parse-column-value-char)))
scheme@(guile-user)> (parse-column-value (string->stream "abc;"))
$5 = #<<parse-result> value: "abc" stream: #<stream #\; ...>>
```

As you can see, there's still elements in the stream. The semi-colon
control character is not parsed yet, but it's really part of the
column.  So what will do next is parse that control char and remove it
from `parse-result` using `parse-map`. Try to guess how before reading
what's follows.

So we need to chain our `parse-column-value` with a
`parse-column-control-char`.  But before that
`parse-column-control-char` is a simple `(parse-char #\;)`, we define
it to make the parser more readable and redefine `parse-column-value`
it terms of it because that's actually the real semantic of parsing a
column value:

```
scheme@(guile-user)> (define parse-column-control-char (parse-char #\;))
scheme@(guile-user)> (define parse-column-value-char (parse-unless parse-column-control-char parse-any-char))
scheme@(guile-user)> (define parse-column-value (parse-map list->string (parse-one-or-more parse-column-value-char)))
```

Check that `parse-column-value` still works as expected.

Like I said earlier we need to chain `parse-column-value` with
`parse-column-control-char` to build `parse-column`. For that we can
use `(parse-each parser ...)`:

```
scheme@(guile-user)> ((parse-each parse-column-value parse-column-control-char) (string->stream "abc;def;"))
$7 = #<<parse-result> value: ("abc" #\;) stream: #<stream ...>>
```

As you can see, now we have a list with two values in
`parse-result`. We don't care about the semi-colon in the output. It's
only present in the input to mark the end of column. So we `parse-map` away:

```
scheme@(guile-user)> ((parse-map car (parse-each parse-column-value parse-column-control-char)) (string->stream "abc;def;"))
$9 = #<<parse-result> value: "abc" stream: #<stream ...>>
```

That's is it, we have the definition of `parse-column`:

```
scheme@(guile-user)> (define parse-column (parse-map car (parse-each parse-column-value parse-column-control-char)))
scheme@(guile-user)> (parse-column (string->stream "abc;def;gnu;"))
$10 = #<<parse-result> value: "abc" stream: #<stream ...>>
```

As you might have guess we can repeat one or more time `parse-column`
to parse a single row:

```
scheme@(guile-user)> ((parse-one-or-more parse-column) (string->stream "abc;def;gnu;"))
$12 = #<<parse-result> value: ("abc" "def" "gnu") stream: #<stream>>
```

Neat isn't it?

But this doesn't really every kind of row. Because there is two kind of rows:

- The last row that ends with an `eof`
- The other rows that ends with a newline

Let's define a `parse-eol`:

```
scheme@(guile-user)> (define parse-eol (parse-any parse-end (parse-char #\newline)))
```

Now we can (almost) define `parse-row`:

```
scheme@(guile-user)> (define parse-row (parse-each (parse-one-or-more parse-column) parse-eol))
scheme@(guile-user)> (parse-row (string->stream "abc;def;gnu;"))
$15 = #<<parse-result> value: (("abc" "def" "gnu") #t) stream: #<stream>>
```

As you can see, there is some #t garbage in the `parse-result`'s
value. let's get rid of it using `parse-map`:

```
scheme@(guile-user)> (define parse-row (parse-map car (parse-each (parse-one-or-more parse-column) parse-eol)))
scheme@(guile-user)> (parse-row (string->stream "abc;def;gnu;"))
$16 = #<<parse-result> value: ("abc" "def" "gnu") stream: #<stream>>
```

Wee!!! We have complete row! Guess what parser combinator you have to
use to parse several rows...

Time is up:

```
scheme@(guile-user)> (define parse-csv (parse-one-or-more parse-row))
```

Let's define a small csv document and try to parse it:

```
scheme@(guile-user)> (define document "abc;def;gnu;\n123;456;789;")
scheme@(guile-user)> (parse-csv (string->stream document))
$21 = #<<parse-result> value: (("abc" "def" "gnu" "\n123" "456" "789")) stream: #<stream>>
```

Ooops! There is a single list in the output; there's a bug in a
parser! There is no such thing as `\n123` column. So there must be a
bug in the `parse-column` parser... The solution is... to not parse
columns starting with a newline! So let's use `parse-unless` again:

```
scheme@(guile-user)> (define parse-column (parse-unless (parse-char #\newline) (parse-map car (parse-each parse-column-value parse-column-control-char))))
```

Our final csv parser looks like the following:

```
(define parse-column-control-char (parse-char #\;))
(define parse-column-value-char (parse-unless parse-column-control-char parse-any-char))
(define parse-column-value (parse-map list->string (parse-one-or-more parse-column-value-char)))
(define parse-column (parse-unless (parse-char #\newline) (parse-map car (parse-each parse-column-value parse-column-control-char))))
(define parse-row (parse-map car (parse-each (parse-one-or-more parse-column) parse-eol)))
(define parse-csv (parse-one-or-more parse-row))
```

There is a handy `parse` procedure in guile-parser-combinators that
allows to define the following procedure:

```
scheme@(guile-user)> (define (csv string) (parse parse-csv string))
scheme@(guile-user)> (csv document)
$14 = (("abc" "def" "gnu") ("123" "456" "789"))
```

That's all folks!
