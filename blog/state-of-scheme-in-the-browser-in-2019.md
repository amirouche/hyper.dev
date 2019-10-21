# 2019/10/04 - State of Scheme in the Browser

I made some progress around my experiences in the browser, this lead
me to write a Scheme-to-JavaScript compiler that is incomplete but can
do some stuff.

## Chicken

I still did not try Chicken's Spock egg.

ref: http://wiki.call-cc.org/eggref/4/spock

## BiwaScheme

This is an interpreter written in JavaScript that doesn't support
tail-call optimization.

- demo: https://hyperdev.fr/defunct-forward.scm/
- repo: https://github.com/amirouche/defunct-forward.scm

## Gambit JavaScript backend

It is still a work in progress. ~~It prolly support tail-call
optimization but requires some work. With the build I tested,
tail-call factorial gives an error.~~

edit: It works well actually. The problem was on my side.

- demo: https://scheme-live.github.io/scheme-fuss/
- repo: https://github.com/scheme-live/scheme-fuss

## Schism

This is the most promising stuff. It is a self-hosted
Scheme-to-WebAssembly (wasm) compiler. The two things that are missing
are some kind of call/cc support and I don't know how to yield the
control back to JavaScript.

- repo: https://github.com/google/schism/

## Chibi Scheme WebAssembly build

It works most of the time on Firefox but it (used to) crash on Windows
Chrome.

- repo: https://github.com/scheme-live/ff.scm
- demo: https://scheme-live.github.io/ff.scm/

## Ruse Scheme

This is my work-in-progress compiler that targets JavaScript and not
WebAssembly (yet).

- repo: https://github.com/scheme-live/ruse-scheme/
- demo: https://scheme-live.github.io/ruse-scheme/demo/counter/
