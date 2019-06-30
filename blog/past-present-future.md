# 2019/06/30 - Past, Present, and Future

> Plans are worthless, but planning is everything. There is a very
> great distinction because when you are planning for an emergency you
> must start with this one thing: the very definition of “emergency”
> is that it is unexpected, therefore it is not going to happen the
> way you are planning.

# Past

My main focus was working on the sample implementation for SRFI-167
and SRFI-168 along the continued work on a real implementation on top
of WiredTiger using (Chez Akku) Arew Scheme. I managed to get together
a release dubbed 0.1.1, that you can try using the following command:

> git clone [https://github.com/scheme-live/srfi-167-and-168-tutorial](https://github.com/scheme-live/srfi-167-and-168-tutorial)

The standardization process is kicking and more people got involved by
sharing wishes, bug reports and in general valuable positive and
negative feedbacks. My talk on this subject to [Scheme
Workshop](https://icfp19.sigplan.org/track/scheme-2019-papers) was
accepted. I would have liked write and submit a full paper about it, I
mostly failed. I started writing a tutorial (book?) about the Ordered
Key-Value Store that is called [Around Multi-Model
Database](/around.20190624v1.pdf).

I drew [a
plan](https://github.com/awesome-data-distribution/datae/issues) in
the sand of github about datae.

I put together some ideas about [peer-to-peer
networks](https://github.com/scheme-live/peer-to-peer-network) and
[functional package manager](https://github.com/scheme-live/sin).

Also, schemedoc launched [Awesome
Scheme](https://github.com/schemedoc/awesome-scheme/).

I got involved in some W3C mailling list related to RDF and AI.

At last, I got some energy to read things and listen to Noam Chomsky.

I found especially interesting the text entitled: [Design Principles
Behind
Smalltalk](https://www.cs.virginia.edu/~evans/cs655/readings/smalltalk.html).

Here is a first quote about their "scientifical" approach to design
systems:

> Our work has followed a two- to four-year cycle that can be seen to
> parallel the scientific method:
>
> - Build an application program within the current system (make an
>   observation)
>
> - Based on that experience, redesign the language (formulate a
>   theory)
>
> - Build a new system based on the new design (make a prediction that
>   can be tested)
>
> The Smalltalk-80 system marks our fifth time through this cycle.

Here is another about the relation between tools, individual
accomplishments and how to achieve them:

> I'll start with a principle that is more social than technical and
> that is largely responsible for the particular bias of the Smalltalk
> project:
>
> Personal Mastery: If a system is to serve the creative spirit, it
> must be entirely comprehensible to a single individual.
>
> The point here is that the human potential manifests itself in
> individuals. To realize this potential, we must provide a medium
> that can be mastered by a single individual. Any barrier that exists
> between the user and some part of the system will eventually be a
> barrier to creative expression. Any part of the system that cannot
> be changed or that is not sufficiently general is a likely source of
> impediment. If one part of the system works differently from all the
> rest, that part will require additional effort to control. Such an
> added burden may detract from the final result and will inhibit
> future endeavors in that area. We can thus infer a general principle
> of design:

> Good Design: A system should be built with a minimum set of
> unchangeable parts; those parts should be as general as possible;
> and all parts of the system should be held in a uniform framework.

Seems like the spirit of Scheme or [worrydream.com](http://worrydream.com/).

I also liked the [lisp os
text](http://metamodular.com/Common-Lisp/lispos.html). Here is the
part that echoed the most with my work:

> Object store based on tags

> Instead of a hierarchical file system, we propose an object store
> which can contain any objects. If a file (i.e. a sequence of bytes)
> is desired, it would be stored as an array of bytes.

> Instead of organizing the objects into a hierarchy, objects in the
> store can optionally be associated with an arbitrary number of
> tags. These tags are key/value pairs, such as for example the date
> of creation of the archive entry, the creator (a user) of the
> archive entry, and the access permissions for the entry. Notice that
> tags are not properties of the objects themselves, but only of the
> archive entry that allows an object to be accessed. Some tags might
> be derived from the contents of the object being stored such as the
> sender or the date of an email message. It should be possible to
> accomplish most searches of the store without accessing the objects
> themselves, but only the tags. Occasionally, contents must be
> accessed such as when a raw search of the contents of a text is
> wanted.

> It is sometimes desirable to group related objects together as with
> directories of current operating systems. Should a user want such a
> group, it would simply be another object (say instances of the class
> directory) in the store. Users who can not adapt to a
> non-hierarchical organization can even store such directories as one
> of the objects inside another directory.

While the idea of building a Scheme operating system is beautiful.  I
don't have enough time for it. Much inspiration can be taken from
existing projects like GNU Guix,
[Mezzano](https://github.com/froggey/Mezzano) or Unikernels...

Another interesting read is: [Accelerating Science: A Computing
Research
Agenda](https://cra.org/ccc/wp-content/uploads/sites/2/2016/02/Accelerating-Science-Whitepaper-CCC-Final2.pdf):

> Accelerating Science: The Value Proposition
>
> Cognitive tools for acclerating science could lead to dramatic
> increases in scientific productivity by increasing efficiency of the
> key steps in scientific process, and in the quality of science that
> is carried out (by reducing error, enhancing reproducibility), allow
> scientific treatment of topics that were previously impossible to
> address, and enable new modes of discovery that leverage large
> amounts of data, knowledge, and automated inference.

... and allow effective learning.

# Present and Future

The sample implementation for SRFI-167 in particular needs more love.
It happens that I need it, for some future projects. Among others I
use it in emacs-like editor and I might rely on it in the functional
package manager. I have still things to figure.  It seems like I am
trying to shoehorn it, especially in the case of the functional
package manager. In the case of the editor, it is less likely to be a
mistake because indeed it is helpful and implements separation of
concerns like Model-View-Controler. Having the same data-structure
everywhere is helpful and it is more powerful than a hash-table or
struct as it allow to easily do introspection to ease debugging.

While I was excited by datae as a demonstration of change-request
mechanic over structured data that is bigger than memory. I was
thinking that it might lead to making a living out-of-it with grants,
community support or consulting. Getting together that software with
100% support of SPARQL is not impossible. The question is do I really
want to invest my time in this particular project?  At some point,
"maybe" is not anymore an acceptable answer. In the meantime, I will
just put it on "standby" mode.

I am discussing a possible relicencing of Arew into something dubbed
business-friendly most likely Apache 2.0. This will lead to a split of
the project into two components. The first will remain in Arew and
will be dedicated to [R7RS](https://r7rs.org) support and moar.  The
second repository will be prolly called babelia and will be licensed
in a fork of the Affero GPL licence that is more humane, more sensible
to the challenges faced by the anthorposcene.

I got a better idea about my Personal Knowledge Base project or if you
prefer my Personal Assistant or Research Assistant. To quote Ronald
J. Brachman:

> Can we have realistically useful Knowledge Base that is designed in
> the absence of specific intended applications?

Otherwise said, I need an application of the application (!) to be
able to dogfood the idea. I think studying Artificial Intelligence and
its history is a good subject of study, in particular I need to learn
more about non-monotoic logic and ordinal number systems.
