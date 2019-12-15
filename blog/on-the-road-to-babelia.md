# 2019/11/15 - On the road to guile-babelia

Yeah, I am back in GNU Guile land. With yet another good name for the
very same project that boils down to fight boredom, learn new skills
and bring back the power to the computers of every lambda users.

Quick flashback: I started with a minimal bulletin board more than
15 years ago. It was all good, and some success, lost all the backup
and to repeat the same mistake: poor software pratices. Nevermind, it was
mostly copy-pasted LAMP stack code written on Windows 2000. The lost
backups will haunt me back for sure. But what does not?! Then I tried
with Python, Django, Flask, MongoDB, Neo4J, PosgreSQL, Whoosh, skipped
ElasticSearch, read a few hundreds of lines of Lucene documentation
and code. Dozens of science papers. Enjoy Ordered Key-Value Store all
the way down. Re-discovered fuzzbuzz. Learned Scheme. gnunet is making
progress. Dozen of prototypes on various subjects. I have a very good
idea of the graphical user interface in terms of web stack (to get the
project started). Various good good discussions happening around rdf,
AI-KR, GOFAI. And a glimpse into proprietary commercial system that
have great success.

Eventually, more or less, a roadmap for the next five decaces.

I have two immediate pain points:

- gmail. I hate that interface. I much prefer inbox. I could upgrade
  ff.js framework. But meh. And Gambit is missing some library. I
  tried to help but then lost interest, temporarly, because the next
  point is more important.

- Search engine overall user experience: simply said I want to own all
  the data I search and that should not be scatered in various
  privative or hidden sqlite files! I want an IDE of my research
  adventures. I do not want to do 3 or more clicks and fail to
  retrieve the paper I read 3 days or 3 years ago that is now not
  publicly accessible. I want to ban medium.com from my search
  results.  But still, unhide it in case of boredom or emergency.

You prolly guessed, that I want a personal search engine.

Here is in no particular order pieces that I think are missing in GNU Guile:

- headless firefox driver for crawling Single-Page-Application,
- a smart crawler (see what use Common Crawl),
- news.ycombinator.com (meh) html snapshot,
- stackoverflow html snapshot,
- quora snapshot? not sure it is possible, it is a walled garden,
- wet/warc file parser,
- Common Crawl support,
- Somekind of wet/warc file consumer that will (only) build page/domain ranks.
- A fork of Grammar Link in pure Guile (with minisat bindings) to... check pages grammar.
- a word2vec and paragraph2vec similar to Gensim and Spacy that would
  allow to finger print the subject of domains / webpages against
  wikipedia vital articles hierarchy.

Sure all this stuff can be put together in a few days by a junior
architect using a franken-assemblage, to quote myself:

> We could argue indefinitly that one or more of those requirements
> are unnecessary, overkill and YAGNI. We could argue that by relaxing
> a few of the requirements, a particular software or set of softwares
> can come close. We could argue endlessly that building
> yet-another-database [or search engine] is NIH, wheel re-invention
> that curse the software industry with fragmentation and fatigue. We
> could invoke UNIX philosophy, entreprise software architectures,
> experiences, know-how, failed patterns, decades of good services and
> big communities.

Blue pill: To use a vocabulary that has a lot mindshare: that is my product, isn't?

Red pill:

> "Plans are only good intentions unless they immediately degenerate
> into hard work"
>
> Peter Drucker
