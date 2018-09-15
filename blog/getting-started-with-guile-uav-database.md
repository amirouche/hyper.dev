# 2016/01/01 - Getting started with guile UAV database

UAV database is a tuple space database that is easy to use and easy to
grasp. There is also a database server that allows to query the database
from multiple processus.

We will get started by using the database directly without the database
server illustrated with an music album collection kind of stuff and then
will open the road to use the database server.

You can fetch the lasted version of UAV database using git:

```
git clone https://framagit.org/a-guile-mind/guile-wiredtiger.git
```

### UAV Tuple Space

What is the tuple space? It's table with three columns.

In what follows we consider the following assoc:

```
(define lagale-lagale
    '((artist . "La Gale")
      (title . "La Gale")
      (year . 2012)))
```

#### Give me a `U`

The first column `U` stands for *unique identifier*. it's a random
string assigned the first time you add an assoc to the database. A
single assoc is represented with several rows in the table but share
the same identifier.

#### Give me a `A`

`A` stands for *attribute name*. In the above example it's `title` and
`year`. In this case attributes are symbols but can be any scheme
value that can be serialized with `write`.

#### Give me a `V`

The last column is `V` for *value*. It can be any scheme value that
can be serialized with `write`.

#### Wrapping up

If we add `lagale-lagale` to the database, and the assigned unique
identifier is `ABCDE`, the database will more or less look like the
following:

```
    uid  |  attribute |   value
  =======+============+===========
   ABCDE |   artist   | "La Gale"
  -------+------------+-----------
   ABCDE |   title    | "La Gale"
  -------+------------+-----------
   ABCDE |    year    |   2012
```

### API

Fire an REPL inside the wiredtiger directory using the following command:

```
wiredtiger $ guile -L .
```

#### Open the database

And load the `uav` module with:

```
(use-modules (uav))
```

To get started you need to open database:

```
(define connexion (uav-open* "/tmp/"))
```

#### Add a document to the database

To add a document to the database you simply format you data into an
assoc and use uav-add!:

```
(define uid (uav-add! '((artist . "La Gale")
                        (title . "La Gale")
                        (year . 2012))))
```

#### Debug the database

There is a debug procedure that allows to have a pick at the
underlying schema.  Using `uav-debug` you will get something like the
following:

```
scheme@(guile-user)> (uav-debug)

;;; (key ("DZI3P5MU" "artist"))

;;; (value ("\"La Gale\""))

;;; (key ("DZI3P5MU" "title"))

;;; (value ("\"La Gale\""))

;;; (key ("DZI3P5MU" "year"))

;;; (value ("2012"))
```

#### Referencing a document

Now you can use `uav-ref*` to retrieve the document using its `uid`:

```
scheme@(guile-user)> (uav-ref* uid)
$3 = ((year . 2012) (title . "La Gale") (artist . "La Gale"))
```

#### Update a document

We assigned previously the identifier of *La Gale* album to `uid`.

We can with this information update the document with `uav-update!`.
The thing to keep in mind is that this procedure updates the whole
document so you need first to retrieve the original assoc, update
the assoc and commit the new version using `uav-update!`.

For instance, let's add the *genre* to the assoc:

```
scheme@(guile-user)> (uav-ref* uid)
$6 = ((year . 2012) (title . "La Gale") (artist . "La Gale"))
scheme@(guile-user)> (acons 'genre "Hip Hop" $3)
$7 = ((genre . "Hip Hop") (year . 2012) (title . "La Gale") (artist . "La Gale"))
scheme@(guile-user)> (uav-update! uid $7)
scheme@(guile-user)> (uav-ref* uid)
$8 = ((year . 2012) (title . "La Gale") (genre . "Hip Hop") (artist . "La Gale"))
```

Let's check the output of `uav-debug`:

```
scheme@(guile-user)> (uav-debug)

;;; (key ("DZI3P5MU" "artist"))

;;; (value ("\"La Gale\""))

;;; (key ("DZI3P5MU" "genre"))

;;; (value ("\"Hip Hop\""))

;;; (key ("DZI3P5MU" "title"))

;;; (value ("\"La Gale\""))

;;; (key ("DZI3P5MU" "year"))

;;; (value ("2012"))
```

There is a new key/value pair with a `genre` attribute associated with
`"Hip Hop`.

#### How to delete a document

To delete a document you simply use `(uav-del! uid)` procedure:

```
scheme@(guile-user)> (uav-del! uid)
scheme@(guile-user)> (uav-debug)
scheme@(guile-user)>
```

As you can see `uav-debug` displays nothing, the database is empty!

#### attribute-value index reference

You can retrieve document using *attribute-value* association. Otherwise
said, you can retrieve every document that has a given attribute/value pair
in its assoc.

Let re-add `lagale-lagale` to the database an try to retrieve it by year:

```
scheme@(guile-user)> (uav-add! '((artist . "La Gale")
                                 (title . "La Gale")
                                 (year . 2012)))
```

Let's add another album

```
scheme@(guile-user)> (uav-add! '((artist . "La Gale")
                                 (title . "Salem City Rocker")
                                 (year . 2015)))
```

Let's add the album of another artist:

```
scheme@(guile-user)> (uav-add! '((artist . "Mighz")
                                 (title . "Equilibre")
                                 (year . 2015)))
```

Now it's funny enough to query the database! Let's try `uav-index-ref`:

```
scheme@(guile-user)> (uav-index-ref 'year 2012)
$16 = ("3UTO7NW0")
scheme@(guile-user)> (uav-index-ref 'year 2015)
$17 = ("WCKA2IWH" "PQVA9NBB")
```

That's all folks!
