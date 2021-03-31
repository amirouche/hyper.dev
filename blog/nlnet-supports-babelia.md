# 2021/04/01 - NLnet supports Babelia

I am happy to announce that [nlnet supports
Babelia](https://nlnet.nl/project/Babelia/).

I am very pleased with the financial support, but even more so about
the recognition of my past work, I have been working on this for 10
years, and the immediate efforts on Babelia.

That is the occasion to share rationales, the roadmap I devised
for 10 months, and some technical notes.

## Why a search engine?

TL;DR: I can do better than Google.

Search has been an essential part of knowledge acquisition from the
dawn of time. It is even more prevalent today because it is more
accessible than ever before. Most people have access to a large amount
of knowledge thanks to privateer (sometime wanna-be privacy-friendly)
search engines.

Here is what problems my search engine will solve compared to existing
search engines:

- Free and open search engine that anybody will be free to study,
  fork, and run;

- Hence, it will not be under the control of a single (possibly
  selfish) group. People will be able to tweak it, even without
  programming knowledge thanks to full control over the crawler, with
  control over the knowledge base and with the help of the moderation
  tools;

- It will not be privacy-friendly wann-be: the source code will be
  available for anybody to check any privacy claim I make;

- It may yield more interesting results;

One thing I will not claim is that it will eliminate the [filter
bubble](https://en.wikipedia.org/wiki/Filter_bubble). In a way that is
a similar situation to the fediverse: a self-hosted or community
search engine will entice some kind of filter bubble because of
confirmation bias such as "The results of that instance are good,
hence all results are good", or such as "I agree with the results, so
all results are truthy". Also, because of unknown unknowns. In any
case, it will be, like today, the responsability (and duty) of any
fediverse citizen (fedizen) to cross-check results, and likely escape
the gilded cage they constructed for themself, and their community.

What I can claim is the following: there will be more search engines,
with more diversity, and hopefully expert instances that are curated
fairly.

I build a search engine because that is apparantly the most difficult
software that can be built.

To summarize "why a search engine" boil down to a) the current
situation can be improved, b) I can do better, c) I want my own search
engine.

## Why not an existing FLOSS search engine?

TL;DR: There is none.

Even if some software might qualify as "search engine", the bare
minimal requirement is that they should be written in an easy to the
mind programming language such as Python or... Scheme.

Also, I have added non-biased constraint features such as easy to
setup, run, and maintain, that disqualify all other thinkable software
or set of software.

NB: I plan to out-perform solutions based on ElasticSearch such as
[commonsearch](https://github.com/commonsearch).

NB: Recently, on my side, Google search started to group results for
things such as StackOverflow, reddit, Quora and whatnots. Since a
couple of weeks, for some reason, Google started to try to present
more diverse set of results. Maybe they hope that it will bring back
the 1990 era of geocities, or the era before they killed feed readers,
eventually improving organically Google search, because Google
algorithms can not figure that almost anything about software outside
StackOverflow is subpar, and it particular it can not figure what is a
good page. Google wants to tackle the problem of centralization...

NB: At some point, searching for `simhash` was yielding three mirrors
of [wikipedia's page entitled
simhash](https://en.wikipedia.org/wiki/SimHash), those websites were
setup by black hats to capture ad clicks.

NB: I wrote down the above story to be able to drop: Google quacks!

## Why will I succeed where others have failed?

TL;DR: Maybe I will fail. Maybe I will succeed, I worked a lot for
that, and made choices.

First, there is always a chance or evil luck that I will fail.

Outside the very top notch high world-class level of self-esteem ego I
have, there are several source of confidence:

- Babelia is not a privateer search engine;
- Babelia does not aim to be a global search engine;
- I did my best to eliminate all source of known unknowns.

Babelia seek to eliminate the need for Google, and down the road even
deliver better tooling that any wanna-be unicorn... Babelia does not
play by the same rules. Babelia will not consider that the user is
stupid. Babelia is FLOSS, that alone will be enough to get rid of
Google. It will also be part of the fediverse. And further in the
future the basis of a fully decentralized Internet at the application
level

NB: By the way, I believe Google's search engine is already built
around the idea of a federation, except it happens in a controled
environment. So, what Babelia will achieve is more difficult that what
Google try to do (and arguably sometime succeed).

NB: I do not know why Cliqz failed or even Qwant did not succeed. I
may find out.

## Really, why a search engine?

TL;DR: Star-system is the limit, Facebook and GitHub are next.

The search engine is gathering place, like a library. I like to think
Google is the modern incarnation of the Library of Alexandria. There
is also Wikimedia projects. I mean, having loads of books without a
way to find out the book you are interested in is not useful to have.

In my opinion, a search engine is a fundamental piece in a knowledge
construction.

What about wikipedia, wikidata or other wiki stuff, or Facebook, or
even GitHub? Those things are more social than a search engine: a
registry, a filling cabinet can be automated, whereas decyphering
mushrooms caps, and categorizing into species, as of yet, can not be
automated so much.

Another fundamental piece in knowledge construction is communication.

To improve upon the establishment, and established practices, my goal
is to mimick the world wide web distribution model (easy updates, and
the long gone view-source), and getting inspiration from GNU/Linux
distributions (network of trust), with the far-reaching perfection
and/or minimalism dedication of projects such as suckless, netbsd,
or... R7RS.

The idea is to build a desktop environment that stems around a
decentralized (publicly distributed) code space where you can stream
updates from a network of friends. No, Bill Gates is not your friend.

Yes, the basis of the desktop environment will be a networked
programming language. It will not be networked in the sense of
Erlang.

Unlike anthropocene desktop environment, it will not try to hide
programming from you.  It should be painless to share your tweaks,
scripts or programs into the public network.  The best and still
wanna-be feature is easier internationalization (i18n) of code.
Footnote: Clickports will be available.

Code is a meme. Where you can share codes, you can share memes.  The
inverse is not always true. I experimented with a peer-to-peer social
network with [qadom](https://github.com/amirouche/qadom). While, it is
incomplete, it allowed me to figure that it is not impossible, there
might be hidden corners, tho.

To summarize: Other aspects of the Internet are more social than a
search engine. To deliver the features that can compete with Facebook,
GitHub while sticking to demonstrated good pratices such as network of
trust, the way forward is to build a desktop environement that is
built around a programming language that embody, in world made of
diversity, the social nature of software making. Being able to share
code as easily as sharing cat memes, and being able to download those
memes, after a review, and possibly some tweaks, install them in your
own desktop is: the next big thing.

## Roadmap

Back to the more prosaic roadmap toward the release of Babelia 1.0:

- Milestone 1, Graphical User Interface: The first goal is to build
  the user interface. For regular users, the mighty input box will be
  featured with search results (called hits), along a search pad...
  The operator will be presented how to populate the knowledge base,
  how to control the crawler, along a dashboard to display health, and
  sort out moderation requests.

- Milestone 2, Boolean-Keyword Search Engine: The second step is to
  build the basis of the backend that can achieve boolean-keyword
  search with exact-match, and negated keywords, without the support
  of the operator `OR`. Also, I will create a program to convert
  `.zim` files from [kiwix.org](https://kiwix.org) into a SQLite LSM
  database, add the ability to populate the database with files using
  the Web ARChive format nicknamed `.warc`. At which point, it will
  make sense to package Babelia in NixOS.

- Milestone 3, Knowledge Base: in that step the goal is to create the
  backend that will allow to create the knowledge base that gathers
  information about known entities and their relatedness. At this
  point it will be possible to display recognized entities on result
  page. The main goal being the added possibility to travel to the
  right of the semantic continuum through hops in relations between known
  entities and keywords from the query.

- Milestone 4, Crawler: The point of this milestone is to build a
  crawler (also known as spider). Unlike a privateer spider, it does
  not aim to be very fast.  One of the main goal of Babelia is to be
  one stop solution for your search need. Hence, the main feature of
  the crawler is to be well integrated with the rest of search
  engine. It will be possible to subscribe to RSS, and ATOM
  feeds. Also, it will be handy, to also support firefox bookmarks. It
  will be possible to ignore URLs with glob patterns. Also, the number
  of hops outside seed domains will also be configureable to help
  escape the gilded cage.

- Milestone 5, Moderation and Dashboard: Here the goal is to allow the
  operator of a Babelia instance curate domains with the ability to
  delete indexed documents, or even purge a domain that were flagged
  by an user.

## Architecture

A few notes about the design of the whole thing:

- Milestone 1, the graphical user interface will be built with [Gambit
  Scheme](https://github.com/gambit/gambit/) JavaScript backend,
  [preact](https://preactjs.com/), and
  [okvslite](https://github.com/scheme-live/live/tree/okvslite-and-co/live/okvslite/#status).
  I will to try to use Gambit with Termite to help with concurrency.

- Milestone 2, Boolean-Keyword Search Engine: The inverted index will
  associate words to documents after they are transliterated to ascii.
  At query time, keywords in the query will be also transliterated to
  ascii, the least common token will serve as the seed to select the
  smallest set of documents that contains all the results, those are
  called candidates. At which point, a non-distributed map-reduce will
  score document against the query, whie Aho-Corascik is streaming the
  words from cached candidate documents. Map-reduce will keep top N
  results, where N might be configurable.

- Milestone 3, Knowledge Base: that will be a port of copernic,
  `vnstore2` will be built on top of the new extension I invented
  called
  [`nstore2`](https://github.com/scheme-live/live/tree/okvslite-and-co/live/okvslite/nstore2#readme). The
  advantage of `vnstore2` over `nstore2` is that it allows to track
  changes, and the added benefit of being able to rollback. At query
  time depending on the number of bangs `!`, the search engine will
  follow links between keywords and their related entities, to travel
  in the semantic continuum possibly yield more interesting results,
  it might also increase false positives. `vnstore2` will also be
  useful to add summaries or descriptions to known entities, that
  could be linked to their official page or wikipedia page.

- Milestone 4, Crawler: Unclear as of yet.

- Milestone 5, Dashboard: It is a Create-Read-Update-Delete graphical
  interface, the backend code looks boring...

You might ask: I am not a coder, what is in there for me? In that case
re-read the above, and [send me an email with a precise description of
what the above is missing](mailto:amirouche@hyper.dev).

NB: I plan to deliver before rustaceans start to consider coding
software that are not command-line helpers.
