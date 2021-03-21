# 2021/01/10 - Babelia search engine design planning (take three)

![](https://images.unsplash.com/photo-1528076178276-9dff69729561?ixlib=rb-1.2.1&q=85&fm=jpg&crop=entropy&cs=srgb&w=1024)

I recycled two previous notes into one and added some.

I read Steve Jobs said something along the lines of "Before big projects come
big thoughts". I have been brainstorming the next steps of babelia for the
last few weeks. Some of you might think that this is merely procrastinating.
Announcing a project before it is done is against the netiquette, and dubbed
useless. This is not only about bragging about my project and propping up my
ego. One couple of months worth of thinking is a lot of work. There was almost
no production of working code. Product design is a job on its own and hence
deserves some recognition. That recognition will take the form of a blog post,
a few hits on my web server, and I dare hope some feedback!

## Prelude

I read more often than ever that people are looking for ways to build
their own search engines.

Even if more on more "advanced" features are integrated into search
engines.  They are mostly based on human grunt work. Semantic search
engine, whatever "semantic" does mean for you, is in fact merely a
couple, not more than a dozen, set of tricks. I like to say, much of
Google's search engine is good old human labor. If you still doubt it,
here is again: Google results are not only biased, also they are
editorialized. Whether algorithms, and their bugs, party is
irrelevant.

My point is: it is human made. Not some necessarily advanced alien tool.

The only thing preventing you to have your own search engine is there
is no readily available software. In fact, there is
[commonsearch](https://github.com/commonsearch). The reason there is
no public FLOSS search engine is because there is no cheap hardware.

This might sound like a crazy idea five or ten years ago, but with the
advent of AMD Epyc and AMD threadripper ie. [cost gravity at
play](http://cultureandempire.com/html/cande.html) getting together a
personal search engine is, if not a necessity, at least a possibility.

The most common complain I read about Google is that it yields
irrelevant text "that do no even contain my search terms". That is not
a bug, that is a feature! It seems to me the subtext is that you can
not easily customize Google or whatever search algorithm since it is
privateer. Even retrieving Google search results for further
processing if not forbidden, is difficult.

## Big Picture

The primary user interface of a search engine is… dum dum dum… the
search input box. What is interesting is what goes inside it: the
so-called boolean- keyword query. For example:

```
search engine (postgresql OR psql OR pgsql OR postgres) -tsearch2
```

The intention behind that query is to retrieve the attempts to build a
search engine with PostgreSQL without tsearch2 extension. As you see,
the PostgreSQL concept can have multiple realization "psql" or
"pgsql"... This could be handled by the search engine itself with
synonym expansion.

While the discovery of synonyms is not planned, there will be a way
for the user to customize babelia dictionary of lemma, one way
synonyms and two way synonyms with a dedicated knowledge-base. It will
be global to the instance.  It will be built on top of what is known
as [copernic](https://github.com/amirouche/copernic/). If you are too
lazy to click (and star), to put it simply: copernic is a cooperative
knowledge base.

So instead, of typing the above query the user will only have to type
the following:

```
search engine postgresql -tsearch2
```

On the subject of query expansion, I want to stress the importance of:

- Stem
- Lemma
- One-way synonyms
- Two-way synonyms

Possibly other lexical features that can be taken into account. For
instance, the following query:

```
big search engine
```

Can be translated into the following query:

```
(big OR giant OR global) search engine
```

That can entirely be handled by the same machinery.

Another important feature of babelia is that it will both support stem
and lemma. Usually stems allow you to find documents that contain
words that look like the one typed in the query. Imagine the following
query:

```
search engine product
```

You might want to also match the following:

```
search engine production
```

Nowadays this happens automatically. That behavior can be turned off
using double quotes, like:

```
search engine "product"
```

The above query matches documents that contain the exact word "product".

But the above approach does not always work. For instance, given the following
query:

```
avoir le mojo
```

You might want to also match the following:

```
J'ai le mojo
```

Or

```
Il a le mojo
```

Or even:

```
Nous avons le mojo
```

You get it. Stems are a first step toward achieving high precision and
recall because they reduce false negatives, but it does not completely
eliminate the problem. To help with that, babelia will rely on
lemma. Unlike stems, lemma can not be computed automagically, you need
a database, that is another place where the knowledge-base will be
useful.

I read often that you have to use only one of : a) stem or b)
lemma. That is not true. In fact, you can use both.

To help the user a little with typos, babelia will feature a spell
checker that takes its input from the index, so that it can improve
itself without the need to manually update the dictionary. In the next
sprint, I will only support ascii and languages that can be easily
transliterated to ascii like french, Spanish, Italian, unlike Chinese,
Korean and Japanese which are out-of-scope of the next alpha.

Another aspect that I prototyped in faux-texte, is query
suggestion. Since, I do not have a vast amount of user queries, I can
not compute nearest neighbors using word2vec or BERT with the help of
something like
[faiss](https://github.com/facebookresearch/faiss/wiki/Getting-started). I
could do that against the index. Instead of considering user queries,
which is not very privacy preserving, it will rely on the documents
that were indexed.  At index time, babelia will build a Markov-chain
that will allow babelia to complete and mix-and-match queries.

Queries will be limited to one second at most. The limit will be based
on word frequency and computed on available hardware. To workaround
that limitation the user will be suggested related queries constructed
with the help of Markov-chains described above.

One last aspect regarding queries. This is a significant feature,
because the tagline of the project stems from that feature: the
federation. Because of privacy, the queries will not be distributed
all the time to other babelia instances. Instead, every babelia
instance will advertise a summary of the content of their index. In
case the user requests it or if there is no results in the current
instance, babelia will analyze the terms and match them with other
babelia instances and the user will be able to decide whether to
remotely submit that query.

Problem:

If 10 users share a single server with 20 cores, hence 40 available
threads that cost 100 euros per month (10 euros per person). Each user
does 100 queries per day that last 1 second, the overall server
utilization will still be at 2%. That CPU power needs to shared
otherwise it is wasted.

Call to participation

If you are interested in a FLOSS search engine that is privacy
respecting and most likely more relevant, chime into the conversation
at [<http://peacesear.ch>](http://peacesear.ch/).

You can subscribe to the mailing list, send an email to the following
address to subscribe:

```
~peacesearch/peacesearch-discuss+subscribe@lists.sr.ht
```

## Conclusion

There is a gigantic leap that is going to happen in search because of
hardware availability, and free software with readable source ie. the
only thing that makes human progress possible: knowledge sharing.

> "Plans are only good intentions unless they immediately degenerate
> into hard work." Peter Drucker
