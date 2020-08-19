# 2020/08/19 - fauxtexte

fauxtexte is a fake text generator based on markov chains.

## Getting started

```
# fauxtexte
Usage:

  learn INPUT OUTPUT
  generate INPUT [SOME FUN ...]
```

- `fauxtexte learn INPUT OUTPUT` will learn the vocabulary. `INPUT` is
  supposed to be a texte file with a single phrase per line. `OUTPUT`
  will be the name of the generated model.  You can call multiple time
  `learn` with different `INPUT` but the same `OUTPUT`.
  
- `fauxtexte generate INPUT [SOME FUN ...]` will generate a single
  sentence using the `OUTPUT` of the above command.  That is `INPUT`
  in this command is the name you passed as `OUTPUT` in the above!
  
Here is an example run:

```
# ./fauxtexte learn data/scheme-2020-04.txt model.fauxtexte
done!
# ./fauxtexte generate model.fauxtexte "% scheme is"
% scheme is
# ./fauxtexte generate model.fauxtexte % scheme is
% scheme is pascal and pascal is fortran
# ./fauxtexte generate model.fauxtexte % scheme is
% scheme is fascinating
# ./fauxtexte generate model.fauxtexte % scheme is
% scheme is appropriate in your redefinitions
```

The `%` in the `fauxtexte generate` command will instruct the program
to try to start, otherwise it can pick any word it learned from
anywhere in a sentence.

## ChangeLog

- 2020/08: v0.0.0 - initial release 

  - [alpine binary](/bin/fauxtexte/alpine/0.0.0/fauxtexte)
  - [ubuntu / debian](/bin/fauxtexte/debian/buster/0.0.0/fauxtexte)
