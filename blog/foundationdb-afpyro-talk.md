# 2019/10/07 - FoundationDB

Ceci est un rendu approximatif avec quelque ameliorations au talk que
j'ai donnee hier chez BackMarket.

## A Database To Rule Them All

Derriere ce titre pompeux se cache la volonte a peine voile de faire
de FoundationDB votre principale source de verite dans votre systeme
d'information.

Mais aujourd'hui je ne veux pas (uniquement) vous vendre FoundationDB
et transmettre une idee plus grande. A savoir, comment aborder la
programmation des bases de donnee clef-valeur ordonnees. Contrairement
au `dict` Python, ce n'est pas l'ordre d'insertion qui prime mais la
comparaison lexicographic entre les octets, autrement dit l'ordre du
dictionaire des langues naturelles.

### Kesako FoundationDB

FoundationDB est une base de donnee ordonee clef-valeurs scalable
horizontalement qui est
[ACID](https://fr.wikipedia.org/wiki/Propri%C3%A9t%C3%A9s_ACID) et
respecte les guaranties de Coherence et resiste au erreurs de
Partionnement dans le cadre du [theoreme
CAP](https://fr.wikipedia.org/wiki/Th%C3%A9or%C3%A8me_CAP).  Les
garanties offertes sont similaires a PosgreSQL (c'est dire CP)

Voir https://apple.github.io/foundationdb/cap-theorem.html

C'est aussi une base de donnee mieux tester que les bases de donnees
qui ont endurer les tests [jespen.io](https://jepsen.io/). En fait,
l'un des foundateur de FoundationDB a quitte Apple pour se concentrer
sur cette methode de developpement (qui en somme est du TDD++) dans
une entreprise dedies a promouvoir cette pratique dite de la
simulation.

Voir [https://www.youtube.com/watch?v=fFSPwJFXVlw](https://www.youtube.com/watch?v=fFSPwJFXVlw).

Cela etant dit, l'idee la plus importante pour commencer la
programmation avec FoundationDB est l'idee qu'il s'agit d'un
*dictionaire ordonnee*.  Et cette "ordre" fait de FoundationDB une
base tres versatiles. En preservant les garanties ACID et CP pour les
charges temps reels, elle peux s'adapter a n'importe quelle (!)
modele de donnee. D'ou l'idee d'en faire la source de verite
principale.

Un dictionaire ordonnee, comme [l'arbre rouge et
noir](https://fr.wikipedia.org/wiki/Arbre_bicolore), n'est pas
uniquement utile pour rangee des entiers dans l'ordre croissant ou
decroissant avec une complexite logarithmique. L'ordre permet de creer
des structures ou abstraction de pus haut niveau.

### Who use FoundationDB

Je vous renvoie vers les [FoundationDB Summit de
2018](https://www.youtube.com/playlist?list=PLbzoR-pLrL6q7uYN-94-p_-Q3hyAmpI7o),
ainsi que le [future summit de
2019](https://forums.foundationdb.org/t/foundationdb-summit-2019/1636?u=amirouche)
de la Linux Foundation.

TL;DR: Des entreprises qui doivent gerer de gros volume de donnee.

Note: voir le talk: ["Lightning Talk: Entity Store: A FoundationDB
Layer for Versioned Entities with Fine Grained Authorization and
Lineage"](https://www.youtube.com/watch?v=16uU_Aaxp9Y&list=PLbzoR-pLrL6q7uYN-94-p_-Q3hyAmpI7o&index=2&t=0s)
qui discute d'une base de donnee utilise dans le cadre de pipeline de
data science chez Apple (ecrit en Python 2.7 :).

### Why use FoundationDB

- Vous avez plus d'un 1TB de donnee

- Vous avez besoin de resistance au panne et donc besoin de replication, YOLO!

- Vous avez de l'argent a investir sur le long terme. Le projet reste
  jeune et beaucoup de fruits restent a ceuillir.

- Vous voulez apprendre quelque chose de nouveau, sans quitter votre zone de confort :)

### When not to use FoundationDB

Vous n'avez pas besoin d'utilisez FoundationDB sur vos projet legacy
qui tourne bien! Si vous utilisez PosgreSQL pour votre projet perso ou
d'entreprise probablement que cela va tenir a certains temps.

Cela dit sachez que FoundationDB, n'est pas la seule base de donnee
clef-valeur ordonnnees.

Il y a:

- SQLite LSM extension, voir https://github.com/coleifer/python-lsm-db/
- MongoDB Wiredtiger
- Facebook RocksDB
- Google LevelDB
- Et feu [bsddb](https://docs.python.org/2/library/bsddb.html)

Sans oublier TiKV ou Google Spanner (privatif). A ce sujet je
recommende la lecture du papier ["Spanner: Google's
Globally-Distributed
Database"](https://ai.google/research/pubs/pub39966).

(Et pendant que j'y suis le papier surnomme [Large-scale cluster
management at Google with
**Borg**](https://ai.google/research/pubs/pub43438))

(Note: relire ["Fast key-value stores: An idea whose time has come and
gone"](https://ai.google/research/pubs/pub48030))

### How to program FoundationDB

L'ordre du dictionaire FoundationDB n'est pas l'ordre d'insertion!

L'ordre du dictionaire FoundationDB n'est pas l'ordre d'insertion!

L'ordre du dictionaire FoundationDB n'est pas l'ordre d'insertion!

Grace a tuple.pack on peux considerer que foundationdb est un
dictionaire de tuple ordonnee selon l'ordre naturel des types de bases
`int`, `float`, `byte`, `str`.

Oui vous avez bien lu entre les lignes, il y a un couple de fonction
qui permet de traduire certains types Python vers des bytes qui
perservent l'ordre de ses types.

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

**L'ordre permet de creer des structures ou abstraction de plus haut niveau.**

### The End

Avant de commencer garder en tete que FoundationDB n'est pas tres
facile a mettre en production, mais c'est facile a tester en dev. Il y
a un backend memoire et un backend ssd. Et un nouveau backend appeller
redwood qui va lever [certaines des limitations decrites dans la
documentation
officielle](https://apple.github.io/foundationdb/known-limitations.html#known-limitations).
