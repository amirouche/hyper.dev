# 2020/01/22 - Scheme fatigue

Scheme fatigue has two sides.  In the following I try the describe my
views about Scheme programming language and also poke at a few other
topics.

It might not be very well structured.

## Fragmentation

As far as I can tell, Scheme as a programming language is easy to the
mind, there is a limited set of features (albeit sometime powerful
ones) to grasp before being productive.  Scheme is easy to maintain in
the sense that when you come back to a piece of code (that is tested)
months after you last checked it, it is possible to make sense of it,
but also easy to rework or improve it.  At least, Chez Scheme has
profiling, a step debugger, with correct source file informations and
is efficient. Did I mention it was fast?

Scheme has a healthy ecosystem of computer scientist, coders,
standards and implementations.

Many say, there is too many implementations, and that it is bad luck
for the programming language as a whole.  I would add that there is
many **maintained** implementations.  I disagree with the fact that it
is bad luck.  Scheme programming language describes a Turing-complete
programming language that is easy, fun, documented, and grateful to
implement in an interpreter or a compiler.  That offers a clear and
well documented path from apprentice to master.

Too much choice, kills choice you might say; one side of the coin of
the Scheme world: which Scheme implementation should I choose?

The official answer is that you should choose: none.  It makes sense
versus [vendor lock-in](https://en.wikipedia.org/wiki/Vendor_lock-in).
The [Scheme Reports](http://www.scheme-reports.org/) steering
committee agreed on the fact that Scheme code ought to be be portable
across implementations:

> The purpose of this work is to facilitate sharing of Scheme
> code. One goal is to be able to reuse code written in one conforming
> implementation in another conforming implementation with as little
> change as possible. Another goal is for users of this work to be
> able to understand each other's code based on a shared and
> unambiguous interpretation of its meaning.
>
> [Charter for [R7RS] working group
> 2](http://scheme-reports.org/2010/working-group-2-charter.html)

Based on experiences, both [R6RS](http://r6rs.org/) and
[R7RS](http://r7rs.org/) provide a way to create portable code.  It is
already possible to write portable code across Scheme implementations.
The situation can only improve.

The standards help describe a path for portability, is a shared space
to exchange ideas, good practices, innovations, and nurture
[emulation](https://en.wiktionary.org/wiki/emulation#Noun).

Maybe they were [some
disagreements](https://weinholt.se/articles/r7rs-vs-r6rs/) about
wording, philosophy and how big or small it ought to be.  That is
somewhat political.  At the end of the day, each Scheme implementation
retains its defining characteristics.  That is helpful because it
allows the split (or share) the work to explore new ideas and
re-explore old ideas.  It is also in the interest of commercial
efforts because it avoids vendor lock-in.

**Fragmentation is good**.


## Do It Yourself

The other side of the Scheme coin is the "Do It Yourself" philosophy.

It stems among other things from the fact that [it used to be mostly a
teaching material](http://lambda-the-ultimate.org/node/3312).

There is the idea that minimalism equals small. On this topic I like
to quote:

> Programming languages should be designed not by piling feature on
> top of feature, but by removing the weaknesses and restrictions that
> make additional features appear necessary.

One might say that R5RS amd R7RS-small are good enough and that
schemes' efforts should be focused on improving and refining the ideas
of small but powerful minimalism.  The above quote goes to the point,
minimalism is defined as the result of the work of taking away
spurious features.  If, to get started you have an empty set, there is
nothing to remove, then there can be no notion of minimalism.  I
entertain the idea that, in this regard, R6RS and the larger R7RS will
allow to create a set of common idioms upon which Scheme will continue
its true minimalism seeking adventure.  Prolly, R7RS will not be the
end of minimalism, an ideal.  Maybe there will be things to take away
from it, but as of yet, since it is not finished and because there is
still room for experiments one can not definitly rule that R7RS-large
is not Scheme spirit.  For instance, I think, Scheme object type
called `port` are misleading, do not promote good programming
practices, clutter the specification and the implementations.  I made
recently the discovery that one can rely on procedures to mimic the
behavior of ports in backward compatible way while re-using existing
code and idioms.  That is, even in R5RS, there is, according to me,
things to take away.  Without R7RS generators and accumulators, I
would not be able to think that ports are a spurious abstraction
coming from the past, haunting new students and seasoned engineers
alike.  The idea behind generators is well understood and
self-contained to the extent that it does not break the small language
kind-of idea and keeps around the DIY philosophy that is strong within
the Scheme community.

There is the widespread meme named the [Lisp
Curse](http://winestockwebdesign.com/Essays/Lisp_Curse.html) along the
lines of:

> Problems that yields technical issues in other programming
> languages; with Scheme programming language, they yield social
> issues.

In particular, I quote the following:

> Every project has friction between members, disagreements, conflicts
> over style and philosophy. **These social problems are counter-acted
> by the fact that no large project can be accomplished otherwise.**
> “We must all hang together, or we will all hang separately.” But the
> expressiveness of Lisp makes this countervailing force much weaker;
> one can always start one's own project. Thus, individual hackers
> decide that the trouble isn't worth it. So they either quit the
> project, or don't join the project to begin with. This is the Lisp
> Curse.

That means, that there is no problem to write the code solving any
problem, the issue is to **agree on the [Good
Thing](https://en.wikipedia.org/wiki/Worse_is_better)**. In fact, we
do not **need** to agree on everything.  That is the point of Scheme.

The Lisp Curse essay, try to explain that it is way too easy to do a
fork.  I argue that we should let it be so.  **I argue we should make
it easier to fork**.  Meanwhile we should *individually* strive for
better softwares.  Better software should include rationales, tests,
documentations.  And credits to be able to understand the lineage of
the idea, and question whether the premise that lead to a given
solution do still make sense.  And, only later, maybe at some point,
some guarantees like backward compatibility, deprecation policy,
upgrade path and long time-support story.  To put emulation,
innovation and ideas melting at the forefront of humans goals.

I put long-time support at the end because the Good Thing is to be
able to handle things on your own.  Do it yourself.  That is the most
important idea that underlies the free and open source movement.  That
is what made the hop from pre-millenium based on cisor, paper and
fossil fuel to current century possible.

"Lisp Curse" inflict upon the idea that lisp will never bring back the
good old days that are before the AI-winter.  Time traveling is not
possible, or [maybe there
is](https://github.com/amirouche/arew-scheme/blob/d5648fbc021997e452b89a251900fc40b39ea0a6/vnstore.scm#L684),
but that does not matter.  The thing that matters is lisps have
overcome their past daemons related to performance and efficiency.
Actually, people (like me) have reported that their Common Lisp or
Scheme code to be faster than the C or C++ equivalent.  Also, lisp, in
particular Scheme has improved the maintainability of Scheme e.g.  the
advent of [hygenic
macros](https://en.wikipedia.org/wiki/Hygienic_macro), make the code
much more readable, and more future proof.  It is a complex, maybe
complicated idiom, but a powerful one.

A consequence of the AI-winter is that lisps have, to some extent,
lost mainstream momentum.  Yeah, there was winter, but now it is
spring.

People cooperate toward a common goal, in distributed, non-coordinated
way, even in evil environments with non-trusted peers most of the
time, if not, all the time e.g. human race survival.  That is, the
[bazaar](https://en.wikipedia.org/wiki/The_Cathedral_and_the_Bazaar)
is the Real Thing.  Tho, I don't want to down play the role of the
cathedral: the bazaar is made of many cathedrals, some times one-man
lone-wolf hacker endeavors, some times the craft feat of many
dedicated engineers.

I want to stress the fact that Scheme needs to further [embrace,
extend and
encourage](https://en.wikipedia.org/wiki/Embrace,_extend,_and_extinguish)
more the distributed non-coordinated cooperation model.

It is a fact that on the topic of cooperation, schemers are not at
rest.  There is the [Scheme Request For
Implementations](https://srfi.schemers.org/) and
[RnRS](https://en.wikipedia.org/wiki/History_of_the_Scheme_programming_language#Standardization)
standards.  More familiar to pythonistas and javascripters, more in
the spirit of the bazaar, there is [so many scheme package
managers](https://weinholt.se/articles/so-many-scheme-package-managers/).

At this point, I think we agree that the lisp curse is not that bad,
being able to fork is healthy!  In many ways, Scheme and Common Lisp
projects by themselfs contradict the idea that it is not possible to
build and sustain long and multi party efforts toward the goal of
building Earth scale software systems.  I will not cite more specific
details or particular commerical or wanna-be whole world changing
distribution because what Scheme programming language implementations
have achieved, are, in my opinion, valuable enough in a scope that is
larger than the programming community itself.

**Do-It-Yourself is good**.

## Conclusion

To be honest, I started the note to try to explain, first to myself,
why I will work on a Scheme implementation that takes more inspiration
from Python and JavaScript (but still a scheme lisp :P).  There is
already ALOT of package managers, schemes et al.  The steering
committee would like to see more portable Scheme code.  I am a tiny
little spark.  I think there is definitly space for another Scheme,
especially such as it rely on an existing compiler.  DIY philosophy,
fighting maintream ideas like "that is NIH and wheel re-invention" and
to some extent "good enough" and boredom has shaped the human,
minimalism and truth seeking aventurer and bytes wrangler that I am.
I feel much more confortable with coding even if I forgot most of
computer science theory.  That does not mean it is useless.  I learned
some other ((more) practical) ideas e.g. immutability,
Continuation-Passing-Style and trampolines that I already put to good
use.

I need to decide what to do of my free time.

My hearth is happy with the idea of a peer-to-peer collaboration
system that would make it possible to fork at the function level.
Taking inspiration from [radicle.xyz](https://radicle.xyz/) and
[unison](https://www.unisonweb.org/) and why not ethereum.  It would
also make it possible to translate definitions into your favorite
natural language.  No more english-only programmable programming
systems.  It looks like a gigantic hop, but awesome one.
