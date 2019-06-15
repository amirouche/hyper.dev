# 2019/06/15 - Functional Database: Versioned Generic Tuple Store

## Keywords

- Database
- Knowledge Base
- Reproducible Science
- Scheme programming language
- Version Control System

## Summary

Versioning in production systems is a trick everybody knows about
whether it is through backup, logging systems and ad-hoc audit
trails. It allows to inspect, debug and in worst cases rollback to
previous states. There is no need to explain the great importance of
versioning in software management as tools like mercurial, git and
fossil have shaped modern computing.

Having the power of multiple branch versioning open the door to
manyfold applications. It allows to implement a change-request
mechanic similar to github's pull requests and gitlab's merge requests
in any domains.

The change-request mechanic is explicit about the actual human
workflow in entreprise settings in particular when a senior person
validates a change by a less senior person.

Versioning tuples in a direct-acyclic-graph make the implementation of
such mechanics more systematic and less error prone as the
implementation can be shared across various tools and organisations.

Being generic allows downstream applications to fine tune their
time-space requirements. By incrementing the number of items in a
tuple, it allows to easily represent provenance or licence. Thus, it
avoid the need for reification technics as described in
[Frey:2017](http://www.semantic-web-journal.net/content/evaluation-metadata-representations-rdf-stores-0)
to represent metadata on all tuples.

[datae](https://github.com/awesome-data-distribution/datae) is a
software that takes the path of versioning data in a
direct-acyclic-graph. It applies the change-request mechanic to
cooperation around the making of a knowledge base. It is similar in
spirit to wikidata or freebase.

Resource Description Framework (RDF) offers a good canvas for
cooperation around open data but there is no solution that is good
enough according to
[Canova:2015](https://iris.polito.it/handle/11583/2617308).  The use
of a version control system to store open data is a good thing as it
draws a clear path for reproducible science.

In projects like [datahub.io](https://datahub.io) or
[db.nomics](https://db.nomics.world/), datae aims to replace the use
of git.

datae can make practical cooperation around the creation, publication,
storage, re-use and maintenance of knowledge base that is possibly
bigger than memory.

datae use a novel approach to store tuples that is similar in
principle to OSTRICH
[Ruben:2018](https://rdfostrich.github.io/article-jws2018-ostrich/) in
a key-value store. datae use [WiredTiger database storage
engine](http://www.wiredtiger.com/) to deliver a pragmatic versatile
ACID-compliant versioned generic tuple store.

datae only stores changes between versions. To resolve conflicts,
merge commits must copy some changes. datae does not rely on the
theory of patches introduced by Darcs
[Tallinn:2005](https://en.wikipedia.org/wiki/Darcs).

## Current status, and plans for the future

This is stil a work-in-progress. You can find the code at [source
hut](https://git.sr.ht/~amz3/chez-scheme-arew).
