# 2018/01/01 - A Graph-Based Movie Recommender Engine Using Guile Scheme

The goal of this article is to introduce the `grf3` graphdb library
and its graph traversal framework named traversi. To dive into
traversi, we will implement a small recommender system over the
movielens dataset.

### grf3 graphdb library

`grf3` is graph database library built on top of an *assoc space*
persisted to disk thanks to [wiredtiger](http://wiredtiger.com).

#### Basics

Basically you create vertices using `(create-vertex assoc)` and
`(create-edge start end assoc)` where `ASSOC` must be an alist with
symbol keys and any serializable scheme value as value. `START` and
`END` must be `<vertex>` see below. Those procedures will return
respectively a `<vertex>` and `<edge>` record.

Both `<vertex>` and `<edge>` have an assoc and unique identifier named
`uid`.  They have sugar syntax to interact with the assoc via
`(vertex-set vertex key value)`, `(vertex-ref vertex key)`, `(edge-set
edge key value)` and `(edge-ref edge key)`. Mind the fact that `-set`
procedures have no `!` at the end which means they return a new
record.

`<edge>` has two specific procedure called `edge-start` and `edge-end`
which will return the unique identifier the start vertex and
respectively the end vertex.

`(get uid)` will return a `<vertex>` or `<edge>` with `UID` as unique
identifier.

`(save vertex-or-edge)` will persist changes done to a vertex or edge.

That is all for the basics of the `grf3` library. If you experiment a
little with the library in the REPL you will notice that the `assoc`
associated with `<vertex>` and `<edge>` contains more than what you
put in it. NEVER change the keys that starts with `%` char or the
database will break.

#### traversi stream framework

*traversi* is a port of Tinkerop's Gremlin to scheme using streams
implemented using delayed lambda evaluation. This does not use srfi-41
because srfi-41 is slower.

The API is similar to srfi-41:

- `(list->traversi lst)`
- `(traversi->list lst)`
- `(traversi-car traversi)`
- `(traversi-cdr traversi)`
- `(traversi-map proc traversi)`
- `(traversi-for-each proc traversi)`
- `(traversi-filter proc traversi)`
- `(traversi-backtrack traversi)` will backtrack to the value
  that produce the current value by the previous call to
  `traversi-map`.
- `(traversi-take count traversi)`
- `(traversi-drop count traversi)`
- `(traversi-length traversi)`
- `(traversi-scatter traversi)` takes a traversi of lists (where each
  value of the stream is a list) and convert all the thing to single
  traversi composed of the value containes in the lists of the stream.
- `(traversi-unique traversi)` keep only on occurence of each value.
- `(traversi-group-count traversi)` return an alist with the count of
  each value.

### helpers

Here is a few helpers:

- `(vertices)` return a traversi made of all the vertex **uids** found
  in the database
- `(edges)` return a traversi made of all the edge **uids** found in
  the database
- `(from key value)` return elements which the value associated with
  `KEY` is `equal?` to `VALUE`
- `((where? key value) uid)` predicate procedure which will return
  `#true` if the element `UID` has `VALUE` as `KEY`.
- `((key name) uid)` return the value of `KEY` for the element which
  has `UID` as unique identifier.
- `((key? name value) uid)` predicate procedure which will return
  `#true` if the element which has `UID` as unique identifier has a
  `(name . value)` pair in its assoc.
- `(incomings uid)` return a list made of the *incoming edges* of the
  element `UID`. `UID` must be the identifier of a vertex. If `UID` is
  the identifier of an edge it will return an empty list (except if
  the database is broken).
- `(outgoings uid)` return a list made of the *outgoings edges* of the
  element `UID`. `UID` must be the identifier of a vertex. If `UID` is
  the identifier of an edge it will return an empty list (except if
  the database is broken).
- `(start uid)` if `UID` is the identifier of an edge return the edge's
  *start node*. Otherwise the behavior is not specified.
- `(end uid)` if `UID` is the identifier of an edge return the edge's
  *end node*. Otherwise the behavior is not specified.

Last but not least, there is `(get-or-create-vertex key value)` which
will create a vertex with `((key . value))` if there is not vertex
with such a pair or return the existing vertex otherwise.

## Using a graphdb to do recommendation

Now we will put this all together to movie recommendations.

### Getting started

First you need a bit of setup.

Clone the culturia repository using the following command:

```bash
> git clone https://github.com/amirouche/Culturia
```

Rendez vous inside the `src` directory, create a `data` directory and
inside that directory download the movielens small dataset and
decompress the archive:

```bash
> cd Culturia/src
> mkdir data
> wget http://files.grouplens.org/datasets/movielens/ml-latest-small.zip
> unzip ml-latest-small.zip
```

Go back the `src` directory, create a `/tmp/wt` directory, study a
little the `movielens-step00-load.scm` file using your favorite editor
emacs and fire guile to load the dataset as `grf3` database:

```bash
> cd ..
> mkdir /tmp/wt
> emacs movielens-step00-load.scm &
> guile -L . movielens-step00-load.scm
....
```

Loading will take a few minutes.

To understand the graph traversal you need to know how the graph is
drawn. There is three kinds of vertices:

- movie vertices have a `'movie` label, `'movie/id` and a `'movie/title`
- genre vertices have a `'genre` label and a `genre/title`.
- user vertices have a `user` label and a `'user/id`

There is two kinds of edges:

- edges starting at movies, which connects to a genre vertex labeled
  as `'part-of`
- edges starting at users, which connects to a movie vertex labeled as
  `rating`. They also have a `rating/value` integer value.

Here is a schema of the graph mapping:

![graphdb mapping](movielens.png)

Fire guile REPL and import all the things:

```bash
> guile -L .
GNU Guile 2.1.3
Copyright (C) 1995-2016 Free Software Foundation, Inc.

Guile comes with ABSOLUTELY NO WARRANTY; for details type `,show w'.
This program is free software, and you are welcome to redistribute it
under certain conditions; type `,show c' for details.

Enter `,help' for help.
scheme@(guile-user)> (use-modules (ukv) (grf3) (wiredtigerz) (wiredtiger) (ice-9 receive) (srfi srfi-26))
```

Open an environment over the `/tmp/wt` directory:

```scheme
scheme@(guile-user)> (define env (env-open* "/tmp/wt" (list *ukv*)))
```

You are ready!

### Forward

First we would like to know which movie has the id `1`:

```scheme
scheme@(guile-user)> (with-context env (traversi-for-each pk (traversi-map get (from 'movie/id 1))))

;;; (#<<vertex> uid: "V6HM7CEX" assoc: ((movie/title . "Toy Story (1995)") (movie/id . 1) (%kind . 0))>)
```

Remember that every time you access the database in the REPL you need
to wrap the call using `with-context`. This is also the prefered way
to work with `grf3` in modules.

Now let's see what genres is *Toy Story*:

```scheme
scheme@(guile-user)> (with-context env (traversi-for-each pk (traversi-map (key 'genre) (traversi-map end (traversi-filter (key? 'label 'part-of) (traversi-scatter (traversi-map outgoings (from 'movie/id 1))))))))

;;; ("Fantasy")

;;; ("Animation")

;;; ("Children")

;;; ("Comedy")

;;; ("Adventure")
```

Seems good to me. Mind the `traversi-scatter` it used just after
`(traversi-map outgoings ...)` this is pattern that you will see very
often.

Now let's do something more complex. We would like to know which movies
are liked by the same people that liked *Toy Story*.

Remember that compose must be read from right to left, which means
in this case bottom-up:

```scheme
(define (users-who-scored-high movie/id)
  (with-context env
   (let ((query (compose
		  ;; fetch the start vertex ie. users
		  (cut traversi-map start <>)
		  ;; backtrack to edge uids
		  (cut traversi-backtrack <>)
		  ;; keep values that are <= 5.0
		  (cut traversi-filter (lambda (x) (<= 4.0 x)) <>)
		  ;; fetch the 'rating/value of each edge
		  (cut traversi-map (key 'rating/value) <>)
		  ;; keep edges which have 'rating as 'label
		  (cut traversi-filter (key? 'label 'rating) <>)
		  ;; scatter...
		  (cut traversi-scatter <>)
		  ;; fetch all incomings edges
		  (cut traversi-map incomings <>))))
	  (traversi->list (query (from 'movie/id 1))))))
```

This is not very useful since we don't know the users, but the final
result might be more interesting because we might now the movies (or
at least we can STFW).

As an exercise check that the uids that were fetched are really user
vertex.

Now will check the users likes and *group-count* to see if it makes
sens:

```scheme
(define (users-top-likes users)
  (with-context env
    (let ((query (compose
                  (cut traversi-group-count <>)
                  ;; retrieve movie vertex's title
                  (cut traversi-map (key 'movie/title) <>)
                  (cut traversi-map end <>)
                  ;; retrieve rating edges with a score of at least 4.0
                  (cut traversi-backtrack <>)
                  (cut traversi-filter (lambda (x) (<= 4.0 x)) <>)
                  (cut traversi-map (key 'rating/value) <>)
                  (cut traversi-filter (key? 'label 'rating) <>)
                  (cut traversi-scatter <>)
                  (cut traversi-map outgoings <>)
                  (cut list->traversi <>))))
      (list-head (query users) 10))))
```

The above algorithm is available in the
`culturia/src/movielens-step01-recommend.scm` file.

See by yourself!
