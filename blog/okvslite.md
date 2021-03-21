# 2021/02/13 - okvslite

I do not want to spread Fear, Uncertainty and Doubt (FUD) about
[SRFI-167
(okvs)](https://github.com/scheme-requests-for-implementation/srfi-167/)
and [SRFI-168 (nstore)](https://github.com/scheme-requests-for-
implementation/srfi-168). Those libraries are useful and can be used
as demonstrated in guile-babelia, and guile-nomunofu. They can also be
improved. In this article, I try to tackle problems specific to
SRFI-167 aka. okvs.

## Engines

The engine procedures were supposed to abstract the underlying
implementation to be able to swap implementation hence storage
database backend at will in user code.

A better abstraction is [generic functions as seen in
chibi](http://synthcode.com/scheme/chibi/lib/chibi/generic.html.). The
document is little light, but the tests explain very well how it
works:

```scheme
(define-generic add)

(define-method (add (x number?) (y number?)) (+ x y))

(define-method (add (x string?) (y string?)) (string-append x y))

(test 4 (add2 2))

(test "22" (add "2" "2"))
```

Another way I would call it, probably is: "predicate-based
multi-methods" or "predicate-based multiple dispatch". See the
following article:

[Multiple dispatch Multiple dispatch or multimethods is a feature of some
programming languages in which a function or method can be dynamically
dispatched based on the run-time (dynamic) type or, in the more general case,
some other attribute of more than one of its arguments.](https://en.wikipedia.org/wiki/Multiple_dispatch#Java)

In Python, it looks much like an abstract abc class with the added
support of multiple dispatch that is more powerful that single
dispatch. See python documentation:

- [abc - Abstract Base Classes - Python 3.9.1 documentation This module
provides the infrastructure for defining abstract base classes (ABCs) in
Python, as outlined in PEP 3119 ; see the PEP for why this was added to
Python. (See alsoPEP 3141 and the module regarding a type hierarchy for
numbers based on ABCs.)](https://docs.python.org/3/library/abc.html)

- [functools - Higher-order functions and operations on callable objects -
Python 3.9.1 documentation Source code: Lib/functools.py The module is for
higher-order functions: functions that act on or return other functions. In
general, any callable object can be treated as a function for the purposes of
this module. The module defines the following functions: Simple lightweight
unbounded function cache. Sometimes called "memoize".](https://docs.python.org/3/library/functools.html#functools.singledispatch)

Also, the dispatch is done with any predicate that is slightly more
powerful than Python's isinstance.

So, in okvslite, all engine-fooobar procedure will be generic methods.

## pack and unpack

The signature of pack has a problem: (pack . key) -> bytevector?. That
is symmetric with (unpack bytevector) -> list?. We can simulate their
use with the following code:

```scheme
(assume? (equal? (unpack (apply pack key)) key))
```

That is ok in most case, except the fact that key rest argument will
force the creation of a new list in some (most?) scheme
implementation, hence stress the garbage collector in the hot
path. This is might not be a problem, if they were no easy faster
alternatives. In that case, there is a performance trick that is also
an enabler. We can change the signature of pack to:

```
(pack obj) -> bytevector
```

Similarly unpack becomes:

```
(unpack bytevector) -> obj
```

Hence the above simulation becomes:

```
(assume? (equal? (unpack (pack key)) key))
```

See that apply disappeared. That is not only slightly faster and
memory efficient, and it will add the ability to pass any basic scheme
object to pack as top level value. Possibly a vector? instead of a
list, and also an atomic value like some number, a boolean.

That will also enable another small optimization, again in the hot
path, while reducing the complexity of the code in many cases. For
instance, in the case where the value part is an atomic value,
previously it was required to pass a list as value, otherwise said,
the value was necessarily wrapped inside a list:

```scheme
;; To store 42 as a value before you were required to do the following.
;; Mind the fact that the rest argument,
;; makes it implicit that the value is a list!

(okvs-set! #vu8(C0 FF EE BA D0) (pack 42))

;; Then when you query that key:

(define fortytwo (car (okvs-ref #vu8(C0 FF EE BA D0)))
```

The new code is more readable:

```scheme
;; There is no implicit list!
(okvs-set! #vu8(C0 FF EE BA D0)
(pack 42))
;; Then when you query that key:
(define fortytwo (okvs-ref #vu8(C0 FF EE BA D0))
```

Hence there is less car in the hot path!

## okvs-in-transaction

In the SRFI document, I did not explain what is a transaction:

A database transaction wrap operations that will all be applied, otherwise in
case of error, none will be applied.

The full signature is:

```
(okvs-in-transaction okvs proc [failure [success [make-state [config]]]])
```

failure and success are similar those used in hash-table-ref. A
similar pattern with Python is try / except / else :

```python
try:
    out = proc()
except Exception:
    return failure()
else:
    return success(out)
```

The advantage of the Scheme approach is that it makes a stack
shuffling aka.  exception or non-local exit, optional, hence it makes
some optimizations possible (compared to Pythonic code that rely on
exceptions in similar cases).  Most of the time with Scheme exceptions
are opt-in. Also the code is much shorter, and suggest to create a
procedure with failure and success which leads to more readable code.

More on okvs-in-transaction: I think I will drop all-around config
from all procedures because this is really here to enable some
optimizations with wiredtiger, but wiredtiger... make-state is useful
but rather obscure, I need to document more cases that makes use of it
(mind the fact that is the last optional argument when config will be
gone).

## `okvslite-query`

A big change that is coming is to merge okvs-ref and okvs-range to
make it explicit that the API is the query Domain Specific
Language. So, okvslite- query looks like:

```scheme
(okvslite-query okvslite key [comparator1 comparator2 other [offset [limit]]])
```

A common realization is to query `[a..b[`:

```scheme
(okvslite-query okvslite a '<= '< b)
```

To retrieve a reversed generator, that is from b to a where b is excluded:

```scheme
(okvslite-query okvslite b '< '<= a)
```

Then okvs-remove will have a similar signature.

okvs-range-prefix will be renamed okvs-query-prefix as sugar one-liner
helper to avoid to dive into strinc... okvs-query-prefix can be easily
expressed with okvs-query when strinc is public and understood:

```
(define (okvs-query-prefix okvslite key-prefix)
  (okvslite-query okvslite key-prefix '<= '< (strinc key-prefix)))
```

## Hooks

I think okvs-hook-on-transaction-begin must be called again in the
case where okvs-in-transaction rollback to replay the transaction.

Prolly, similarly to make-state, hooks are too advanced, and I do not
use them anymore...
