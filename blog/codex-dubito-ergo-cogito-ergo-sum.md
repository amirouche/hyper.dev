# 2021/06/04 - Codex: Dubito, ergo Cogito, ergo Sum

Last couple of weeks I learned about:

- 3-LISP: a theorical evolution of LISP where everything can be
  inspected;

- Kernel: an evolution of Scheme that forgo syntax transformers as
  described in Scheme;

- Control Flow Analysis / Just-In-Time and Ahead-Of-Time compilation /
  optimizations: what I call "dubito". It is known as partial /
  symbolic / algebraic evaluation, and includes type inference.

My goal is to devise and build an optimizing compiler which does not
precludes AOT or JIT. In other words: I want both AOT and JIT. As a
subgoal, I want to build an optimizing or optimized pattern matching
program in the spirit of SRFI-200, and SRFI-204, that I call pattern
combinators. One particular optimization, I think about is what
Software Design for Flexibility [SDF] calls unification.

For instance given the following `match` expression:

```scheme
(match exp
  ((a) out1)
  ((a d) out2))
```

Can be rewritten as follow:

```scheme
(match exp
  ((a . rest) (match rest
                (() out1)
                ((d) out2))))
```

In that case, doing some kind of prefix compression.

`match` can be seen as a pattern combinator, that is a parser
combinator that can traverse not only a sequence, but also a sequence
made of nested sequence in a recursive way. For the purpose of the
pattern combinator, a sequence is a finite acyclic ordered set. A
sequence might be a list, vector or an ordered mapping. A parser
combinator such as the one described in [GLL] is a good basis for a
pattern combinator, except if does not support the optimizing /
optimized part.

To be able to implement optimizing pattern combiner, it would require
to reflect upon the match predicates, in particular have access to a
predicate `subsume?` that allows implement a partial order over
predicates. And that should be done at in the object language.

The object language is the language of the user. It is defined in
opposition to meta language that is used to implement the object
language. The meta language might be itself implemented in terms of
another meta language until... until all the way down! That is where
3-LISP call into atoms, the physical atoms (not the atoms of the
simulation).

We will just glimpse over the problem(s), and add a reflection
applicative called `sum`, so that we can introspect how applicative
and operative are made, so that in turn we may be able to optimize
code at runtime from the object language.

Instead of trying to implement `subsume?` and the optimizing pattern
compiler, I will implement only arithmetic folding (replace an
arithmetic computation with its value) with an applicative based on
the inferences / knowledge / theories built by an applicative called
`dubito`.

So, given the following pseudo-code:

```scheme
(define (make-frob-adder value)
  (lambda (other)
    (+ other value 36)))

(define my-frob-adder-2 (make-frob-adder 2))

(my-frob-adder-2 4) ;; => 42
```

A simple compiler will just compile `my-frob-adder-2` into a `lambda`
that is passed an extra environment argument called `static` so that
the resulting procedure does not have free-variables, it will look
like:

```scheme
(define (my-frob-adder-2-compiled static other)
  (define value (environment-ref static 'value))
  (+ other value 36)
```

The trick is that if we forgo the last line of the previous program,
the closure of `my-frob-adder-2` is known at compile time. If we also
consider the last line, the whole program can be compiled to `42`:
That is what is called (AFAIK) constant folding.

Let's consider the following program:

```scheme
(define (make-frob-adder value)
  (lambda (other)
    (+ other value 36)))

(define my-frob-adder-2 (make-frob-adder 2))

(my-frob-adder-2 (string->number (cadr (command-line))))
```

It is similar to the original program, except it `my-frob-adder-2`
takes its argument from command-line, hence it can not be folded into
an integer object, because... `(command-line)` is not known at compile
time. So, indeed after a simple compilation, we end up with the
following code:

```scheme
(define (my-frob-adder-2 static other)
  (define value (environment-ref static 'value))
  (+ other value 36))

(my-frob-adder-2 (alist->environment `((value . ,2))) (string->number (cadr (command-line))))
```

That is naive example: an optimizing compiler can create the following
optimized definition for `my-frob-adder-2`:

```scheme
(define (my-frob-adder-2 other)
  (+ other 40)) ;; 36 + 4 = 40
```

So what is this all about?!1!

It is also seems a little naive given that Chez Scheme can compile to
native code an s-expr at runtime, given a perfomance timer (cost
center), and counters, that gather new knowledge only known at
runtime, it is completly possible to implement a manual JIT
[MANUAL-JIT].

So what do `sum` do that is new? Not much: it puts all that together.

Kernel will factorize macro and procedure into operatives, it will
also reify all environments: static / lexical, and dynamic. The
application `sum` will reify in the object language the implementation
of any object... including `eval` in other words, `eval` can be
reifyed as a meta-evaluator or better as the "source code" in the
previous meta language. `sum` does not only mean that the source is
embedded in the program, but also prescribe that it is possible to
represent in a possibly infinitly resursive way all the
meta-languages. The limit being our knowledge, time, and energy to
encode that as source. Does it mean that this language is
self-bootstrappable, in other words that it does not require a seed:
no. Even it it self-hosted and self-describing, it requires a seed
[BOOTSTRAPPABLE].

In the above paragraph I glossed over `(sum eval)`: i) does it return
a meta-evaluator, a program represented in the object language that
can evaluate the object language (itself), ii) does it return an
evaluator in the previous meta-language. Both are possible, the
latter is more interesting, because it expose the compiler tower
[NANOPASS] to the object language.

`eval` is not the only interesting primitive procedure. In the context
of Scheme, it is interesting to reflect upon a couple of
procedures. One of the most interesting is `call/cc`, another
interesting procedure is the non-standard `expand` and yet another is
everything related to the garbage collector. To stay goal-driven, a
target application of that reflection, that I think may be
interesting, can be to disable or customize the garbage collector for
a subset of the program. Another goal might to change for a subset of
the program the evaluation strategy without relying on meta-evaluation
[EVALS].

In the case where `(sum eval)` returns the source of `eval` in the
previous meta-language, `expand`, `call/cc`, and the garbage collector
should be represented... somehow!

## References

- [SDF] https://mitpress.mit.edu/books/software-design-flexibility

- [GLL] https://epsil.github.io/gll/

- [MANUAL-JIT] https://m00natic.github.io/lisp/manual-jit.html

- [BOOTSTRAPPABLE] http://bootstrappable.org/

- [NANOPASS] https://nanopass.org/

- [EVALS] https://en.wikipedia.org/wiki/Evaluation_strategy
