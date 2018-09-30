# 2018/09/29 - One Step Closer To The Moon

It's long time I did not do a meta post to give a gimpse of where I am
at and where I am going.

As you might have guessed, I started a new project called
`socialiter`.

Let's proceed step by step.

## Scheme vs Python

I confident Scheme is the future of computing. I mean it's doomed to
replace the primary dynamic language out there namely Python. Why?
Because of its minimalistic powerful primitives and clean design,
because of its impressive performances and its roots in science. All
of that push scheme programming language everyday one step
forward. One thing that is missing in Scheme ecosystem is ready-made
solutions for your problem *ahem* I mean what you think is a solution
to problem you think you have. Let's not be dishonest. I am sorry, but
Scheme community is missing a lot of documentation for the mass. That
is not everybody is willing to dive into black and white papers
(source of actual knowledge) to learn how to use a web
framework. Again, sorry to say but Scheme is not sexy. I think Scheme
community needs to compromise and try to attract more
developpers. Racket (which is not a Scheme *anymore* but still has the
best documentation of all the time) is already doing that. I mean that
Scheme community must keep seeking the thruth and deliver actual
knowledge through papers, books **and** it must also deliver
half-backed articles with nice gifs, emojis and sillicon valley
friendly colors "au gout du jour". That is (still?)  the hard reality
of nowdays computing.

Because scheme is not fashionable and a lot of people are stupid, I
decided to pursue my immediate dream(s) in Python. Actually, it is a
bet I am doing with myself. I bet that I can get enough perks from
that project to be able, in the future, to invest more time with
Scheme.

## neon also known as zehefyu93600, wiredtiger and FoundationDB

Neon is a project I started this year. The goal was to experiment with
RDF-like database somewhat like datomic but mixed with git.  That is a
versioned branch-able triple store.  The idea is very nice and again I
think it has a place in the future. If `socialiter` is a moon
shot. [zehefyu93600](https://github.com/amirouche/zehefyu93/) is a
Andromeda shot.

I will not give up on wiredtiger. I still think it's an awesome
abstraction. It is not because I invested a lot time in it, that I
keep the idea around but because Apple open-sourced
[FoundationDB](http://foundationdb.org/). FDB is the same abstraction
with the same guarantees but distributed. You might be wondering why I
will need a distributed database?! Well, outside again perks I can get
from learning how to use it. It can come handy to operate a big-ish
search engine because it's easier to scale, I believe.  It is not
black or white. Even if wiredtiger is easier to operate on a single
machine. I still don't have a precise idea how I will handle in terms
of code the fact that wiredtiger API is blocking. Whereas FDB can be
asynchronous.

## ForwardJS and BeyondJS

When I started `socialiter` I ported the state management routine I
created in Scheme to JavaScript and started playing with that.  I
fixed a few bugs and a race condition. It worked well on experiments.

At the end of the day, even if JavaScript made tremendous progress
it's still not up to the mark compared to Python, especially Python
3.5+.

Also, let's be honest, with shitty VueJS but overhelming marketing and
the zillions of other frameworks in JavaScript, it is very hard to
market a framework that is somewhat inspired from elm and ported from
Scheme.  Few people will take the time to read the code and as far as
I know nobody has tried. In terms of professional carreer, I keep some
JavaScript-fu under the pillow, but apparently it's not where my
strength is. Also, I don't enjoy coding in JavaScript that much.

Last but not least, as far as I am concerned I don't think browser
technologies has a place in the future that I am thinking about.

## civkit

You might have read my rambling about
[bootstrappable](http://bootstrappable.org/) ideas. Basically, I don't
think one can make it to Andromeda with your favorite web
browser. This is technically non sens to plan a journey of several
decade with so much clutter in the tech stack.

While the idea to build a legacy-less maintanable software to help
people create colonies on other planets is noble goal. It's also a
crazy idea. That's why, I prefer to aim for a more reasonable goal
that is `socialiter`.

## Conclusion

So, here I am with new goals, [almost new code base with almost all my
favorite tools](https://github.com/amirouche/socialite/) into a
journey that will hopefully last... Until next time.
