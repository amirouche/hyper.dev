# 2016/01/01 - Somewhat Relational Database Library Using Wiredtiger

This is kind of click bait title, because I'm not going to build a
relational (not even remotly) in this article. But write about how
one can use wiredtiger database like a rdbms.

People don't seem convinced that wiredtiger is the best solution, as
of right now, to create database backed application in Guile. Maybe I
drink too much of my cool aid. But let me try to convince you again.

This time no fancy algorithms, no, no, no minikaren. We will build
a social blogging application using wiredtiger to explicit the fact
that it can be used as an RDBMS. So no fancy tricks outside simple
RDBMS like tables and indices.

And by the way, if you need more performance or other features in
wiredtiger let me know.

If you did not read
[Getting Started With Guile Wiredtiger](/notes/getting-started-with-guile-wiredtiger.html),
please do.

wiredtiger can be downloaded using the following command:

```
git clone https://framagit.org/a-guile-mind/guile-wiredtiger.git
```

To create a guile wiredtiger database you need a Guile REPL.

Ready?!

## Schema

I don't recall the precise semantic that must be used to describe a
relational database schema so I hope the following will do the trick:

```

  *------*           *------*           *------*
  | user | <-------- | blog | <-------- | post |
  *------*           *------*           *------*
     ^                                      ^
     |               *---------*            |
     *-------------- | comment \ -----------*
                     *---------*

```

That is all.

## Another glimpse into wiredtiger

Let's define using the `wiredtigerz` DSL tables and indices for all
the above tables. Remember the language looks like the following:

```
(table-name
 (key assoc as (column-name . column-type))
 (value assoc as (column-name . column-type))
 (indices as (indexed-name (indexed keys) (projection as column names))))

```

Here is the schema of this simple social blogging app platform:

```
(define user '(user
               ((uid . record))
               ((username . string)
                (bio . string)
                (created-at . unsigned-integer))
               ()))  ;; no index

(define blog '(blog
               ((uid . record))
               ((user-uid . unsigned-integer)
                (title . string)
                (tagline . string))
               ((user-to-blog (user-uid) (uid)))))

(define post '(post
               ((uid . record))
               ((blog-uid . unsigned-integer)
                (title . string)
                (body . string)
                (created-at . unsigned-integer))
               ((blog-to-post (blog-uid) (uid)))))

(define comment '(comment
                  ((uid . record))
                  ((post-uid . unsigned-integer)
                   (user-uid . unsigned-integer)
                   (body . string)
                   (created-at . string))
                  ((post-to-comment (post-uid) (uid))
                   (user-to-comment (user-uid) (uid)))))
```

There is several (!) ways to go on now, I try to make the API simple
in the simple case of single threaded applications. So will go on with
that API for now.

`wiredtiger-open` is a do-it-all procedure that return two values.
You will use that:

```
>>> (use-modules (ice-9 receive) (wiredtiger) (wiredtigerz))
>>> (define cursors (receive (db cursors) (wiredtiger-open "/tmp" user blog post comment) cursors))
```

`cursors` is an assoc where actual cursor symbols are associated with
`<cursor>`.  Since all our table have a single record key column there
is three kind of cursors for each table:

- `gnu-append` where `gnu` is the name of the table. This kind of
  cursors allows to insert (or more precisly append) a row in the
  `gnu` table.

- `gnu` which is the cursor useful for doing something else ie. not
  append a row.

- `gnu-index` where `gnu` is the name of the table and `index` the
  name of the... index. This cursor looks like `gnu` cursor except
  that it's read-only.

## Inserting rows

Now we will create a basic user:

```
>>> (cursor-value-set (assoc-ref cursors 'user-append)
                    "amz3"
                    "Guile hacker 4 ever"
                    (current-time))
>>> (cursor-insert (assoc-ref cursors 'user-append))
>>> (define amz3 (car (cursor-key-ref (assoc-ref cursors 'user-append))))
```

`amz3` variable contains the uid of the created user.

Let's add a blog:

```
>>> (cursor-value-set (assoc-ref cursors 'blog-append)
                      amz3
                      "cryotoptography"
                      "random musing")
>>> (cursor-insert (assoc-ref cursors 'blog-append))
>>> (define cryotoptography (car (cursor-key-ref (assoc-ref cursors 'blog-append))))
```

Wonderful!

Let's define a small procedure to *insert* rows to a table quickly:

```
(define (insert cusors table . args)
    (let* ((cursor-name (symbol-append table '-append))
           (cursor (assoc-ref cursors cursor-name)))
        (apply cursor-value-set (cons cursor args))
        (cursor-insert cursor)
        (car (cursor-key-ref cursor))))
```

Let's add a few data to the database

```
>>> (define hyperdev (insert cursors 'blog amz3 "hyperdev" "guile musing"))
>>> (insert cursors 'post hyperdev "RDBMS in GNU Guile" "start with (use-modules (wiredtiger))" (current-time))
>>> (insert cursors 'post hyperdev "GraphDB in GNU Guile" "cf. RDBMS in GNU Guile" (current-time))
>>> (insert cursors 'post hyperdev "Ahah moment" "Goofing while developping GNU Guile application" (current-time))
>>> (insert cursors 'post hyperdev "A glimpse into opencog" "opencog is a kitchen sink" (current-time))
>>> (define abki (insert cursors 'user "abki" "old good things are old" (current-time)))
>>> (define protractile (insert cursors 'blog abki "protractile" "never ending story"))
>>> (insert cursors 'post protractile "Brief introduction to mezangelle" "mezangelle is code poetry" (current-time))
>>> (insert cursors 'post protractile "An Algorithm for poetry" "replace word by definition" (current-time))
```

### Resolving foreign keys

I forgot to add an index to retrieve users by usernames. So let's
assume that we know the identifier associated with usernames like
`abki` and `amz3`.

So we have usernames, let's lists blogs associated with `amz3`. But
first let create a procedure to easily select a single row based on
its primary key (or record number).

```
(define (ref cursors table key)
    (let ((cursor (assoc-ref cursors table)))
          (cursor-search* cursor key)
          (cursor-value-ref cursor)))
```

Let's check that is works correctly:

```
>>> (ref cursors 'user amz3)
("amz3" "Guile hacker 4 ever" 1466961863)
>>> (ref cursors 'user abki)
("abki" "old good things are old" 1466964117)
```

Now we can easily resolve primary keys to rows. Indices as defined
previously only reference the row primary key. This can be configured
otherwise for performance tuning reasons but from a cognitive load
point of view it's easier to only introduce primary key as index
values.

So let's find out what blog has `amz3` and `abki`:

```
>>> (define user-to-blog (assoc-ref cursors 'blog-user-to-blog))
>>> (for-each (lambda (key) (pk key (ref cursors 'blog key))) (map cadr (cursor-range user-to-blog amz3)))
>>> (for-each (lambda (key) (pk key (ref cursors 'blog key))) (map cadr (cursor-range user-to-blog abki)))
```

Similarly we can retrieve the posts associated with a given blog:

```
>>> (define blog-to-post (assoc-ref cursors 'post-blog-to-post))
>>> (for-each (lambda (key) (pk key (ref cursors 'post key))) (map cadr (cursor-range blog-to-post hyperdev)))
```

### Pagination

Pagination is just a matter of slicing the list of primary keys that
you retrieve during index lookup.

That's said sometime you don't have uids at all! And you need to slice
the table directly. In this case it might be faster to retrieve all
primary keys of the table, slice that list of primary key and then `ref`
the primary keys. But this is only a performance trick!
