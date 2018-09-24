# 2015/01/01 - Debuter avec la base de donnée clef-valeur bsddb

**Remarque** je préfère aujourd'hui [wiredtiger](http://wiredtiger.com).

Berkeley database est la base de donnée la plus utilisé dans le monde
d'après ses créateurs. Pourquoi? Car elle est très flexible. Ici je
vais pas m'étaler sur les différentes fonctionnalités. Je défriche la
création d'une base de donnée et la création d'index.

### Basics

Le backend btree est très bien pour créer un index ordonnée.

```python
import os
import shutil

from bsddb3.db import *

from json import dumps
from json import loads

# reset the database if it already exists
if os.path.exists('/tmp/bsddb'):
    shutil.rmtree('/tmp/bsddb')
os.makedirs('/tmp/bsddb')

# initialize the database
env = DBEnv()
env.open(
    '/tmp/bsddb',
    DB_CREATE | DB_INIT_MPOOL,
    0
)


def compare(a, b):
    # at initialisation time a & b are empty strings
    # those can't be deserialized by json
    if a and b:
        # a and b are string keys
        # In this case comparing them as is, is non-sens
        # they must be deserialized
        a = loads(a.decode('ascii'))
        b = loads(b.decode('ascii'))
        if a < b:
            return -1
        elif a == b:
            return 0
        else:
            return 1
    return 0


index = DB(env)
# set the function to compare keys
index.set_bt_compare(compare)
index.open('index', None, DB_BTREE, DB_CREATE, 0)


# populate the database

# keep track of all the values that are in the database
# in order of insertion
values = list()

i = 0  # keep track of insertion order
def populate(*key):
    global i
    values.append(list(key))
    key = dumps(key).encode('ascii')
    value = dumps(i).encode('ascii')
    index.put(key, value)
    i += 1

populate(1, 0, 0)
populate(3, 0, 0)
populate(0, 2, 1)
populate(2, 0, 0)
populate(0, 2, 0)

# fetch all index values in order
all = list()
cursor = index.cursor()
next = cursor.first()
while next:
    key, value = next
    key = loads(key.decode('ascii'))
    value = loads(value.decode('ascii'))
    all.append(key)
    next = cursor.next()

print('initial keys\t', sorted(values))
print('cursor keys\t', all)
assert sorted(values) == all
```

Un autre exemple plus parlant qui fait intervenir deux bases de
données:

```python
import os
import shutil

from bsddb3.db import *

from json import dumps as json_dumps
from json import loads as json_loads


def dumps(value):
    return json_dumps(value).encode('ascii')


def loads(value):
    return json_loads(value.decode('ascii'))


# reset the database if it already exists
if os.path.exists('/tmp/bsddb'):
    shutil.rmtree('/tmp/bsddb')
os.makedirs('/tmp/bsddb')

# initialize the database
env = DBEnv()
env.open(
    '/tmp/bsddb',
    DB_CREATE | DB_INIT_MPOOL,
    0
)


# create articles database
articles = DB(env)
# DB_HASH is recommanded for database
# that can not fit fully in memory
articles.open('articles', None, DB_HASH, DB_CREATE, 0)


# create index database
def compare(a, b):
    if a and b:
        a = loads(a)
        b = loads(b)
        if a < b:
            return -1
        elif a == b:
            return 0
        else:
            return 1
    return 0


def duplicate(a, b):
    # this compares ascii bytes values of the index
    # this is supposed to be the default comparaison
    # but the bsddb fails to do so
    if a < b:
        return -1
    elif a == b:
        return 0
    else:
        return 1

index = DB(env)

index.set_bt_compare(compare)
index.set_dup_compare(duplicate)
index.open('index', None, DB_BTREE, DB_CREATE, 0)


# populate the database
def populate(title, body, published_at, modified_at):
    value = dict(
        title=title,
        body=body,
        published_at=published_at,
        modified_at=modified_at,
    )
    value = dumps(value)
    # save article in articles database
    # here title is used as a key but it can
    # be anything memorable.
    key = title.encode('ascii')
    articles.put(key, value)

    # index the article
    key = (published_at, modified_at)
    key = dumps(key)
    value = title.encode('ascii')
    index.put(key, value)


body = 'a k/v store is a dictionary a set of key/value associations'
populate('Getting started with kv store (1/2)', body, 1, 5)
body = 'the gist of the practice of using kv stores is to build'
body += ' a schema on top of it using string patterns'
populate('Getting started with kv store (2/2)', body, 2, 2)

# for some reason the following article is put in the database
# before the followings even if it is published later
body = 'Wiretiger is kind of the successor of bsddb'
populate('Behold wiredtiger database (1/2)', body, 6, 10)

body = 'bsddb has still room to be put to good use.'
populate('Almighty bsddb (1/2)', body, 4, 3)
body = 'bsddb is stable!'
populate('Almighty bsddb (2/2)', body, 5, 2)

# the following articles will have the same index key
body = 'Working with wiredtiger is similar. Take advantage of its'
body += 'own features'
populate('Behold wiredtiger database (2/2)', body, 7, 0)
body = 'Good question'
populate('Is it worth the trouble?', body, 7, 0)


print('* All articles in chronological order')
cursor = index.cursor()
next = cursor.first()
while next:
    key, value = next
    key = loads(key)
    # the value is the title, this can also be used
    # to fetch the associated article in articles database
    title = value.decode('ascii')
    published_at, modified_at = key
    print('**', published_at, modified_at, title)
    next = cursor.next()


print('\n* All articles published between 4 and 6 inclusive in chronological order')

cursor = index.cursor()
next = cursor.set_range(dumps((4, 0)))
while next:
    key, value = next
    key = loads(key)
    if 4 <= key[0] <= 6:
        title = value.decode('ascii')
        published_at, modified_at = key
        print('**', published_at, modified_at, title)
        next = cursor.next()
    else:
        break


print('\n* Last three articles in anti-chronological order with body')
cursor = index.cursor()
previous = cursor.last()  # browse the index in reverse order
for i in range(3):
    # we don't need to deserialize the key
    _, value = previous
    # the value is the title, it is used to fetch the full article
    # datastructure. This is a join.
    article = articles.get(value)
    article = loads(article)
    title = value.decode('ascii')
    body = article['body']
    print('**', '%s: %s' % (title, body))
    previous = cursor.prev()
```

Comme c'est un peu très souvent qu'il faut construire des indexes
bsddb fournis des routines pour aider:

```python
import os
import shutil

from bsddb3.db import *

from json import dumps as json_dumps
from json import loads as json_loads


def dumps(value):
    return json_dumps(value).encode('ascii')


def loads(value):
    return json_loads(value.decode('ascii'))


# reset the database if it already exists
if os.path.exists('/tmp/bsddb'):
    shutil.rmtree('/tmp/bsddb')
os.makedirs('/tmp/bsddb')

# initialize the database
env = DBEnv()
env.open(
    '/tmp/bsddb',
    DB_CREATE | DB_INIT_MPOOL,
    0
)


# create articles database
articles = DB(env)
# DB_HASH is recommanded for database
# that can not fit fully in memory
articles.open('articles', None, DB_HASH, DB_CREATE, 0)


# create index database
def compare(a, b):
    if a and b:
        a = loads(a)
        b = loads(b)
        if a < b:
            return -1
        elif a == b:
            return 0
        else:
            return 1
    return 0


def duplicate(a, b):
    # this compares ascii bytes values of the index
    if a and b:
        if a < b:
            return -1
        elif a == b:
            return 0
        else:
            return 1
    return 0

index = DB(env)

index.set_bt_compare(compare)
index.set_dup_compare(duplicate)
index.open('index', None, DB_BTREE, DB_CREATE, 0)


# XXX: this is the main change to the code
def callback(key, value):
    # this will keep the index automatically up-to-date
    value = loads(value)
    published_at = value['published_at']
    modified_at = value['modified_at']
    key = (published_at, modified_at)
    key = dumps(key)
    return key
articles.associate(index, callback)


def populate(title, body, published_at, modified_at):
    value = dict(
        title=title,
        body=body,
        published_at=published_at,
        modified_at=modified_at,
    )
    value = dumps(value)
    # save article in articles database
    key = title.encode('ascii')
    articles.put(key, value)
    # no need to update the index database
    # it's done by bsddb


body = 'a k/v store is a dictionary a set of key/value associations'
populate('Getting started with kv store (1/2)', body, 1, 5)
body = 'the gist of the practice of using kv stores is to build'
body += ' a schema on top of it using string patterns'
populate('Getting started with kv store (2/2)', body, 2, 2)
body = 'Wiretiger is kind of the successor of bsddb'
populate('Behold wiredtiger database (1/2)', body, 6, 10)
body = 'bsddb has still room to be put to good use.'
populate('Almighty bsddb (1/2)', body, 4, 3)
body = 'bsddb is stable!'
populate('Almighty bsddb (2/2)', body, 5, 2)
body = 'Working with wiredtiger is similar. Take advantage of its'
body += 'own features'
populate('Behold wiredtiger database (2/2)', body, 7, 0)
body = 'Good question'
populate('Is it worth the trouble?', body, 7, 0)


# XXX: index cursor return the primary database value,
# a json serialized article dictionary, no need
# to do the join manually
print('* All articles in chronological order')
cursor = index.cursor()
next = cursor.first()
while next:
    # XXX: just like before key is the **index key**
    # for that article
    key, value = next
    # XXX: but the value is the serialized article value of
    # instead of the primary key of the article
    # which means that the join was done by bsddb
    article = loads(value)
    title = article['title']
    published_at = article['published_at']
    modified_at = article['modified_at']
    print('**', published_at, modified_at, title)
    next = cursor.next()


print('\n* All articles published between 4 and 6 inclusive in chronological order')

cursor = index.cursor()
next = cursor.set_range(dumps((4, 0)))
while next:
    key, value = next
    key = loads(key)
    if 4 <= key[0] <= 6:
        article = loads(value)
        title = article['title']
        published_at = article['published_at']
        modified_at = article['modified_at']
        print('**', published_at, modified_at, title)
        next = cursor.next()
    else:
        break


print('\n* Last three articles in anti-chronological order with body')
cursor = index.cursor()
previous = cursor.last()  # browse the index in reverse order
for i in range(3):
    key, value = previous
    article = loads(value)
    title = value.decode('ascii')
    body = article['body']
    print('**', '%s: %s' % (title, body))
    previous = cursor.prev()


# XXX: The get method of the secondary database ie. the index
# also returns the primary data instead of the primary key
# of the article
print('\n* Retrieve the article published the 6/10')
# XXX: Using index.pget will return (primary_key, primary_data)
# here it's not required to retrieve the primary key
# since it's also available as part of primary_data
value = index.get(dumps((6, 10)))
article = loads(value)
title = article['title']
published_at = article['published_at']
modified_at = article['modified_at']
print('**', published_at, modified_at, title)
value = index.pget(dumps((6, 10)))

# XXX: Let's delete that article
key = title.encode('ascii')
articles.delete(key)

# XXX: Try to retrieve it from the index just like before
value = index.get(dumps((6, 10)))
assert value is None  # it's not anymore in the secondary index
```

### Multi processus

Apparament on peux faire du multiprocess avec BerkeleyDB, voilà un
exemple pas très concluant d'après mes tests:

```python
#!/usr/bin/env python3
import os
from time import sleep
from datetime import datetime
from hashlib import md5
from json import dumps as _dumps
from json import loads as _loads
from shutil import rmtree
from bsddb3.db import *
from sys import exit
from multiprocessing import Process


def dumps(v):
    return _dumps(v).encode('ascii')


def loads(v):
    return _loads(v.decode('ascii'))


# reset database
path = '/tmp/bsddb-mutliprocess'
if os.path.exists(path):
    rmtree(path)
os.makedirs(path)


def opendb():
    # create and open database environment
    env = DBEnv()
    env.set_cachesize(1, 0)
    env.set_tx_max(4)
    flags = (DB_INIT_LOG |
             DB_INIT_LOCK |
             DB_INIT_TXN |
             DB_CREATE |
             DB_INIT_MPOOL
    )
    env.open(
        path,
        flags,
        0
    )
    # create database
    txn = env.txn_begin(flags=DB_TXN_SNAPSHOT)
    flags = DB_CREATE | DB_MULTIVERSION
    counter = DB(env)
    counter.open('counter', None, DB_BTREE, flags, 0, txn=txn)
    txn.commit()
    return env, counter


def writer(identifier):
    print('writer', identifier, 'running')
    env, counter = opendb()
    # open database and update it
    txn = env.txn_begin(flags=DB_TXN_SNAPSHOT)
    counter.put(identifier, dumps(0), txn=txn)
    txn.commit()

    for i in range(100):
        # print('writer', identifier, '@ iteration', i)
        txn = env.txn_begin(flags=DB_TXN_SNAPSHOT)
        count = counter.get(identifier, txn=txn)
        count = loads(count)
        count += i
        counter.put(identifier, dumps(count), txn=txn)
        txn.commit()
        sleep(0.2)
    print('writer', identifier, 'finished')
    counter.close()
    env.close()
    exit(0)


def reader(identifiers):
    # print('reader running')
    env, counter = opendb()
    for i in range(100):
        for identifier in identifiers:
            txn = env.txn_begin(flags=DB_TXN_SNAPSHOT)
            count = counter.get(identifier, txn=txn)
            txn.commit()
            if count:
                count = loads(count)
                print('time:', i, 'read', identifier, count)
        sleep(1)
    print('reader finished')
    counter.close()
    env.close()
    exit(0)


def uuid():
    now = datetime.now()
    now = now.isoformat()
    data = now.encode('ascii')
    id = md5(data)
    id = id.hexdigest()
    return id.encode('ascii')


if __name__ == '__main__':
    jobs = list()
    # spawn (or fork?) two writer
    identifiers = list()
    for i in range(2):
        identifier = uuid()
        identifiers.append(identifier)
        p = Process(target=writer, args=(identifier,))
        p.start()
        jobs.append(p)

    # spawn (or fork?) one writer
    p = Process(target=reader, args=(identifiers,))
    p.start()
    jobs.append(p)

    # check for deadlocks...
    env, counter = opendb()
    while True:
        dead = 0
        for job in jobs:
            if not job.is_alive():
                dead += 1
        if dead == 3:
            break
        r = env.lock_detect(DB_LOCK_DEFAULT)
        if r != 0:
            print('deadlock')

    # print result
    txn = env.txn_begin(flags=DB_TXN_SNAPSHOT)
    for identifier in identifiers:
        count = counter.get(identifier, txn=txn)
        if count:
            count = loads(count)
            print(identifier, count)
    txn.commit()
    counter.close()
    env.close()
```

### Astuce des entrées en double (ou composition de clef)

Avec le backend Btree il est possible d'avoir plusieurs valeurs pour
une meme clef. A chaque db.put('super-dupper-high-mojo-key', value)
une nouvelle entrée est crée dans la base de donnée avec la clef et
cette valeur. Si la clef existe déjà elle est ajouté à la fin (par
défaut).

Le problème c'est que lorsqu'on supprime la clef
db.delete('super-dupper-high-mojo-key'), la base va supprimer toutes
les entrées. C'est pas forcement ce que l'on veux. Une façon de
contourner ce problème est de mettre la valeur dans la clef et utilisé
une chaine vide comme valeur.

Par exemple, si on index les propriétés des documents avec leur valeur
de façon à pourvoir retrouver tous les documents qui ont une valeur
donnée pour un champs donnée. Il faut utiliser un curseur, le placer à
l'aide de cursor.range correctement:

```python
from collections import namedtuple


cursor = index.cursor()

# Keys have the following format:
#
#  (attribute_name, value, identifier) -> ''
#
# Where identifier is the identifier of a document
# with ``attribute_name`` set to ``value``.
#
KeyIndex = namedtuple('KeyIndex', ('attribute', 'value', 'identifier'))


def lookup_documents_identifiers(attribute, value):
    # The idenfier placeholder is set to the empty
    # string so that the cursor will be positioned at the first
    # key found for the combination of ``attribute``
    # and ``value`` if any, because the empty strings is the
    # smallest string value and the index is sorted.
    lookup = KeyIndex(attribute, value, '')
    next = cursor.set_range(dumps(lookup))

    while next:
        key, _ = next  # value is a useless empty string
        key = KeyIndex(*loads(key))
        # check that key is within bound of the lookup
        if (key.attribute == lookup.attribute
            and key.value == lookup.value):
            yield key.identifier
            next = cursor.next()
        else:
            # it can mean that:
            #
            #   key.attribute != lookup.attribute
            #
            # which means there is no more document indexed
            # with this attribute, no need to iterate over more
            # keys
            #
            # or that:
            #
            #   key.value != lookup.value
            #
            # They are some document that have a value for
            # ``lookup.attribute`` but ``key.value`` is not
            # what we look for and will never be anymore since
            # the index is ordered.
            #
            # In both case, there is no more matching documents.
            break
```

En utilisant ce schema il est possible de mettre à jour l'index quand
la valeur d'un attribut change sans impacter les autres documents
ayant la meme valeur pour un attribut.

Y a d'autres chose dans bsddb évidemment. Si le sujet vous interesse
je vous conseille de lire les documents fournis par Oracle.
