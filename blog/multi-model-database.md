# 2019/06/12 - On the road to a multi-model database

To get a good grasp of what graphdb were, I mocked a graph database
using Python 2.6's anydbm in a project dubbed [ajgu
(2010)](https://pypi.org/project/ajgu/0.1.0/#history).

I created [Graphiti
(2012)](https://bitbucket.org/amirouche/graphiti-unmaintained/) which
was an Object-Relational Model framework for representing graphical
data in your favorite Object-Oriented Programming language, namely
Python. I promise at some point it was working. And I promise, nowdays
I can code better. That project teached the following lesson:
embedding the full query language of graphical databases inside Python
without relying on string interpolation is not possible.

Given it was not possible to embed nicely another Turing Complete
language inside Python, I tried to embed Python inside Tinkerpop in
[GraphitiDB (2013)](https://bitbucket.org/amirouche/java-graphitidb/).
I promise it was working at some point. To me, that was mostly a
failure because it was not really possible to send Python queries
directly from Python code without relying on string interpolation.

also tried to bind [Tinkerpop's Blueprints
(2013)](https://pypi.org/project/Blueprints/#history) inside
Python. It was very slow.

And I figured something else. Using Tinkerpop, unlike with PostgreSQL,
I had to rely on another database to do full-text search and
geospatial queries which would break the ACID semantic I was so
attached to.

I continued working on ajgu all along. At some point I renamed it
[AjguDB (2015)](https://pypi.org/project/AjguDB/0.1/#history). This is
the first version that rely on [Entity-Attribute-Value Model
abstraction](https://en.wikipedia.org/wiki/Entity%E2%80%93attribute%E2%80%93value_model).
That inspired the post: [Do-It-Yourself: A Graph Database In
Python](/blog/diy-graph-database-in-python.html).

At this point, I knew that building a **database** in Python was bad
idea [0].  So, I pivoted into an "graph exploration tool" but never
really executed that idea.

Along the way, I got lost a little regarding my goal. My initial idea
was to create a general purpose database that support transactions all
around.

For other reasons I learned Scheme programming language. GNU Guile did
not have a Global Interpreter Lock and performance were better than
CPython. I continued experimenting with ordered key-value stores.  I
have written several posts regarding this work:

- [Somewhat Relational Database Library Using Wiredtiger (2016)](/blog/somewhat-relational-database-library-using-wiredtiger.html)
- [Getting started with guile UAV database (2016)](/blog/getting-started-with-guile-uav-database.html)
- [Getting started with guile-wiredtiger (2016)](/blog/getting-started-with-guile-wiredtiger.html)
- [Do It Yourself: a search engine in Scheme Guile (2016)](/blog/diy-a-search-engine-in-gnu-guile.html)
- [A Graph-Based Movie Recommender Engine Using Guile Scheme (2016)](/blog/a-graph-based-movie-recommender-engine-using-guile-scheme.html)

Since, the beginning I always wrapped inside classes and Python
objects the abstractions I was building. Somekind of Object-Oriented
Programming made things, very difficult to interop and compose
abstractions. To be honest, even the Scheme functional code was not
easy to compose.

Even the successor of ajgu, namely
[hoply](https://github.com/amirouche/hoply/) is still broken in this
regard.

That is when I FoundationDB was open-sourced that I figured that the
ordered key-value store doesn't have to be hidden. That is the
underlying abstraction can leak on purpose because it helps to build
higher level abstractions, compose them and generaly reach somekind of
fractal architecture.

I have put in motion that idea in
[SRFI-167](https://srfi.schemers.org/srfi-167/) with an exampe
abstraction [SRFI-168](https://srfi.schemers.org/srfi-168/) [1].  That
is, abstractions on top of SRFI-167 shall not hide the ordered
key-value store and accept `prefix` to allow to hook it
somewhere. Also, it should be possible to nest abstractions to be
fractal. This is not possible in the sample implementation because
the packing procedure don't support nested datastructures, as of yet.

So, if you wanted you could build a triple store on top a triple
store.  That is already a thing and some do n-tuples inside triple
store. Based, on my analysis this is not great in terms of
performance.

Or you could star
[datae](https://github.com/awesome-data-distribution/datae).

[0] [edgedb](https://edgedb.com/).

[1] This is still a work-in-progress and we very recently released
    another draft. Chime in!
