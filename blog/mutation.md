# 2021/01/31 - mutation: review & rework of mutmut

![](https://images.unsplash.com/photo-1596079320875-ff665fa4a5dc?ixlib=rb-1.2.1&q=85&fm=jpg&crop=entropy&cs=srgb&w=1024)

A coworker told me about mutation testing, I was immediately
interested because testing is interesting. Testing became even more
interesting when I read how FoundationDB was made. I recommend you
watch the video about testing with deterministic simulation.

I started looking into [mutmut](https://github.com/boxed/mutmut) and a fork
that adds parallel runs support... eventually I though: [how hard can it
be?](https://hackernoon.com/mutmut-a-python-mutation-testing-
system-9b9639356c78)

Yeah, you might think that is my thing, and that is the thing of many
(most?) developers starting on a new project: "the code is evil,
let's rewrite!". And that is somewhat the idea behind this series of
logs, so I will not say I am not into "rewrites" myself (more on that
later).

I went swiftly through all projects that pop'ed in google first page
result, and still was interested to rewrite. Let's dive deeper into
those projects.

Instead of an introduction to mutation testing, let our imagination
play with the following nice track from Disiz Peter Punk called
Mutation:

[Disiz Peter Punk Intro Mutation](https://www.youtube.com/watch?v=ihZEaj9ml4w)

> Standing on the shoulders of giants

## mutmut

After my initial review, mutmut seemed like the most straightforward
except the fact that you can no run tests in parallel but there is a
fork that does.  The code is another story. I will go through the
[fork](https://github.com/boxed/mutmut/pull/195) because it is the
code that I am most interested in.

### `cache.py`

In no particular order:

- I am still clueless about what is the point short lines of text as
global variables,

- I am an early fan of Object-Relation-Mapper, and I changed my
mind. I want to stress that [I am not the only one to find the ORM
abstraction dubious](https://news.ycombinator.com/item?id=14826496).

- init_db is way too much indented and score 7 level of indentations.

- If we dive into init_db we figure that it is a decorator, hence it
is not as evil as I was thinking to nest function definition. Nested
function definition do not play nice with the module pickle. It is
also painful from a performance perspective because the CPython VM
will not optimize it (closure allocation, useless free variables and
even the function definition that will be re- computed and
re-instanciated everytime the VM goes through init_db. The situation
is worse when a class is allocated at runtime).

- Re init_db, the first branch of the if should return early. That is
a case where "Do not Repeat Yourself" is harmful.

- The except OperationalError: pass is dubious.

- There is other problems with code details, but really the big design
mistake is to make database initialization something
unpredictable. initdb will decorate database function and initialize
the database once and only once the first time one of the cache (!)
function is called. From experience, it is much better to have a
dedicated function e.g. the function called wrapper called at every
entry points of the program or programs.

- Also db object is a global variable instanciateed from
pony.orm.Database at the top-level. I will not spend time discussion
slow global variable access with CPython, instead ask myself, why the
database initialization is not done at that point.


- The good thing in this code is that it [use
transaction](https://docs.ponyorm.org/transactions.html) (even if the
name is not explicit)

- A small nitpick the following code is difficult to test:

```python
def hash_of(filename):
    with open(filename, 'rb') as f:
        m = hashlib.sha256()
        m.update(f.read())
        return m.hexdigest()
```

Because it rely on a side-effect open the good abstraction if one is
necessary, is a sugar (!) that takes bytes as arguments and computes
the digest:

```
def sha256sum(bytes):
    m = hashlib.sha256()
    m.update(bytes)
    out = m.hexdigest()
    return out
```


The function sha256sum is very easy to tests, no need to fiddle with on disk
files during testing.

- In hash_of_tests: Modern python code should use pathlib.Path and
glob pattern matching.

- The whole thing could be re-written as a list comprehension and a
proper use of a helper function.

- `found_something` is not necessary, it should be an independent
predicate. I am not a great fan of exceptions, but return
NO_TESTS_FOUND would be written as raise SomeException in pythonic
code (in the case where there is no predicate that guard the hash
computation).

- print_result_cache has too many arguments and is too much nested (maybe use a
dataclass?)

- sorted(iterable) == list(sorted(iterable)) the list is spurious, it just does
copy the list created by sorted.

- itertools.groupby takes a sorted iterable as argument.

- create_html_report does not follow the "separation of concerns"
principles. It should really be at least two function 1) one to gather
the data 2) another to render the html

- Overall, the functions that are really related to the database take
high level abstractions that makes it a) difficult to test b) force
the data access layer to do operations that are not really data
related (like preparing the actual values to create, read, update or
delete) c) basic data types are easier to debug (except generators).

- I frown upon the use of getattr

I like the idea of [cache.py](http://cache.py/) but the name is not
well chosen, I prefer [db.py](http://db.py/) or something like
[dal.py](http://dal.py/) for data access layer.

### `__init__.py`

I start to think having code in __init__.py is not as evil as I
though, I might just be biased because of my experience with Django in
the early days.

- RelativeMutationID would be a good case of a dataclass.
- Again a lot of indentation.
- mutant_statuses would make a good Enum
- Ha! `**_`: it looks like a snake with big glasses!
- All the mutation function and sort-of framework could use their own file.
- The use of Context instances is broad and large in the code base but
  there is no docstring. It seems to be a configuration, with a lot of
  @property . Note: I consider @property harmful. dataclass? dict?

The following pattern:

```python
try:
    something()
except SomethingException:
    print("something that wants to be useful")
    raise
```

The above is useless. Instead of print it is better to comment the code and
avoid the try / except.

- In my opinion multi-line strings are painful. I prefer to use msg +=
line especially when I end up with a multi-line statement like raise
ProgrammingError(msg)

- mutate_node is almost two page long, with a very important code at
the end. It would be easier to read such as:

```python
def mutate_code(node, context):
    context.stack.append(node)
    try:
        maybe_mutate_code(node, context)
    finally:
    contexte.stack.pop()
```

An even better pattern is to use a context manager.

- Config vs. Context ?!

### `__main__.py`

That is the cli definition with the library called click that is not
my favorite library, I believe it is better to keep thing simple hence
I rely on docopt that does less magic (!) and gives you more control
(also,
[docopt](https://github.com/boxed/mutmut/issues/193#issuecomment-744015892)[
does display all
options](https://github.com/boxed/mutmut/issues/193#issuecomment-744015892)).
Interface are complex topic, and I have no definitive answer regarding
cli.

### `loader.py`

install will create a class object on the fly without directly relying
on type with top-level functions passed as arguments. That is a
performance optimization, but when the time of execution is several
days, most milliseconds matters.

Relative imports are difficult to read.

## cosmic-ray

Next I looked at cosmic-ray mostly because there was an exchange
between cosmic-ray's maintainer and mutmut's maintainer and I wanted
to see by myself what was the problem. I do my review a few month or
years after that exchange happened so the situation is different.

Spoiler: I find the code of cosmic-ray better, I disagree that the
mutations are not easy to extract and use them independently (except
that it requires to dive into openstack libraries, but that ought to
be good thing right !

The only thing I disagree with is the fact it rely on Celery (how hard
can it be.  Celery in that case is not necessary, because it is easier
to rely on multiprocessing, also even more so nowadays it is easier to
setup and configure a single machine with 20, 40 or even 128 thread
cores than the equivalent infrastructure with multiple machines. Also
less costly.

On the subject of server costs, it is a perfect time to share the following
blog post:

[Cerebralab Blog Note: Some details of the stories in this article are
slightly altered to protect the privacy of the companies I worked for It's
somewhat anecdotal, but in my work, I often encounter projects that seem to
use highly inefficient infrastructure providers, from a cost perspective.
https://cerebralab.com/Is_a_billion-dollar_worth_of_server_lying_on_the_ground
![](/logo.png)](https://cerebralab.com/Is_a_billion-
dollar_worth_of_server_lying_on_the_ground)

There is some interesting library in the requirements like yattag
which is not my favorite in-python html templating library but still
an interesting take, also stevedore should be the subject of follow up
review!

The code is rather short with 2196 python lines of code. The code look
visually nice, and is well commented. It use log as the variable name
that holds the python logger, hence I am not the only one to do that.

There is a few mistakes here and there, but the overall code is good!

I recommend to read cosmic-ray code if you are getting started with Python!

## Others

I did not have time to review the following projects:

- [EvanKepner/mutatest Are you confident in your tests? Try out mutatest and
see if your tests will detect small modifications (mutations) in the code.
Surviving mutations represent subtle changes that are undetectable by your
tests. These mutants are potential modifications in source code that
continuous integration checks would miss.](https://github.com/EvanKepner/mutatest)

- [mutpy/mutpy MutPy is a mutation testing tool for Python 3.x source code -
mutpy/mutpy!](https://github.com/mutpy/mutpy)

## Rework

- Unlike the maintainer of mutmut I think that parallel testing is a
requirement for this kind of tool.

- Unlike cosmic-ray's maintainer I think Celery is overkill (mind the
fact that Celery is an add-on in cosmic-ray)

- Deterministic behaviors are a good thing, and mutmut seems to miss that.

- mutmut seems to rely on sampling, but there is no way to control it.

- Again the process to test 15k lines of source code takes around 24
hours on my side even with the fork that use a thread-pool. More
optimizations? Yes, maybe, but more importantly, it would be nice to
be able to have a look at the results while the process is running
with a cli or better with a feature creep web interface.

Overall I am happy with the result, except the following:

- I could use multiple module files especially for the class
describing the mutations.

- Some functions could use better names.

- I need to replace the use of the imp package.

Last but not least, I need to replace parso with Python 3.9 ast
because it produce less noisy mutations.

forge at [~amirouche/mutation](https://git.sr.ht/~amirouche/mutation).
