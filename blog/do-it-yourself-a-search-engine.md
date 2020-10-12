# 2020/10/12 - Do It Yourself: A Search Engine

## Prelude

I read more often than ever that people are looking for ways to build
their own search engines.

Even if more on more "advanced" features are integrated into search
engines.  They are mostly based on human grunt work.  Semantic search
engine, whatever "semantic" does mean for you, is in fact merely a
couple, not more than a dozen, set of tricks.  I like to say, much of
Google's search engine is good old human labor.  If you still doubt
it, here is again: Google results are not only biased, also they are
editorialized.  Whether algorithms, and their bugs, party is
irrelevant.

My point is: it is human made.  Not some necessarly advanced alien
tool.

The only thing preventing you to have your own search engine is there
is no readily available software, why? because there is no cheap
hardware.

This might sound like a crazy idea five or ten years ago, but with the
advent of AMD threadripper ie. [cost gravity at
play](http://cultureandempire.com/html/cande.html) getting together a
personal search engine is, if not a necessity, at least a possibility.

The most common complain I read about Google is that it yields
irrelevant text "that do no even contain my search terms". That is not
a bug, that is a feature!  It seems to me the subtext is that you can
not easily customize Google or whatever search algorithm since it is
privative.  Even retrieving Google search results for further
processing if not forbidden, is at least difficult.

## Getting started

Let's start with the beginning: what is a search engine? A search
engine is software that will **crawl** the Internet, **index**
ie. store the text in a particular format, and that users can
**query** and receive in return the most relevant text.

Let's dive into what "relevant text" means. What is relevant text?

1. A text that contains the search term in my query
2. A text that has the same topic as my query
3. A text that gives an answer to my query

The good answer is "it depends".  That's why queries have grown from
keywords match like a book index, to boolean queries e.g. `"Apple"
-bible`, until so called semantic search, which boils down to consider
one-way or two-way synonyms and other lexical features.

So far, I failed to build a crawler that works.  Also much of the text
I am looking for is in wikipedia or StackOverflow for which they are
flat releases which are much more easy to get started than putting
together your own crawler.  Still, they are some crawler around, so
you can use that or learn from it.  I will not dive into the crawler
part because it still hurts when I think about `robots.txt`,
throttling, text encoding etc... booooh!

So, we will imagine that you have a dataset of plain text, for
instance wikipedia vital articles.  It helps if you know the content
of the dataset.  Querying random news article is not very easy to
grasp because you have to read (!) the text to figure when and how
they are relevant.

Before querying, you need to store the text, but to know **how** to
store the text you need to know which query feature you want. To get
started I will only consider positive keywords and negative keywords
like `apple -bible`. So, we need to figure which find out which text
contains the word `apple` but not the word `bible`. Looking up
everything that does not contain `bible` is difficult, you would need
to **scan** the whole database to what are those document. Instead we
will look for documents that contains the word `apple`.  So the
following document contains the word we are looking for:

```scheme
(define doc1 "apple is looking for a search engine.")
```

That is the moment where the most advanced technology of our current
century makes it appearance: the inverted index.  **What is an inverted
index? It reverses the relationship between the document and the word**.
Instead of saying "this document contains the word apple" it says
"apple is contained in this document".  So we might have a procedure
that returns the document identifier that contains `apple`, like:

```scheme
(assert (contains? (inverted-index-lookup "apple") 1))
```
`inverted-index-lookup` returns a list, and that list contains the identifier `1`
of the first document.  That list might be big. So **you want to consider the least common word from the query**. I call that step
*candidates selection*.  Also, you might want to convert the positive terms
into lemmas or stems to go toward semantic search, which will mean you need
to store lemmas or stems at index time.

Anyway, the next step, given the list of documents that contain the
least common word or term or lemma or stem, is to **filter and score**
according to the full query. In the above case, that is remove the
documents that contains `bible`.  You can do that step serially, and
it will necessarly take time.  The trick is to use `for-each-par-map`.
That is a cousin of map-reduce that execute the map procedure in
parallel.

For instance something like:

```scheme
(let ((hits '()))
  (for-each-par-map
    (lambda (uid score) (when score (set! hits (take 10 (sort (cons (cons uid score) hits))))))
    score (inverted-index-lookup "apple"))
  hits)
```

The score function is interesting. I think going the
[aho-corasick](https://github.com/abusix/ahocorapy) with a
[FSM](https://medium.com/analytics-vidhya/converting-boolean-logic-decision-trees-to-finite-state-machines-180ad195abf2)
is the best route because it is easy to implement proximity scoring,
"phrase matching", or really anything I can think of.

> ⚠ That last paragraph is really the most important part of this
> post.

## Conclusion

There is a gigantic leap that is going to happen in search because of
hardware availability, and free software with readable source ie. the
only thing that makes human progress possible: knowledge sharing.

## Malfunction! Need input!

- https://en.wikipedia.org/wiki/Tf%E2%80%93idf
- https://en.wikipedia.org/wiki/Precision_and_recall
- https://hal.archives-ouvertes.fr/hal-01730479/document
- https://wiki.nikitavoloboev.xyz/web/search-engines
- https://github.com/amirouche/babelia
