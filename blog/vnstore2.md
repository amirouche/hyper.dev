# 2021/03/15 - Versioned generic tuple store 2

A few years back, I set myself the task to create a versioned
database. I did not come up with that idea myself! Several readings
and professional experiences, lead me to think that was a good idea:

- [AuditTrail - Django As raised in ​a recent discussion on django-developers,
this code is one solution for creating an audit trail for a given model. This
is working in multiple production sites, but is still incomplete. See Caveats
below for more information. The code below requires an SVN checkout as of
r8223 or later.](https://code.djangoproject.com/wiki/AuditTrail)

- [Wikidata Wikidata is a free and open knowledge base that can be read and
edited by both humans and machines. Wikidata acts as central storage for the
structured data of its Wikimedia sister projects including Wikipedia,
Wikivoyage, Wiktionary, Wikisource, and others. Wikidata also provides support
to many other sites and services beyond just Wikimedia projects!](https://www.wikidata.org/wiki/Wikidata:Main_Page)

- [Collaborative Open Data versioning: a pragmatic approach using Linked Data -
CORE By Lorenzo Canova, Simone Basso, Raimondo Iemma and Federico Morando Most
Open Government Data initiatives are centralised and unidirectional (i.e.,
they release data dumps in CSV or PDF format). Hence for non trivial
applications reusers make copies of the government datasets to curate their
local data copy.](https://core.ac.uk/display/76527782?recSetID=)

And most recently:

- [A More Human Approach To Databases End-user databases are all the buzz these
days - Notion, Airtable, Coda, Roam, etc. These products have made it possible
for people to model information in a way that feels more natural and intuitive
to the way we experience it in our daily lives.
https://ccorcos.github.io/filing-cabinets/](https://ccorcos.github.io/filing-cabinets/)

- [Design of system for pending approval and history I am looking for some
insight on how to design a solution that handles both pending changes as well
as a history of an entire entity. I have found several examples of how to
handle this for a single entity object, but I am unsure how to apply this to a
object that can contain several "attached" entities.)](https://stackoverflow.com/questions/66610103/design-of-system-for-pending-
approval-and-history)

I do not claim my approach is bullet proof to every use-case
possible. As its name imply it is a generic solution to implement
versioned database. What the title does not say, is that it support
change request mechanic similar to github pull-requests.

When I started this adventure, the index factor was 120 times the size
of the raw data. Given this factor whether the data is text or bytes
does not matter: one gigabyte times 120 is 120 gigabytes, a lot.

In 2019, I reduced the factor to 10, which is still a lot given at the
time, wikidata was 3 terabytes without change history.

In 2020, thanks to FoundationDB HighContentionAllocator, I managed to
store wikidata lexemes in less space that the textual format. You read
it very well. It requires less space to store the textual data, than
store it inside a database with versioning enabled, and querying
possible in timely manner.

Today, I devised a plan to reduce further the space requirement with
little or no visible feature difference. That further reduce the space
requirement by almost a half.

To summarize: I started with 120 time the size of the data, and today
the versioned and query-able data requires at most 0.6 times the size
of the original data.

## How?

Remember the nstore? It is a generalization of triple stores where the
number of tuple items can be any integer. I used that to drop from 120
to 10. The nstore stored the whole tuple in the key of the okvs. (That
may look like a problem because keys can not grow big, but in practice
since they go through the HighContentionAllocator it is not a
problem). The value was empty!

What I used to think is that when I am required to expose an n
versioned tuple store, I needed n+2 generic tuple store:

> [amirouche/copernic Versioned structured data, with change-request mechanic,
at scale. - amirouche/copernic](https://github.com/amirouche/copernic/blob/131589d2294710da7e737115b0b4dcf38483044c/copernic/vnstore.py#L54-L60)

That is not the case. I can drop the alive? flag from the tuple item
and put it in the value part. That way it reduce the number of items
in a tuple to 4 and according to make_indices that requires only 6
permutations to be able to query any pattern in one hop.

alive? is accessed twice in the current code base. Mind the fact that in both
case alive?.

> [amirouche/copernic Versioned structured data, with change-request mechanic,
at scale. - amirouche/copernic](https://github.com/amirouche/copernic/blob/131589d2294710da7e737115b0b4dcf38483044c/copernic/vnstore.py#L89-L107)

The code says something along the line of:

1. Given a tuple items,

2. Lookup all the history of that items and retrieve their changeid and alive?
status

3. For each of such history item, keep the status alive? of the tuple with the
biggest significance

The returned value called in the above snippet `found` tells whether
items is alive at the latest version of the database.

Another case is the VNStore.FROM does a more general query that try to
bind some patterns against the latest version of the data:

> [amirouche/copernic Versioned structured data, with change-request mechanic,
at scale. - amirouche/copernic](https://github.com/amirouche/copernic/blob/131589d2294710da7e737115b0b4dcf38483044c/copernic/vnstore.py#L129-L159)

What the code says is something along the line:

1. For a given pattern

2. From the versioned tuples, fetch all bindings that match the
pattern and include the alive? and changeid (the latter being useless
in that particular method, but since it is unknown, it can not be
provided by upstream).

3. If the binding is dead aka. `not bindings['alive?']`, then the
binding is not valid in all cases according to the latest version (so,
instead of a variable alive?, we could query with True... see below)

4. Otherwise, if the binding is alive, we check that it is alive at
the latest version. Here lies a bug: if in history there is several
times the same items, that are alive but introduced in different
change, it will yield multiple bindings that are the same. Instead of:

```python
self.ask(*bind(pattern, binding)
```

It should be:

```python
self.latest(bind(pattern, binding), alive=True, changeid=binding["changeid"])
```

Since we are only interested in latest version bindings.

Anyway, my point was that alive? is always a variable (except if we
change that in the third bullet). Also, as part of time traveling
queries, it seems to me rare to query on alive? having a particular
value except when asking for:

> How many times a particular tuple was added or removed

In the case of wikidata, where changes are curated, it seems extremely
unlikely that the same tuple items will be added and removed maybe
times.  Here, there is a choice to be made between CPU time and disk
requirement.

Indeed, I might trade half the space requirements with some CPU time
in some rare cases. Hence the advent of
[nstore2](https://github.com/scheme-
live/live/tree/okvslite-and-co/live/okvslite/nstore2#readme).
