# 2017/03/01 - Do It Yourself: a Graph Database in Python

You maybe already know that I am crazy about graph databases. I am
trying to build a graph database in Python. Which graphdb? Well this
is a moving target. The following design is a good for small databases
that don't include a lot of big fields.

One must know that there is much much less code in this graphdb
implementation than in the previous iteration on ajgudb. I think it a
good fit for graph exploration and analysis but anything that is
bigger than a personnal website will not work, for sure. It doesn't
provide transactions anyway.

It's main advantage is that it's simple and that everything is indexed.

It is inspired from datomic Entity-Attribute-Value pattern. It based
on a schema I call the TupleSpace.

### What is the Tuple Space

The idea behind tuple space is to store a set of tuples inside a
single table that look like the following:

```scheme
(1, "title", "Building a python graphdb in one night")
(1, "body", "You maybe already know that I am...")
(1, "publishedat", "2015-08-23")

(2, "name", "database")

(3, "start", 1)
(3, "end", 2)

...

(4, "title", "key/value store key composition")

...

(42, "title", "building a graphdb with HappyBase")
```

The tuple can be described as (identifier, key, value).

If you study the above example you will discover that both edges
(aka. ManyToMany relations) are represented using the same tuple
schema.

Representing ForeignKey is possible but is left as an exercice to the
reader ;)

### Implementation of a Tuple Space

The first section describe the API of the TupleSpace, following section describe how the TupleSpace is implemented on the storage.

#### API

The API provided by the tuple space is document oriented instead of tuple oriented. It looks like the following:

```python
class TupleSpace:

    def get(self, uid):
        """Return all tuples with the given uid"""
        pass

    def add(self, uid, **properties):
        """Add the tuples formed with key/value pairs
           taken from `properties` and `uid`"""
       pass

    def delete(self, uid):
        """Delete tuples with `uid`"""
        pass

    def query(self, key, value=''):
        """Iterate the index for tuples having `key` and
           optionaly `value`"""
        pass
```

#### Schema

To implement the above schema inside an ordered key/value store we have to find a relevant key. That key I think, is the composition of the identifier and name. This leads to definition of the following table Key:

```python
Key(identifier, name) -> Value(value)
```

Every Key is unique and is associated with a Value. Given the fact that the store is ordered one can easily retrieve every (key, value) tuple associated with a given identifier by going through the the ordered key space.

The above tuple space will look like the following in the key/value database; using a high level view ie. not bytes view:

```
*******|           Key            |                 Value
-------+------------+-------------+------------------------------------------
Colunms| identifier |  name       |                 value
-------+------------+-------------+------------------------------------------
       |     1      |   title     | "Building a python graphdb in one night"
       |     1      |   body      | "You maybe already know that I am..."
       |     1      | publishedat |              "2015-08-23"
       |     2      |   name      |                database

       |     3      |   start     |                   1
       |     3      |    end      |                   2

            ...          ...                         ...

       |     4      |   title     |     "key/value store key composition"

            ...          ...                         ...

       |     42     |   title     |    "building a graphdb with HappyBase"

            ...          ...                         ...
```

#### Key composition

To keep the database ordered you need to pack correctly the components of the Key. You can not simply convert string to bytes, how will you distinguish the string from the other components of the key? You can't use the string representation of number ie. "42" for "42". Remember "2" is bigger than "10".

In a complete TupleSpace implementation one must also take into acccount that values can be of many types.

The simple case of positive integers is solved by struct.pack('>Q', number).

The solution to support all numbers is to always use the same packing schema whatever the sign and whether they are float or not.

Here is a naive packing function that support every Python objects, keeps the ordering of strings and positive integers where integers comes before strings which come before other kind of Python values:

```python
def pack(*values):
    def __pack(value):
        if type(value) is int:
            return '1' + struct.pack('>q', value)
        elif type(value) is unicode:
            return '2' + value.encode('utf-8') + '\0'
        elif type(value) is str:
            return '3' + value + '\0'
        else:
            data = dumps(value, encoding='utf-8')
            return '4' + struct.pack('>q', len(data)) + data
    return ''.join(map(__pack, values))
```

In database that is column aware it's not always required to build
such packing function as the database already has way to compose key
as columns.

### GraphDB

At this point, the TupleSpace provides documents and some relational
paradigm as you can work with references. AjguDB provides a layer on
top of TupleSpace to easily work with a graph database.

#### Data model

The first aspect is building the graph data model:

Vertex are simple TupleSpace documents which identifieres come from
document 0, a counter which is incremented everytime a new vertex or
edge is created. Moreover it stores in _meta_type key that the
document represent a Vertex.

Edge are also simple TupleSpace documents with their identifier come
from the counter document with 0. Same as Vertex, Edge document store
as _meta_type the fact that they are edge. Moreover start and end
attributes are also stores in the TupleSpace document.

Given the fact that every tuples are indexed, it's easy to retrieve
all incomings and outgoings edges of a given Vertex so it's not
required to cache them in the Vertex document (as it is done in ajgu).

#### Better schema

A better schema will use one row per document and use the same row to
store all edge information. That said tuple spaces is an existing
pattern in use in distributed databases.

DIY.
