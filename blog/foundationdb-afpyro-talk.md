# 2019/10/07 - FoundationDB

Ceci est un compte rendu approximatif, avec quelque améliorations, au
talk que j'ai donné hier chez BackMarket.

## A Database To Rule Them All

Derrière ce titre pompeux se cache la volonté a peine voilée de faire
de FoundationDB votre principale source de vérité dans votre système
d'information.

Mais aujourd'hui je ne veux pas (uniquement) vous vendre FoundationDB
et transmettre une idée plus grande. À savoir, comment aborder la
programmation des bases de données clef-valeur
ordonnées. Contrairement au `dict` Python, ce n'est pas l'ordre
d'insertion qui prime mais la comparaison lexicographique entre les
octets, autrement dit l'ordre du dictionnaire des langues naturelles.

### Kesako FoundationDB

FoundationDB est une base de données ordonnée clef-valeurs scalable
horizontalement qui est
[ACID](https://fr.wikipedia.org/wiki/Propri%C3%A9t%C3%A9s_ACID) et
respecte les garanties de Cohérence et résiste aux erreurs de
Partitionnement dans le cadre du [théorème
CAP](https://fr.wikipedia.org/wiki/Th%C3%A9or%C3%A8me_CAP). Les
garanties offertes sont similaires a PosgreSQL (c'est à dire CP).

Voir
[https://apple.github.io/foundationdb/cap-theorem.html](https://apple.github.io/foundationdb/cap-theorem.html)

C'est aussi une base de données mieux testée que les bases de données
qui ont enduré les tests [jespen.io](https://jepsen.io/). En fait,
l'un des fondateur de FoundationDB a quitté Apple pour se concentrer
sur cette méthode de développement (qui est en somme du TDD++) dans
une entreprise dédiée à promouvoir cette pratique, dite de la
simulation.

Voir
[https://www.youtube.com/watch?v=fFSPwJFXVlw](https://www.youtube.com/watch?v=fFSPwJFXVlw).

Cela étant dit, l’idée la plus importante pour commencer la
programmation avec FoundationDB est l’idée qu'il s'agit d'un
_dictionnaire ordonné_. Et cette "ordre" fait de FoundationDB une base
très versatile. En préservant les garanties ACID et CP pour les
charges temps réel, elle peut s'adapter à n'importe quel(!) modèle de
données. D’où l’idée d'en faire la source de vérité principale.

Un dictionnaire ordonné, comme [l'arbre rouge et
noir](https://fr.wikipedia.org/wiki/Arbre_bicolore), n'est pas
uniquement utile pour ranger des entiers dans l'ordre croissant ou
décroissant avec une complexité logarithmique. L'ordre permet de créer
des structures ou abstraction de plus haut niveau.

### Who use FoundationDB

Je vous renvoie vers les [FoundationDB Summit de
2018](https://www.youtube.com/playlist?list=PLbzoR-pLrL6q7uYN-94-p_-Q3hyAmpI7o),
ainsi que le [future summit de
2019](https://forums.foundationdb.org/t/foundationdb-summit-2019/1636?u=amirouche)
de la Linux Foundation.

TL;DR: Des entreprises qui doivent gérer de gros volume de données.

Note: voir le talk: ["Lightning Talk: Entity Store: A FoundationDB
Layer for Versioned Entities with Fine Grained Authorization and
Lineage"](https://www.youtube.com/watch?v=16uU_Aaxp9Y&list=PLbzoR-pLrL6q7uYN-94-p_-Q3hyAmpI7o&index=2&t=0s)
qui discute d'une base de données utilisée dans le cadre de pipeline
de data science chez Apple (écrit en Python 2.7 :).

### Why use FoundationDB

*   Vous avez plus d'un 1TB de donnée

*   Vous avez besoin de résistance aux pannes et donc besoin de réplication, YOLO!

*   Vous avez de l'argent à investir sur le long terme. Le projet reste jeune et beaucoup de fruits restent à cueillir.

*   Vous voulez apprendre quelque chose de nouveau, sans quitter votre zone de confort :)

### When not to use FoundationDB

Vous n'avez pas besoin d'utiliser FoundationDB sur vos projet legacy
qui tournent bien! Si vous utilisez PosgreSQL pour votre projet perso
ou d'entreprise probablement que cela va tenir un certain temps.

Cela dit sachez que FoundationDB, n'est pas la seule base de données
clef-valeur ordonnées.

Il y a:

*   SQLite LSM extension, voir [https://github.com/coleifer/python-lsm-db/](https://github.com/coleifer/python-lsm-db/)
*   MongoDB Wiredtiger
*   Facebook RocksDB
*   Google LevelDB
*   Et feu [bsddb](https://docs.python.org/2/library/bsddb.html)

Sans oublier TiKV ou Google Spanner (privatif). À ce sujet je
recommande la lecture du papier ["Spanner: Google's
Globally-Distributed
Database"](https://ai.google/research/pubs/pub39966).

(Et pendant que j'y suis le papier surnommé [Large-scale cluster
management at Google with
**Borg**](https://ai.google/research/pubs/pub43438))

(Note: relire ["Fast key-value stores: An idea whose time has come and
gone"](https://ai.google/research/pubs/pub48030))

### How to program FoundationDB

L'ordre du dictionnaire FoundationDB n'est pas l'ordre d'insertion!

L'ordre du dictionnaire FoundationDB n'est pas l'ordre d'insertion!

L'ordre du dictionnaire FoundationDB n'est pas l'ordre d'insertion!

Grâce à tuple.pack on peut considérer que foundationdb est un
dictionnaire de tuples ordonnés selon l'ordre naturel des types de
bases `int`, `float`, `byte`, `str`.

Oui vous avez bien lu entre les lignes, il y a un couple de fonctions
qui permet de traduire certains types Python vers des bytes qui
préservent l'ordre de ces types.

Voir le module
[`fdb.tuple`](https://github.com/apple/foundationdb/blob/master/bindings/python/fdb/tuple.py#L21)
dans les bindings Python officiels.

En gros:

```python
from fdb import tuple


before = (1, 2, 3)
after = (10, 20, 30)

assert before < after
assert tuple.pack(before) < tuple.pack(after)
```

Et aussi, c'est une operation reversible:

```python
from fdb import tuple


expected = (123456789, 3.1415, ("hello", "world"), b'\x13\x37')

assert tuple.unpack(tuple.pack(expected)) == expected
```

**L'ordre permet de créer des structures ou abstractions de plus haut niveau.**

### The End

Avant de commencer, garder en tête que FoundationDB n'est pas très
facile à mettre en production, mais c'est facile à tester en dev. Il y
a un backend mémoire et un backend ssd. Et un nouveau backend appellé
redwood qui va lever [certaines des limitations décrites dans la
documentation
officielle](https://apple.github.io/foundationdb/known-limitations.html#known-limitations).
