# 2015/01/01 - Recommendations basées sur les graphes

**Remarque** L'API de ajgudb a changé!

### Prélude

Comme vous le savez peut-être déjà je suis un fan des graphes. L'idée
qui ma charmé initialement est qu'il s'agit d'une base de donnée sans
schema à la mongodb avec un support des transaction sur plusieurs
modifications.

Le fonctionnement de [ajgudb](https://pypi.python.org/pypi/AjguDB)
reflette cette intêret dans le sens où ils y a un support complet des
transactions tel qu'on peux le trouver dans des bases de données
classiques comme postgresql and mysql.

Chemin faisant, j'ai découvert concepnet et je me suis rendu compte
que c'était pas très rapide de charger la base de donnée. J'ai fait
quelques tests avec wiredtiger je me suis rendu compte que c'était
possible de passer de plusieurs heures de chargements à quelque
minutes en utilisant le schema adéquat.

Entre temps, j'ai fait des experiences toujours avec
wiredtiger. Inpiré par Guile et datomic j'ai crée un schema que
j'appelle le TupleSpace. Assez fascinant. Et je me suis rendu compte
que c'était non seulement completement posssible d'utiliser ce schema
pour modeliser une base de donnée en forme de graphe mais que les
performances ne devait pas être mauvaise dans un certains nombre de
contexte.

### AjguDB

Dans les grandes lignes voilà le fonctionnement de la nouvelle
iteration d'ajgu nommé AjguDB qui n'offrent pour le moment qu'un
backend LevelDB.

Definition du TupleSpace:

- Une table où chaque ligne est un tuple: identifiant, nom, valeur

- Une autre table où les tuples sont indexés de cette façon: nom, valeur, identifiant

Definition du schema de la graphdb au dessus du TupleSpace:

- Élément Edge

- Élément Vertex

Et enfin ajout du language de requete Gremlin qui est le grand absent
de ajgu. Je me demande comment faisaient les gens avant.

### Recommendation de film

Une des choses que l'on peux faire avec une graphdb c'est de la
recommendation. Ce n'est pas la méthode la plus populaire. Mais elle
peut-être plus puissante que la méthode classique de recommendation
item-item car elle permet de prendre en compte l'existence de
connection indirecte entre les items, ça demande quand même du
travail. Donc nous n'etudirons pas cette méthode pour le moment.
Préparation

En attendant de nous allons nous contenter de recommendation classique
item-item, c'est à dire «si machin à aimer ce film, tu devrais aimer
ce film».

La première chose à faire est d'installer AjguDB:

```
pip install ajgudb
```

Ensuite télécharger le dataset movielens small:

```
wget http://files.grouplens.org/datasets/movielens/ml-latest-small.zip
```

Une fois decompressé, il faut charger le dataset dans ajgudb à l'aide du script suivant:

```python
from csv import reader

from ajgudb import AjguDB


if __name__ == '__main__':
    graph = AjguDB('db')

    # create indices
    print('Starting load of `movies.csv` in `db/`')
    with open('./movies.csv', 'r') as f:
        next(reader(f))  # skip heading
        for id, title, genres in reader(f):
            props = dict()
            props['label'] = 'movie'
            props['id'] = id
            props['title'] = title
            movie = graph.vertex(**props)
            for genre in genres.split('|'):
                genre = graph.get_or_create(
                    label='genre',
                    name=genre
                )
                movie.link(genre, label='partof')

    print('Starting load of `ratings.csv` in `db/`')
    with open('./ratings.csv', 'r') as f:
        next(reader(f))  # skip heading
        for userid, movieid, value, timestamp in reader(f):
            # get or create user
            user = graph.get_or_create(label='user', id=userid)
            # create edge between movie and user
            movie = graph.select(label='movie', id=movieid).one()
            props = dict()
            props['value'] = int(float(value))
            props['timestamp'] = int(float(timestamp))
            rating = user.link(movie, label='rating', **props)

    print('Starting load of `tags.csv` in `db/`')
    with open('./tags.csv', 'r') as f:
        next(reader(f))  # skip heading
        for userid, movieid, value, timestamp in reader(f):
            movie = graph.select(label='movie', id=movieid).one()
            user = graph.select(label='user', id=userid).one()
            props = dict()
            props['value'] = value
            props['timestamp'] = float(timestamp)
            tag = user.link(movie, label='tag', **props)

    print('closing')
    graph.close()
```

Ça c'est fait!

### Recommendation

Cette partie est inspiré de «[A graph based movie recommender engine](http://markorodriguez.com/2011/09/22/a-graph-based-movie-recommender-engine/)»

Ouvrer une console ipython and ouvrez la base:

```python
from ajgudb import AjguDB; from ajgudb.gremlin import *; db = AjguDB('db')
```

Maintenant nous pouvons laisser s'exprimer toutes la puissance des gremlins.

Récupérons le film Toy Story par exemple:

```python
movie = db.get(1)
```

Pas trop difficille quand on connais déjà l'identifiant. Mais sinon on peut faire:

```python
movie = db.one(title='Toy Story (1995)')
```

Ça c'est fait. A l'occasion on pourra changer de film.

Pour connaitre la moyenne des notes superieurs à 3 on fait:

```python
query = db.query(
      incomings,
      select(label='rating'),
      key('value'),
      filter(lambda g, x: x.value > 3),
      value,
      mean
)
query(movie)
```

Ce qui s'est passé:

- À partir du film, on a remonté vers les arêtes entrantes à l'aide de incomings

- Puis on a séléctionné les arêtes des notes à l'aide de select(label='rating')

- Ensuite on demande la valeur de la clef de chaque arete avec key('value') pour avoir la note attribué

- Suite à ça, on filtre les notes

- Enfin on demande la valeur contenu dans l'iterateur et on fait la moyenne

Pas compliqué. Le langage est dynamique vous ne pouvez pas composer n'importe quel étape avec n'importe quel autre. Par exemple une fois que vous avez réupérer la valeur contenu dans l'iterateur avec value vous ne pouvez plus remontez dans les resultats avec l'étape back que je prensente dans la suite.

Une fois qu'on a filtrer les valeurs des notes on peux revenir sur les arêtes qui ont les notes que l'on veux considerer à l'aide de back. Cette étape retourne avec la selection actuel à l'étape précédente de selection, dans ce cas le select(label='rating'). Ce qui veux dire que dans l'iterateur on va trouver à la place des notes superieur à 3, toutes les arêtes qui ont une note superieur à 3. Pour verifier on peux faire:

```python
query = db.query(
      incomings,
      select(label='rating'),
      key('value'),
      filter(lambda g, x: x.value > 3),
      back,
      get
)
query(movie)
```

L'étape get récupère les elements (noeuds ou arêtes) référencés dans l'iterateur et consome l'iterateur. Ce qui veux dire que plus aucune étape n'est possible après get.

Les arêtes de notes vont de l'utilisateur qui a donné la note vers le film noté. Pour récupéré les utilisateurs qui ont données les notes qui ont été selectionné, on ajoute l'étape start à la requete:

```python
query = db.query(
      incomings,
      select(label='rating'),
      key('value'),
      filter(lambda g, x: x.value > 3),
      back,
      start,
      get
)
query(movie)
```

On va stocké la query précédentes dans liked_by comme ça, le code sera plus lisible.

```python
liked_by = db.query(
         incomings,
         select(label='rating'),
         key('value'),
         filter(lambda g, x: x.value > 3),
         back,
         start
)
```

Remarquez qu'on a retirez le get à la fin.

Maintenant on veux connaitre les films que ces utilisateurs ont bien notés. Ce qui va donner une idée des films à recommender à quelqu'un qui a bien aimé toy story:

```python
likes = db.query(
      outgoings,
      select(label='rating'),
      key('value'),
      filter(lambda g, x: x.value > 3),
      back,
      end
)
```

Si vous lisez bien likes fait le parcours inverse de liked_by.

Autre chose, la requetes précédentes va forcement retourner les même
films plusieurs fois. On peux afffiner le resultat on passant par une
étape de comptage group_count qui utilise un simple Counter.

Le counter va grouper tous les resultats dans un même élément dans
l'iterateur. Pour completer cette étape final nous allons d'abord
récupérer les résultats dans l'ordre des plus courant, derouler la
liste, en enfin récupérer le titre des films:

```python
sort = db.query(
    group_count,
    each(lambda g, x: x.most_common()),
    scatter,
    each(lambda g, x: x.value[0]),
    key('title'),
    limit(10),
    value
)
```

Sans grande surprise on retrouve Toy Story comme premier film à
recommender aux gens qui ont aimé Toy Story :)

Le programme complet:

```python
from ajgudb import AjguDB
from ajgudb.gremlin import *  # noqa

db = AjguDB('db')

liked_by = db.query(
    incomings,
    select(label='rating'),
    key('value'),
    filter(lambda g, x: x.value > 3),
    back,
    start
)

likes = db.query(
    outgoings,
    select(label='rating'),
    key('value'),
    filter(lambda g, x: x.value > 3),
    back,
    end
)

sort = db.query(
    group_count,
    each(lambda g, x: x.most_common()),
    scatter,
    each(lambda g, x: x.value[0]),
    key('title'),
    limit(10),
    value,
)


movie = db.one(title='Toy Story (1995)')

for item in sort(likes(liked_by(movie))):
    print item
```

Et voilà!
