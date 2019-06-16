# 2019/06/16 - Generic Tuple Store

## Keywords

- Database
- Resource Description Framework
- SRFI-168

## Kesako a tuple store?

In [SRFI-168](https://srfi.schemers.org/srfi-168/) a tuple store is defined
as follow:

> a tuple store is an ordered set of tuples.

If you prefer, replace "ordered" with "sorted" (I am not sure what is
the difference). Anyway, the order is the lexicographic order given by
the bytes packing procedure. That can be summarized as: items of the
same type are ordered using their natural order. For instance the
number `2` is smaller that the number `10` but the string `"2"` is
bigger than `"10"`.

The comparison between items of different types is defined but it
doesn't matter for what is following.

## Why Generic?

As explained in
[Frey:2017](http://www.semantic-web-journal.net/content/evaluation-metadata-representations-rdf-stores-0)
named graph perform better at metadata representation than other
strategies. Similarly, nstore excels at representing metadata about
triples or quads. In general, whenever you need to attach some
information to all tuples you can add an item to the tuple to do so.

The canonical Resource Description Framework (RDF) naming of tuple
items are for triple stores:

```scheme
(subject predicate object)
```

For named graph (ngraph) or quad store you prefix the tuple with
`graph`:

```scheme
(graph subject predicate object)
```

If you come from mongodb world, you will have an easier time with
the following naming:

```scheme
(collection object-id key value)
```

If you come from the RDBMS world, you will prefer the following
naming:

```scheme
(table primary-key column-name value)
```

It consider that every row as a primiary key, like in google spanner
[`Corbett:2012`](https://ai.google/research/pubs/pub39966) and most
relational databases I encountered.

In RDBMS when you need to add information to a row, you add column.
That would be equivalent in the RDBMS to RDF mapping to add a
**tuple** to every `primary-key` from a `table` with the given
`column-name`.

The **strict** equivalence in RDF would be, instead, to add an
**item** to every tuple, which is [not yet part of the
specification](https://github.com/w3c/sparql-12/issues/98).

Based on that reflexion, one might argue that RDBMS is more powerful
than RDF or nstore.

## n+1 tuple items

To give some food for thought, try to imagine how to represent
metadata like:

- provenance / source of row values
- license of row values
- history of row values

Done figuring a good schema for that problems?

---

This is difficult.

There is some prior art, like the
[Entity-Attribute-Value](https://en.wikipedia.org/wiki/Entity%E2%80%93attribute%E2%80%93value_model)
model that is used in [magento
CRM](https://en.wikipedia.org/wiki/Magento).

That example use of EAV model, a triple store, in magento is
interesting.  Basically, magento try to be "ready" for every possible
schema by choosing the triple representation. The meme is it has too
many downsides. I argue that this comes from a time where the problem
was different. In particular, hard disk is cheaper nowdays. Also,
event-sourcing architecture has proven that it is completly feasible
to store a lot of data in a
[Single-Source-Of-Thruth](https://en.wikipedia.org/wiki/Single_source_of_truth)
that can written to very quickly and expose "views" of that data in
secondary systems.

You might think, that representing provenance, license for a single
value is overkill. But that is problem that wikidata has and almost
all data science projects should have the same issue if they consider
reproducibility and quality assurance.

Also, regarding keeping track of values history, they are known
audit-trails in the wild. They don't allow time-traveling queries.
Most of the time, it is not systematic. If you have a new table you
have to build a new audit-trail table OR rely on EAV model.

So we are back at triple stores.

What is nice about a triple store, is that they allow to to represent
every kind of facts whether it is relational / graphical, tabular or
documents. And every fact, has its own row. And if you want you can
reify a given triple to add more facts about it. That what
[`Frey:2017`](http://www.semantic-web-journal.net/content/evaluation-metadata-representations-rdf-stores-0)
explains. Most of those technics require to do more **join on every
tuple** to be able to query to fetch the particular information
(provenance, license, history). nstore avoids those extra joins, as
the metadata is stored along the rest of the tuple.
