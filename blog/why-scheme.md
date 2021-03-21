# 2021/01/31 - Why I still Scheme (and you should too!)

That is a reply to the following post on medium:

> [Why I still Lisp (and you should too!) As a long-time user (and
active proponent) of Scheme/Common Lisp/Racket, I sometimes get asked
why Istick with them. Fortunately, I have always headed up my own
engineering orgs, so I have never had to justify it to "management",
but there's the even more important constituency of my own engineering
colleagues who have never ever had the pleasure of using these
languages.](https://mendhekar.medium.com/why-i-still-lisp-and-you-should-too-18a2ae36bd8)

I like the punchline of the post:

> An s-expression based, dynamically typed, mostly functional,
> call-by-value λ-calculus based language

I fully agree with that quote. I disagree with the use of medium, and
they are few facts that are not accurate.

## λ-calculus based language.

First, like some else noted in the comments, the JVM (will) support TCO and
call/cc with the loom project.

Second, the biggest advantage of λ-calculus is that everything can be
explained in terms of λ-calculus. I am not familiar with λ-calculus,
what I understand is that one can explain every single form of Scheme
with a transformation of the code into some `lambda`. A `lambda` is
some kind of anonymous function, it looks more like ES5 function but
with explicit rest arguments. That is true for every Scheme forms
except `if` and `set!`. Why should you care?  Because the immediate
consequence is that it is very easy to explain how the programming
language works. In fact, you only need to know about `lambda`, `if`
and `set!`. The latter allows to change what a variable is holding (≠
from mutating a data structure).

I am not sure λ-calculus helps to "play back the code" that is more
like an argument of side-effect free functions.

The consequence that everything with scheme can be expressed with
lambda is that it is much more clear how variable scoping works
(unlike python scoping).

I fully agree with that:

> As you might have noticed, I'm not using the word functional
> language to describe Scheme. That's because while it is primarily
> functional, it does not skew all the way to non-mutability. As much
> as it discourages its use, Scheme recognizes that there are genuine
> contexts where there may be a use for mutations and it permits it
> without the artifice of auxiliary devices.

But that is not feature of λ-calculus but really a choice during the
design of Scheme.

### Call-by-value

I am not familiar with the "call-by-value". Reading through that
section of the blog post the alternative is lazy evaluation with
Haskell. With Scheme, lazy evaluation is opt-in as explained in the
last paragraph of that section.

### Mostly functional

> Functional programming is great. Playing back functional code in
> your head is simple; the code is easy to read and the lack of
> mutations reassuring. Except when it isn't enough.

To be precise, the lack of mutations is reassuring, except when it isn't
enough, Scheme allows mutations.

### Dynamically Typed

The world today is going on and on about typed languages.

There is something that is not precise: The world today is going on and on
about statically typed languages. The key word is "statically". Scheme is
typed. A lot of people boo dynamically languages with the argument Python or
Scheme are untyped: wrong. Also, people "dynamic" other stuff e.g.
introspection... Or "dynamic is slow" more on that below.

I may or may not disagree with the line "static type checker are
bullshit, because they do not prevent anything more than obvious
bugs". Again it is not accurate to spread the idea that the "compiler"
or "static typing" possibly help avoid even minor bugs, because a) it
is not necessarily a compiler (mypy anyone?) and also because static
typing as in "required written types near some variables" is not what
mypy or even rust compiler use to find some problems. What is
significant is type information. And that can come from static typing
with the help of Hindley-Milner algorithm or some other tool and
heuristics.

I agree with the arguments on invariant, that leads to a better take
on a priori checks of programs or even runtime checks: assert. That is
the best of all worlds, you can get type information and also check
invariant using predicates (predicates that may be registered in the
tool doing the checks or possibly inferred with partial evaluation).

The author goes the route of "no tool to check my code", I prefer the
tool to be opt-in like assert.

> What improves (and somewhat guarantees) software quality is rigorous
> **meticulous* testing.

The absence of proof is not the proof of the absence.

Another mistake: type or constraint or contract information does not
necessarily translate into fast code!

### S-expression based

> The biggest advantage of this form of syntax is a form of minimalism

I prefer "powerful minimalism" because it allows to create a macro
system very easily.

Macros also exist in programming languages that are not based on lispy
s-expression.

The examples of good use of macros are wrong.

### Conclusion

Comes the paragraph on performance, it is prolly about CPU performance:

> And lastly, there's the issue of performance. First, let's put the
> common misconception to rest: Lisp is not an interpreted
> language. It is not slow, and all implementations come with lots and
> lots of levers to tweak performance for most programs. In some cases
> the programs might need assistance from faster languages like C and
> C++ because they are closer to the hardware, but with faster
> hardware, even that difference is becoming irrelevant. These
> languages are perfectly fine choices for production quality code,
> and probably more stable than most other choices out there due to
> decades of work that has gone into them.

Performance is not an issue (not anymore, and certainly not compared
to JavaScript, Python or Ruby) especially the biggest LISP
implementations (SBCL, CCL, Chez Scheme, or Gambit).

> implementations come with lots and lots of levers to tweak performance

That is not the case of Chez Scheme, and it is still very fast
compared to Python or Java or even C.

> I do recognize, learning Scheme/Lisp/Racket is a wee bit harder than
> learning Python (but a lot easier than learning Java/JavaScript).

That is completely false. The number of things you need to ignore in
Python when getting started with programming out number the total
count of concepts that expert Scheme engineer need to know to be
considered expert. The only problem with Scheme, in particular Chez
Scheme is merely the absence of battle tested libraries for everyday
use like HTTP, image processing or browser automation and very
specific but mainstream libraries.

> the beauty of these languages

Beauty is neat. Good tool for the job is better...
