# 2018/09/28 - SQL is the ORM killer

I think the future of data persistence is
[FoundationDB](http://foundationdb.org/) but I don't want to fight
several battles at the same time. For the time being, let's tackle a
pervasive pratice: Object-Relational Mapper. This is so much
entrenched in programming practice that people don't think about it.
It's somewhat like Object-Oriented Programming in a multi-paradigm
language, like, say Python, of course I will use a class! Of course, I
must use an ORM.

In this article, I will explain why ORM is a poor pratice.

## ORM is not a good abstraction

In Python, most people know ORM through Django. Django's ORM is a
**mega** abstraction that try to solve several problems:

1. The ORM wants to be a class-based Python representation of the
   *underlying* RDBMS tables.

2. It's also throught it's `pre_save` and `post_save` hooks a way to
   enforce some constraints on the data.

3. It's also somekind of facade on top the SQL query language.

4. Abstract differences between several databases

This seems like an anti-pattern on first sight as it does not follow
the [single responsability
principle](https://en.wikipedia.org/wiki/Single_responsibility_principle). But
it's worse than that since I omitted that it also try to validate the
schema and data. With an ORM you are on your way for god classes that
break all designs that aim for separation of concerns like
Model-View-Controller.

We will kill all those preconceptions and see how they solved problems
you don't have and worse they hinder progress toward scalable
applications.

## Class-based representation doesn't help

To get started, but many will see it as minor annoyance, if any, most
ORM force you to use classes which adds complexity to the code from
the start.

Python representation of the database schema is wishful thinking but
it doesn't deliver in practice.

First, because of the [Object-relational impedance
mismatch](https://en.wikipedia.org/wiki/Object-relational_impedance_mismatch).

Simply said, the structure of the database doesn't map with
Object-Oriented Programming. In simple cases, for instance tables with
foreign keys it works, but as soon as you start building a more
complex data layer (many-to-many relations, table inheritance or
polymorphic data) you end up with a complicated python representation
that is actually a breeze to deal with in the database native language
namely SQL. Not only that, but it is made very easy in Python to shoot
yourself in the foot because the ORM hides the actual complexity of a
given query throught its numerous layers like the [`SELECT` n +
1](https://stackoverflow.com/q/97197/140837).

Another tooted advantage of having a Python representation of the
schema is that you can do introspection. That is nice. Everything
in the confort of Python metaclass complex architecture. But that is
not an argument anymore since posgresql has introspection. So the same
django-admin you all love (meh) can be built with raw pyscopg or
better [asyncpg](https://github.com/MagicStack/asyncpg). So,
introspection is not a good argument.

Some people say, that Python is more readable than SQL. With that I
heartedly agree if you disregard the complexity required to create
that readable syntax. That being said, having the schema described in
Python is not DRY since the schema is also stored in the database.

## You won't need `pre_save` and `post_save`

`pre_save` and `post_save` hooks implement, as far as I can tell, some
kind of observable pattern. That is, you keep an eye on what happens
on the data and enforce some rules. It is like database triggers but
done in Python.

I argue that `pre_save` and `post_save` hooks are an
anti-pattern. Most likely, the code that goes into those should be in
either a validator or a domain function (if you prefer, read "business
function"). If you start using `pre_save` and `post_save` you are
hardcoding domain behaviors in the model which leads to god classes
and ugly `if`.

Last but not least, remember that Django is a framework that was meant
to create an ecosystem of reusable applications. That's why it
provides hooks and signals. What I want you to notice is that in real
world scenario where you build an application for yourself, especially
after the Minimum Viable Product or prototype, you head your way to a
monolith where you are fully in control. That is completly different
from the Django use-case where you want Joe to extend Jane's
application.

## Embrace the power of SQL

The abstraction on top of SQL is moot. That is ORM does not help you
completly avoid SQL and it gives you more guns to shoot yourself.

Of course, SQL has another syntax but the ultimate language doesn't
exists, especially if you plan to deliver something this month. You
should rather keep thing simple and avoid building too much
abstraction in order to keep things in control. Using too much
abstraction, is the best way to see the complexity of your project
explode.

My point is an ORM helps to write simple queries but it's not easy to
write complex queries. Even when you use SQL, you need to fine tune
your query to best make use of indices. If you use an abstraction on
top of SQL, you will need to think about the correct SQL and then
translate that to the correct ORM query incantation.

I won't go into the Django `QuerySet` with its manager shenanigans
because again, it leads to god classes with ugly `if` and yet another
time it makes the OOP approach the default choice where **a proper use
of basic data types and function are good enough.**

The last bit is the same as the first, in the end you will need to
know SQL to take full advantage of your RDBMS.

## Conclusion

I used to practice (read abuse) a lot Object-Oriented Programming and
I loved Django ORM and I was impressed by SQLAlchemy. I grew up (read
learned a lot), and I think I know better. OOP can be useful, god
objects are not. That's what you will end up with using ORM god
objects and bad patterns.

I hope I gave enough elements to answer the question for yourself.  I
omitted some elements, for instance, when you aim for performance you
do not want to `SELECT * FROM table` all the time and that you end up
with pieces of data that don't map to your `Model` classes except if
you build dozens of classes. Of course an ORM haz a **workaround**!
Or you won't use automagic migration tool in big projects.

I also did not dive into the issues related to the use of JSON data
types that is now part of modern postgreSQL. That leads to other
interesting problem that are partly solved in Object Document Mappers
aka. ORM for document stores. I have not extensive experience with
those but my choice will be prolly the same. Stick with the basics,
see where they are patterns and solve those with carefully choosed
abstractions.

Think about it carefully. Known good and somewhat obvious guiding
principles like "single responsability principle" or "seperation of
concerns", try to be **systematic**: always solve the problem the same
way. In particular, ORM are not systematic, simple queries are done
some way, complex queries are complicated and not explicit...

*Caveat emptor*!
