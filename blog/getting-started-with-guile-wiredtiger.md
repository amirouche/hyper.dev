# 2016/01/01 - Getting started with guile-wiredtiger

guile-wiredtiger is a library binding wiredtiger which is database
library. I like it because I don't like/master SQL. Other people use
it to build real databases like mongodb. Myself I've done one or two
toy projects using it like planetplanet clone.

wiredtiger is low level compared to a SQL database.

I can't convince you to use it, but I can show you how it works.

### Ground zero

Download
[wiredtiger 2.6.1](http://source.wiredtiger.com/releases/wiredtiger-2.6.1.tar.bz2)
and install it using the usual cli dance. Then retrieve wiredtiger
repository with git:

```
git clone https://git.framasoft.org/a-guile-mind/guile-wiredtiger.git
```

Now go to guile-wiredtiger directory and fire a REPL using the following command:

```
guile -L .
```

Mind the dot.

### Use wiredtiger

Inside the REPL import the wiredtiger module:

```
scheme@(guile-user)> (use-modules (wiredtiger))
```

### Open a connection

Open a connection against a directory say /tmp/wt:

```
scheme@(guile-user)> (mkdir "/tmp/wt")
scheme@(guile-user)> (define connection (connection-open "/tmp/wt" "create"))
```

It's always safe to open a connection against a directory using the create argument even if there is already a database inside that directory.

a <connection> is thread-safe.

### Open a session

To jump to using the database you have to open a session:

```
scheme@(guile-user)> (define session (session-open connection))
```

a <session> is not thread-safe.

### Create a table

wiredtiger is nosql but has a concept of table. It's a two columns
layout with sub-columns. The first master column is the key. The
second master column is the value.

This dichotomy is useful because the table is automatically ordered
using the what is stored in the key.

Let's create simple table with a single string sub-column key, and a
single string sub-column value. Yes, columns are typed. Without
further addo:

```
scheme@(guile-user)> (session-create session "table:kv" "key_format=S,value_format=S,columns=(k,v)")
```

It's safe to session-create a table even if it already exists in the database.

Here we created a table named kv as specified above. The key
sub-column is named k and the value sub-column is named v.

Naming columns is optional but required if you want to build indices.
Create an index

To create an index we use the same session-create procedure with
another configuration string.

Say, we want to invert k sub-column with v sub-column ie. create an
index table where the key single sub-column is v from kv table. We can
use the following command:

```
scheme@(guile-user)> (session-create session "index:kv:inverse" "columns=(v)")
```

This instruct wiredtiger to add a row to index:kv:inverse table
everytime a row is added to table:kv where the key single column
content is the content of the column named v in table:kv row.

The index is always synchronized with the reference table for updates,
deletes and inserts.

### Getting started with cursors

#### Insert

A <cursor> is the way to search, navigate, insert and update a
table. This is also used to search and navigate index tables.

Let's open a <cursor> on table:kv:

```
scheme@(guile-user)> (define cursor (cursor-open session "table:kv"))
```

Let's add a record ie. a key/value pair inside the table:

```
scheme@(guile-user)> (cursor-key-set cursor "key")
$4 = 0
scheme@(guile-user)> (cursor-value-set cursor "value")
$5 = 0
scheme@(guile-user)> (cursor-insert cursor)
$6 = #t
```

This is bit involving for our simple case of single sub-columns configuration. Define a procedure to add a record with a single procedure:

```
(define (cursor-insert* cursor key value)
  (cursor-key-set cursor key)
  (cursor-value-set cursor value)
  (cursor-insert cursor))
```

And put it to good use:

```
scheme@(guile-user)> (cursor-insert* cursor "another" "record"))
$7 = #t
scheme@(guile-user)> (cursor-insert* cursor "something" "else")
$8 = #t
```

#### Search

To look into the table, you also have to use the wiredtiger primitive cursor-key-set followed by cursor-search or cursor-search-near.

For instance, we can do:

```
scheme@(guile-user)> (cursor-key-set cursor "key")
$10 = 0
scheme@(guile-user)> (cursor-search cursor)
$11 = #t
scheme@(guile-user)> (cursor-value-ref cursor)
$12 = ("value")
```

The return value of cursor-value-ref is a list because there might be
several sub-columns in a master column. Similarly cursor-key-ref
returns a list:

```
scheme@(guile-user)> (cursor-key-ref cursor)
$13 = ("key")
```

Unsuprisingly this returns key because the cursor was positioned at
that key using search. This is not a relevant call to do after
cursor-search because cursor-search does an exact match of the key or
match nothing. This is not the case of cursor-search-near which use
some heuristic to find the nearest key. We will study this, but first
let's define cursor-search-near star:

```
(define (cursor-search-near* cursor key)
  (cursor-key-set cursor key)
  (cursor-search-near cursor))
```

And try it:

```
scheme@(guile-user)> (cursor-search-near* cursor "ke")
$14 = 1
scheme@(guile-user)> (cursor-key-ref cursor)
$15 = ("key")
```

As you can see cursor-search-near star ie. cursor-search-near returns 1
instead of true or false like cursor-search. cursor-search-near is
very useful. I warmly recommend you have a look at its documentation.
Navigate

We can verify that the table is correctly ordered. Remember we
inserted the following keys: key, another and something.

So in theory we should see them appearing in the alphabetic aka. the
lexicographic order.

Let's reset the cursor position and navigate the database:

```
scheme@(guile-user)> (cursor-reset cursor)
$21 = #t
scheme@(guile-user)> (cursor-next cursor)
$22 = #t
scheme@(guile-user)> (cursor-key-ref cursor)
$23 = ("another")
scheme@(guile-user)> (cursor-next cursor)
$24 = #t
scheme@(guile-user)> (cursor-key-ref cursor)
$25 = ("key")
scheme@(guile-user)> (cursor-next cursor)
$26 = #t
scheme@(guile-user)> (cursor-key-ref cursor)
$27 = ("something")
```

All is good.

You can also mix cursor-search[-near] with cursor-next and
cursor-previous. Don't forget to read wiredtiger error output ;)

#### Remove

To remove a record, just set cursor's key content, an remove it using cursor-remove:

```
scheme@(guile-user) [1]> (cursor-key-set cursor "key")
$28 = 0
scheme@(guile-user) [1]> (cursor-remove cursor)
$29 = #t
```

Let's check that this code, is doing what it's supposed to be doing:

```
scheme@(guile-user)> (cursor-key-set cursor "key")
$30 = 0
scheme@(guile-user)> (cursor-search cursor)
$31 = #f
```

cursor-search returns false, which means the key is not found.

Try again with cursor-search-near star.
