# 2019/07/07 - SPARQL to Scheme Generic Tuple Store (nstore)

SPARQL is Resource Description Framework (RDF) query langauge.  It
allows to query triple stores and quad stores (called named graph).

Scheme Generic Tuple Store is work-in-progress Scheme Request For
Implementation (SRFI) dubbed 168. It embeds a triple store or quad
store or set of tuples of n items in Scheme programming language.

It rely on a pattern matching query semantic similar to SPARQL upon
which minikanren logic language can be bound.

In the following, I will show how to translate some SPARQL queries
into Scheme code.

In what follow we consider the following two stores. A triple store:

```scheme
(define triplesotre (nstore #vu8(00) '(subject predicate object)))
```

And a quad store:

```scheme
(define quadstore (nstore (#vu8 01) '(graph subject predicate object)))
```

And `tx` is a transaction object.

## Data Types

The supported data types are composition of the follow basic Scheme
types:

- boolean
- numbers (big integers, float and double)
- symbol
- string
- bytevector
- list (soon)
- vector (soon)

There is no specific handling of date time objects or URIs.

## Simple query

### SPARQL

```SPARQL
SELECT ?title
WHERE
{
  <http://example.org/book/book1> <http://purl.org/dc/elements/1.1/title> ?title .
}
```

### Scheme

```scheme
(nstore-query
  (nstore-from tx triplestore
               (list 'http://example.org/book/book1
                     'http://purl.org/dc/elements/1.1/title
                     (nstore-var 'title))))
```

### SPARQL

```SPARQL
PREFIX foaf:   <http://xmlns.com/foaf/0.1/>
SELECT ?name ?mbox
WHERE
  { ?x foaf:name ?name .
    ?x foaf:mbox ?mbox }
```

### Scheme

```scheme
(nstore-query (nstore-from tx triplestore
                           (list (nstore-var 'graph)
                                 'http://xmlns.com/foaf/0.1/name
                                 (nstore-var 'name)))
              (nstore-where tx triplestore
                            (list (nstore-var 'graph)
                                  'http://xmlns.com/foaf/0.1/mbox
                                  (nstore-var 'mbox))))
```

If you prefer, you can define a procedure in Scheme:

```scheme
(define (foaf symbol)
  (string->symbol (string-append "http://xmlns.com/foaf/0.1/" (symbol->string symbol))))
```

And then the query becomes:

```scheme
(nstore-query (nstore-from tx triplestore
                           (list (nstore-var 'graph)
                                 (foaf 'name)
                                 (nstore-var 'name)))
              (nstore-where tx triplestore
                            (list (nstore-var 'graph)
                                  (foaf 'mbox)
                                  (nstore-var 'mbox))))
```

## `FILTER`

### SPARQL

```SPARQL
PREFIX  dc:  <http://purl.org/dc/elements/1.1/>
SELECT  ?title
WHERE   { ?x dc:title ?title
          FILTER regex(?title, "^SPARQL")
        }
```

### Scheme

```scheme
(gfilter (lambda (binding) (string-prefix? "SPARQL" (hashmap-ref binding 'title)))
  (nstore-query (nstore-from tx triplestore
                             (list (nstore-var 'x)
                                   'http://purl.org/dc/elements/1.1/title
                                   (nstore-var 'title)))))
```

### SPARQL

```SPARQL
PREFIX  dc:  <http://purl.org/dc/elements/1.1/>
PREFIX  ns:  <http://example.org/ns#>
SELECT  ?title ?price
WHERE   { ?x ns:price ?price .
          FILTER (?price < 30.5)
          ?x dc:title ?title . }
```

### Scheme

```scheme
(gfilter (lambda (binding) (< (hashmap-ref binding 'price) 30.5))
  (nstore-query (nstore-from tx triplestore
                             (list (nstore-var 'x)
                                   'http://example.org/ns#price
                                   (nstore-var 'price)))
                (nstore-where tx triplestore
                              (list (nstore-var 'x)
                                    'http://purl.org/dc/elements/1.1/title
                                    (nstore-var 'title)))))
```

## `OPTIONAL`

### SPARQL

```SPARQL
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
SELECT ?name ?mbox
WHERE  { ?x foaf:name  ?name .
         OPTIONAL { ?x  foaf:mbox  ?mbox }
       }
```

### Scheme

JOKER!

## `UNION`

### SPARQL

```sparql
PREFIX dc10:  <http://purl.org/dc/elements/1.0/>
PREFIX dc11:  <http://purl.org/dc/elements/1.1/>

SELECT ?title
WHERE  { { ?book dc10:title  ?title } UNION { ?book dc11:title  ?title } }
```

### Scheme

```scheme
(gappend
  (nstore-select (nstore-from tx triplestore
                              (list (nstore-var 'book)
                                    'http://purl.org/dc/elements/1.0/title
                                    (nstore-var 'title))))
  (nstore-select (nstore-from tx triplestore
                              (list (nstore-var 'book)
                                    'http://purl.org/dc/elements/1.1/title
                                    (nstore-var 'title)))))
```

You are not obliged to copy-paste and you can factor queries...

## `FILTER NOT EXISTS`

JOKER

## `FILTER EXISTS`

JOKER

## `MINUS`

JOKER

## BIND

Use `gmap`

## `GROUP BY`

JOKER

## `HAVING`

Use `gfilter`

## Sub-queries

Trivial.

## Graph queries

Trivial.

## `ORDER BY`

JOKER

## `DISTINCT`

JOKER

## `LIMIT ... OFFSET ...`

Use `gtake` and `gdrop`.
