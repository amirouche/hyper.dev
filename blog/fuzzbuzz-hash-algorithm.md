# 2019/11/12 - FuzzBuzz Hash Algorithm

fuzzbuzz hash is a [Locality-sensitive
hashing](https://en.wikipedia.org/wiki/Locality-sensitive_hashing)
algorithm that has the following properties:

- The length of the longest common prefix of two bit strings is
  smaller that the length of the longest common prefix of their
  fuzzbuzz hash.

- The smaller the [Hamming
  distance](https://en.wikipedia.org/wiki/Hamming_distance) between
  two bit strings, the bigger the longest common prefix of their
  fuzzbuzz hash.

The algorithm rely on a Merkel-tree that use a bitwise `OR` as a hash
function and then serialize the tree using a top-down depth-first
traversal algorithm.

For instance, let's pick `1001 0001` bit string. We can construct the
following Merkel tree:

```
       __  1  __
      /         \
     /           \
     1            1
   /   \        /   \
  1     1      0     1
 / \   / \    / \   / \
[1][0][0][1] [0][0][0][1]
```

Then we can serialize it the tree without the leafs, using top-down
depth-first traversal.

Here is the same tree, with the index of each bit between parens:

```
       __ 1(0)__
      /         \
     /           \
     1 (1)        1 (4)
   /   \        /   \
  1 (2) 1 (3)  0 (5) 1 (6)
 / \   / \    / \   / \
[1][0][0][1] [0][0][0][1]
```

That result is the following bitstring: `111 1101`

At last, we suffix that bitstring with the original bitstring:

```
11 1110 1001 0001
```

More experiments in [fuzzbuzz
repository](https://github.com/amirouche/fuzzbuzz/blob/master/fuzz.py#L126).
