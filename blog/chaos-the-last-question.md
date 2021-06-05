# 2021/06/05 - Chaos: The Last Question

I am investigating this pattern combinator thing, because pattern are
everywhere in programming e.g Chomsky's grammars, and also Machine
Learning. The thing I am trying to build is different from Machine
Learning pattern recognition. Pattern combinators are neither
supervised nor unsupervised, they do not learn, they are teached with a
specification constructored with combinators how to recognize
patterns.

Pattern matching facility ease the work of constructing an interpreter
or compiler. They are the basis of Scheme syntax-rule, syntax-case,
nanopass framework, Kernel, and GNU Guile compiler tower
[GNU-GUILE]. Part of Guile compiler tower, there is `foldt*` by Andy
Wingo. `foldt*` builds upon Kiselyov's `foldt`. Both `foldt` and
`foldt*` allow to recognize patterns in s-expr, they also allow to
construct a new object (just like regular `fold`). Pattern combinators
are concerned about traversing the source; the patterns in that source
are recognized with user prodiced procedures (fhere, fdown, fup);
pattern combinators always contruct an object following the same
template, that is a flat environment, such as a mapping or association
list.

In the previous note, I have glossed over `sum` that re-surface the
implementation of a procedure. `dubito` some kind of inference
engine. `cogito` was barely mentioned, but I meant it as an
`eval`.

In this note, I will try to explain how `(sum cogito)` works.

Here is the *Shutt's Equation of Software*:

```scheme
(define eval
  (lambda (exp env)
    (cond ((kernel-pair? exp)  (combine (eval (kernel-car exp) env)
                                        (kernel-cdr exp)
                                        env))
          ((symbol? exp)  (lookup exp env context))
          (else exp))))
```

This is a slightly modified version of `SINK`'s `eval`, I dropped the
`context` that is the reification of a continuation, that in `(call/cc
proc)` is passed to `PROC`. Unlike in Scheme, a context is
encapsulated ie. it is its own type (see Racket and Gambit).

## Tentative emulation of Kernel with Scheme

About Scheme, I will try to describe the semantic of Kernel using
Scheme without actually building an interpreter in Scheme (that is
what SINK does). Instead, I will describe a subset of Kernel in
particular, the `$vau` operative, that allows to create new
operative with Scheme pseudo-code:

```scheme
(define-syntax $vau
  (lambda (stx)
    (syntax-case stx ()
      (($vau args env body ...)
       #'(lambda (args env) body ...)))))
```

That is wild guess ie. prelimeray translation. To call a procedure
constructed with `$vau` you need another syntax transformer and a few
helpers:

```scheme
(define-syntax apply-vau
  (lambda (stx)
    (syntax-case stx ()
      ((apply-vau operative args ...)
       #'(let ((dynamic-environment (environment-current)))
           (operative 'args dynamic-environment))))))
```

(Now that I think about it, it can be implemented in terms of
`syntax-rule`)

Mind the quoted `args`, `args` is constructed in the template as a
quoted expression, and its evaluation might be done in `body ...` with
the help of Scheme's `(eval exp environment)`.

`environment-current` is like Guile's `the-environment`.

## Another emulation of Kernel with Scheme

Another approach is to use only procedures and no macros. For instance:

```scheme
(define (my-operative args env)
  body ...)
```

Since there is two kinds of callables in `Kernel`: operative and
applicative.  One will need to prefix every Scheme call with a
`kernel-call`:

```scheme
(define (kernel-call combiner env args)
  (if (applicative? combiner)
      ((unwrap combiner) (map (lambda (arg) (eval arg env))))
      ;; otherwise, it is an operative
      (combiner args env)))
```

Where `applicative?` is the predicate associated with:

```scheme
(define-record-type <applicative>
  (wrap operative)
  applicative?
  (operative unwrap))
```

Then what you write in Kernel as:

```scheme
(my-combiner a b c)
```

Would be transpiled as:

```scheme
(kernel-call my-combiner (environment-current) (list 'a 'b 'c))
```

`(environment-current)` current can be constructed at compile time,
since it is the static / lexical scope (I hope).

The only missing piece I can forsee is that Kernel support trees as
operands, but that requires more work, including a pattern matcher!

## `sum`, or no `sum`

Previously, I wrote the goal of `sum` is ultimately to call `(sum
eval)` and return an object language representation of `eval` in the
meta-language. In other words, it would return the full source of the
compiler, one language-level below the object language.

I will investigate `(sum +)`: what is the meta-language definition of
the applicative `+` in Scheme:

```scheme
(define (sum +)
  (applicative (operative (lambda (args env) (+ (env-ref env 'a) (env-ref env 'b))))))
```

It does not make sense to compile a mere `lambda`, you need a full
lambda such as:

```scheme
(lambda (args env) (+ (env-ref env 'a) (env-ref env 'b)))
```

It would be transpiled to the following web assembly:

```scheme
(func $a.683 (param $cl.397 externref) (result i32) (result externref)
      (local $a externref)
      (local $b externref)
      (local $out externref)
      (local.set $k (table.get $stack (i32.const 0)))
      (local.set $a (table.get $stack (i32.const 1)))
      (local.set $b (table.get $stack (i32.const 2)))
      (local.set $out (call $+ (local.get $a) (local.get $a)))
      (table.set $stack (i32.const 0) (local.get $out))
      (i32.const 1) ;; continue = yes
      (local.get $k)) ;; continuation closure
```

The previous text would be the representation of `(sum (sum +))` in
the object language. More or less.

## References

- [GNU-GUILE] https://www.gnu.org/software/guile/docs/docs-2.2/guile-ref/Compiler-Tower.html
