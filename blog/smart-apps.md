# 2012/06/01 - Applications intelligentes: catégorisation et recommandations de textes courts

Cet article est à propos de la catégorisation de tweet, j'espère que
les non-anglophone arriverons à suivre avec les schémas

## Préface

Last year I was conducting some research about ways to improve the
usability of Twitter. At the same time I was told about work about
machine learning similar to what StumbleUpon
does. I though that a similar feature in the context of Twitter or any
reader apps would be awesome. So I started digging the problem and
find out that even without strong machine-learning knowledge it was
possible to come up with solutions that in theory could give good
results. There might be better, more deeper solutions of the problem,
what I want is to outline the algorithm used to achieve such
application. But I did not implement it because I believe that without
GraphDBs the solution will a) not be scalable b) not be flexible
enough to add new data c) not flexible enough to implement (new)
algorithms, plus I wanted to have my own application (suite) to
implement this features in.

![De Lapide Philosophico.](smart-apps/ouroboros.jpg)

##  Application intelligente


What I call a smart application is an application that goes forward
user needs and guess or at least try to guess and learn from users
actions/inputs and environnement. Given the context of twitter
application, I am thinking about users and tweets categorization and
users and tweets recommendation. I put the features in this order
because recommendation use categorization to take its decisions, but
it is not the only information it uses. Best smart features are
seamlessly integrated to the current use of the application, that's
what I try to do in the following post.  First how does it look like ?

![The sidebar displays the user's labels, shows the list of category, the gray labels in messages are generated](smart-apps/pyadoop.jpg)

### Catégorisation de tweet et d'utilisateurs

Given a tweet, I wanted to put it in a category, so that at the end of
the day I have properly organised list of tweets #LifeHacks kind of
tweets, #Music tweets, #RandomSmartLinks and #Python stuff properly
organized. While at the same time, given a tweet being able to know
what it is talking about without having to click on it or read
it. This are really interesting information and is, if doable and
applicable, promising for longer texts, and it is.  Given a Twitter
user there is a number of tweets that are tagged plus the network of
followings which have also tagged their tweet, we have the first level
of tweet features, that can be used to build category with. Each user
is associated with the labels he or she used in her or his tweets and
the tweets of her or his network.

![Label network of level one](smart-apps/twitter-label-network.png)

Every red-purple edge has a weight but it's not represented.  With
this data design we can already add most interesting labels in user
profile, but tweet hashtags are not always interesting as features of
users and tweets, for this matter we can use a white-list or
black-list that can be manually or automatically generated with most
popular hashtags but we can also use semantic expansion, based on a
corpus of hierarchical labels that can be easily retrieved from
Wikipedia and well organized websites like github, bitbucket,
delicious, Amazon, newsgroups, forums, dmoz and the like. It's true
that the extracted data might need to be cleaned but a simple
blacklist based on Wiktionary will make the manual work way much
easier. Similarly labeling texts aka. features extraction from random
websites can be made easier using this blacklist method. By semantic
expansion, I mean retrieving the most probable generic word that is
linked to a hashtag, using a hierarchical taxonomy make this easier, a
networked taxonomy make the algorithm a bit more complex but
doable. Given this data/knowledge we can build the second level and
third level of labels. The second level of labels are the labels
extracted from content of tweets or links. The third level is labels
we find with semantic expansion which are represented in green in the
following graphic, they are just like any other labels:

![labels of level two and three discovered by smart algorithms](smart-apps/expansion-extraction.png)

With this knowledge we can compute tags for both user and tweets and
if there is some trouble to find the right label, for instance given
the word «Python», we need to distinguish the animal from the
language, we can use the other labels to find out using a collocation
weight edges in the network of labels.  The fourth level of labels, is
given a tweet with hastags stripped, perform with it a full-text
search on a database of Wikipedia extended with linked articles and
link tweets with the best wikipedia article results.  Tweet
categorization is then just a matter of matching the user interests
with the labels associated with tweets.  Recommandation d'utilisateur
et de tweet The easiest way to recommend users is by looking up an
user's network of followings and retrieve the most common
users. Similarly it is also possible to recommend tweets based on the
«+fav» and «RT» of your network. But this is bound to the first degree
of your network, you can't discover a tweet or an user at 6 degrees of
separation.  To discover tweets and user you can also use the
item-item algorithm used to power Amazon recommendation algorithm, but
you might hit a dimension problem.  If you have categorized your user
and tweets, this can also be achieved to do user and tweet
recommendation by matching user or tweets with similar labels. The
following give an example of a possible implementation to recommend
users:

Tweets recommendation is similar.

## More like this

- FIXME
- FIXME
- FIXME
