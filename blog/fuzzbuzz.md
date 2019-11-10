# 2019/11/10 - DIY approximate string matching (fuzzbuzz)

The idea of fuzzbuzz is to do fuzzy search in textual data otherwise
said, approximate string matching. This is based on the
[simhash](https://github.com/amirouche/fuzzbuzz/raw/master/doc/simhash-2007.pdf).
Which can be summarized as follow:

```python
def features(string):
    """Return a bag of grams of the given STRING."""
    tokens = ['$' + token + '$' for token in string.split()]
    out = Counter()
    for token in tokens:
        iterator = chain(*[ngram(token, n) for n in range(2, len('$CONCEPT$'))])
        for gram in iterator:
            out[hash(gram)] += 1
    return out


def simhash(string):
    """Compute a similary hash called simhash"""
    input = features(string)
    intermediate = [0] * HASH_SIZE
    for feature, count in input.items():
        for index, bit in enumerate(int2bits(feature)):
            intermediate[index] += count if bit == '1' else -count
    # compute simhash
    simhash = ''.join(['1' if v > 0 else '0' for v in intermediate])
    simhash = int(simhash, 2)
    return simhash
```

The astute reader will recognize that `simhash` returns a positive
integer based on a bag-of-grams where grams are slices of words
between 2 and 7 magic.

The idea is that simhash will capture similarity that exist in
small-ish strings:

```python
In [1]: import fuzzbuzz

In [2]: fuzzbuzz.hamming2(fuzzbuzz.simhash('obama'), fuzzbuzz.simhash('barack obama'))
Out[2]: 16

In [3]: fuzzbuzz.hamming2(fuzzbuzz.simhash('obama'), fuzzbuzz.simhash('trump'))
Out[3]: 30

In [4]: fuzzbuzz.hamming2(fuzzbuzz.simhash('concept'), fuzzbuzz.simhash('concpet'))
Out[4]: 22

In [5]: fuzzbuzz.hamming2(fuzzbuzz.simhash('concept'), fuzzbuzz.simhash('concept'))
Out[5]: 0

In [6]: fuzzbuzz.hamming2(fuzzbuzz.simhash('concept'), fuzzbuzz.simhash('concept car'))
Out[6]: 11

In [7]: fuzzbuzz.hamming2(fuzzbuzz.simhash('concept'), fuzzbuzz.simhash('quality'))
Out[7]: 30

In [8]: fuzzbuzz.hamming2(fuzzbuzz.simhash('quality assurance'), fuzzbuzz.simhash('quality'))
Out[8]: 17
```

That is it gives a clue of how similar two strings are. That said, it
requires to compute the [Hamming
distance](https://en.wikipedia.org/wiki/Hamming_distance) of the
simhash.

Given a giant set of documents and a new document, figuring which
document is the most similar requires to compute the simhash before
hand at index time, and then at query time, it requires to compare the
simhash of the new input document with the simhash of ALL the known
documents the complexity is at least O(n).

In fuzzbuzz, `HASH_SIZE` is not documented magic, but was chosen to be
two times bigger than the count of known documents: 2^32 = 4 294
967 296. That is around 4/2 billions documents. That is around 2
billions * 32 / 8 = 8 000 000 bytes otherwise 8GB of memory required
just to store the simhashes. That is way too much for my laptop with
12GB of RAM.

It is not possible to pre-compute (aka. index) the Hamming distance of
all possible input documents.

What about indexing, in an Ordered Key-Value store, the simhash
instead?

That turns out to be is possible.

Given a simhash of 8 bits, one can construct a merkel-tree with binary
`OR` operator as a hash function and serialize the resulting tree
using a depth-first search back to a bit string called `bbk`.

edit: the merkel-tree hash function is binary `OR`.

`bbk` will have the amazing property that the more
similar to two documents are, the longer the common prefix will be.

At query time, the remote distributed dictionary expert system must
compute the simhash of the new document, then the `bbk` hash and then
[search near](http://source.wiredtiger.com/2.3.1/cursor_ops.html) or
query using ranges of `bbk` prefixes of decreasing length.
