# 2018/01/01 - Getting Started With Guile Dynamic Foreign Function Interface

I created a dynamic-link star procedure to help during the creation of
dynamic ffi bindings (which is the prefered way to go now on).

It's helpful for several reasons:

- no need to explicitly call dynamic-func and pointer->procedure, so
  it's two less procedures to know about.

- It mimicks the C signature, so it's easier to read.

This documentation is meant to be self sufficient which means that you
should be able to fully bind your favorite function based C library
just by reading this.

The code of the procedure is at the bottom.

```
((dynamic-link* [library-name]) return-type function-name . arguments)
```

Return a lambda that returns a scheme procedure linked against
FUNCTION-NAME found in LIBRARY-NAME. If LIBRARY-NAME is not provided
this links against the C standard library.

The returned procedure takes the signature of the function that you
want to link against.

Also RETURN-TYPE and ARGUMENTS must be foreign types. They can be
found in (system foreign): int8, uint8, uint16, int16, uint32, int32,
uint64, int64, float, double.

In addition, platform-dependent types variables exists: int,
unsigned-int, long, unsigned-long, size_t, ssize_t, ptrdiff_t.

There is also a void variable that must be used to wrap function that
returns nothing.

Last but not least, the star symbol is used by convention to denote
pointer types.

More [documentation about foreign types](https://www.gnu.org/software/guile/manual/html_node/Foreign-Types.html#Foreign-Types).

### Example

Here is a REPL run, showing how it works:

```
(define stdlib (dynamic-link*))  ;; link against stdlib
(define strlen (stdlib int "strlen" '*))  ;; retrieve a procedure associated to "strlen"
(strlen (string->pointer "abc"))
```

Since you probably don't want to expose the pointer api to the dev. You might define the following strlen procedure:

```
(define stdlib (dynamic-link*))  ;; link against stdlib

(define (strlen string)
   (let ((function (stdlib (int "strlen" '*))))  ;; retrieve strlen function as a procedure
   (function (string->pointer string))))
```

AFAIK, there is no performance gain in memoizing stdlib or function.
Where to go from here?

If you need to bind structures the proper way to go is to use scheme bytestructures.
The code

```
(use-modules (system foreign))

(define* (dynamic-link* #:optional library-name)
   (let ((shared-object (if library-name (dynamic-link library-name)
(dynamic-link))))
     (lambda (return-value function-name . arguments)
       (let ((function (dynamic-func function-name shared-object)))
         (pointer->procedure return-value function arguments)))))
```

That's all folks!
