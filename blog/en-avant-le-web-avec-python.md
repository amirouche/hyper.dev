# 2017/01/01 - En avant le web avec Python 3

A l'approche de la [pycon france 2017](https://www.pycon.fr/2017/) (à
Toulouse (du 21 au 24 Septembre)). Je reflechissait à proposer une
présentation de [`asyncio`](https://docs.python.org/3/library/asyncio.html)
ou [aiohttp](https://aiohttp.readthedocs.io/). La solution proposer par
les developpeurs de CPython pour faire du dev asynchrone.

Aussi je me suis dit qu'avant de faire ça se serait bien de faire le
point sur papier numerique pour voir si ce que j'avais à dire était
assez interessant.

Pour dire vrai, je ne suis pas developpeur CPython, ni `aiohttp` et je
pense pas avoir assez de billes pour faire une conf uniquement sur
ça. Donc voilà ma reflexion sur le sujet du developpement web en
Python.

## Kesako la programmation asynchrone?

A vrai dire, on s'en fou! Tout ce qu'on peut garder à l'esprit c'est
que c'est plus facile de traiter beaucoup de clients avec.

## Kesako `asyncio` ?

`asyncio` est une bibliothèque (de programmation asynchrone) qui vise
à tirer partie de la nouvelle syntaxe `async` et `await` introduit
dans la [PEP 492](https://www.python.org/dev/peps/pep-0492/).

On connaissait déjà la programmation asynchrone en Python 2 grace à
twisted et son framework
web [Nevow](https://en.wikipedia.org/wiki/Nevow) utilisant les
callbacks. On peut resumer l'experience twisted au points suivants:

- Python c'est bien
- Les callbacks caymal

`asyncio` s'inspire de twisted mais utilise dans son incarnation en
Python 3.5 les mots clefs `async` et `await` qui permettent la
programmation asynchrones sans callbacks! Et c'est pour ça qu'on peux
mettre de coté toutes les subtilités de la programmation asynchrone
dans la majorité des cas (et c'est pourquoi on s'en fou au final que
se soit asynchrone).

Un code python 3.5+ ressemblera à un code python 2, saupoudré des
mots-clefs `async` et `await`.

## Kesako `async` et `await` ?

`async` et `await` c'est des nouveaux mots-clefs du langage Python.

Dans `asyncio` si une fonction est declaré comme `async` alors `await`
peut apparaitre à l'interieur de cette fonction. `async` est utilisé
dans `asyncio` pour declarer une fonction asynchrone. `await` est
utilisé pour appeller une fonction asynchrone. Typiquement votre code
va ressembler à quelque chose comme ça:

```python
async def ma_fonction_asynchrone():
    out = await une_autre_fonction_asynchrone()
    return out
```

Mais j'ai dit qu'on en avait rien à faire de la programmation
asynchrone?! C'est là en quelque sorte que l'abstraction au dessus des
callbacks **leak** de façon controllé. Mais c'est pas grave, car
l'utilisation de ces mot-clefs est clairement identifiés et fait
partie de l'API des bibliothèques qui utilisent `asyncio`. Suffit de
faire ce qui est marqué dans la doc!

Derrière toussa, il y a un protocole (comme le protocole des itérables
utilisé pour faire fonctionner les boucles `for`). Jetez un oeil à
la [PEP 492](https://www.python.org/dev/peps/pep-0492/) si vous voulez
en savoir plus. Mais sachez que c'est pas la peine de lire et
comprendre ce document pour utiliser `asyncio`.  J'en suis la preuve
vivante.

En fait, `async` et `await` sont uniquement là pour rendre la
programmation asynchrone explicite et donc plus facile à
maintenir. Cela permet de savoir en un coup d'oeil si une fonction (ou
méthode...) peut etre interrompue et où elle pourra etre
interrompue... Cela dit c'est pas vraiment la peine de s'en soucier
dans une première approche de la programmation asynchrone qui se
limite à l'utilisation des bibliothèques existantes.

Pour pas vous laisser desoeuvré fasse à cette nebuleuse asynchrone, je
rajouterai juste que ça deviens interessant de savoir quand une
fonction peut-etre interrompue quand plusieurs flux d'execution
accèdent à la meme ressource. Autrement dit, c'est un usage avancé
(sauf si vous creez vous meme des globales (ou autres valeurs
partagées) dans votre programme (accessible en ecriture (si les
globales sont accessibles en lecture uniquement cela ne pose pas de
problème))).

**En gros**, il suffit de savoir que vous serez obligé de marquer les
fonctions asynchrones comme `async` et utiliser `await` pour les
appeller comme dit dans la doc. Et c'est tout!

## Kesako `aiohttp`

`aiohttp` est un cadre de developpement web qui inclus:

- un serveur et un client HTTP classique
- un serveur et un client WebSocket qui peut participer à la boucle
  d'évènement que le serveur HTTP classique. C'est à dire qu'un meme
  executable peut servir les client HTTP et websocket et partager les
  ressources tel que les connections à la base de donnée. Et comme
  c'est un seul programme on peut programmer salement!
- un mecanisme de routage à la Django et Flask basé sur les regex qui
  supporte
  les
  [applications recursives](http://aiohttp.readthedocs.io/en/stable/web.html#nested-applications).

Et c'est tout et c'est déjà pas mal je trouve. D'autre bibliothèques
viennent completer ce framework (un peu comme dans l'écosystème Flask)
cette base et fournissent connections à la base de donnée à travers
SQLAlchemy (ou pas!) ou meme
une
[abstraction aux systèmes de cache REDIS ou memcached](https://github.com/argaen/aiocache)

Contrairement à un avis repandu ça ressemble beaucoup à du code python
2 classique à la Django ou Python saupoudrer de `async`/`await`. Ça
change des habitudes et c'est plus relou que la fonction `print` en
terme de reflexe (surtout que les erreurs sont pas toujours clairs, en
tout cas en Python 3.5.3).

Le seul cas qui peux arriver avec aiohttp qui n'arrive jamais en
python 2 synchrone c'est
l'[annulation d'une coroutine](https://github.com/aio-libs/aiohttp/issues/2098) et
donc du controlleur d'une requête. Ce qui peux poser problème si par
exemple on met à jour à la fois la base de donnée et le cache ou si on
**n**'utilise **pas** de transactions ou si on fait de l'autocommit...

## `aiohttp` vs. Django vs. Flask

Je vais pas mentir, le gros souci par rapport aux approches synchrones
(lire Django et Flask) c'est le manque d'utilisateurs et du coup y a
moins de bibliothèques prêtes à etre utiliser ou on trouve encore des
bugs... Mais c'est pas comme si les applications Django étaient sans
bugs...

`aiohttp` c'est un peu comme flask (avec le support des websocket dans
le même thread en plus), il y a pas d'ORM par défault, pas de
framework de formulaire par défaut etc... Donc un peu comme en
Javascript il faut avoir des idées sur comment monter un cadre
logiciel complet.

J'ai commencer le dev avec Django est je trouvai ça super simple, la
doc est clair (et maintenant en plus en français) et des centaines
d'applications pour démarrer son projet rapidement et à vrai dire je
recommanderai encore d'utiliser Django (plutôt que Flask ou `aiohttp`)
pour prototyper (sauf si on a besoin de websocket).

Après le stade du prototype, Django et Flask c'est pas le top.

Apparemment les performances sont moins bonnes, à vérifier.

Mais en plus les choix qui sont fait sont pas toujours geniaux:

- Je trouve qu'utiliser un ORM c'est se tirer une balle dans le pied,
  par exemple le problème
  des
  [requêtes N+1](https://stackoverflow.com/questions/97197/what-is-n1-select-query-issue).
  J'ai cru au début que l'ORM m'éviterai d'apprendre le
  SQL. Faux. Déjà il faut apprendre comment fonctionne l'ORM (aurevoir
  SQLAlchemy). Ensuite il est encore nécessaire de comprendre le SQL
  pour analyser les requêtes générer par l'ORM. Donc au final,
  pourquoi ne pas simplement utiliser le SQL qui est enseigné de base
  dans toutes les formations que je connais.

- L'utilisation massive des globales (apps, url router, template, database
  connection, requete...) ce qui rend le code imbitable cf. dans
  Flask
  cf. [`ctx.py`](https://github.com/pallets/flask/blob/master/flask/ctx.py) et
  [`globals.py`](https://github.com/pallets/flask/blob/master/flask/globals.py) ou
  [dans Django la gestion de plusieurs bases de données](https://docs.djangoproject.com/fr/1.11/topics/db/multi-db/).

- Mélanger la validation des données et le rendu, c'est bien dans le cadre
d'un prototype et ça s’arrête là.

Là je me fourvoie peut-être, mais la dernière fois que j'ai regarder
il y a deux ans, le support des apps dans Django n'était pas
suffisant.  Disons que je créer une application pour vendre du pain
bio. Je met en place la partie métier spécifique kivabien:

```python
painbio = web.Application()

business = web.Application()

# ajouter les routes kivonbien
business.add_route('POST', '/command', handle_command)
business.add_route('GET', '/receipt/{id}/', handle_receipt)

painbio.add_subapp('/', business)
```

Maintenant, je souhaite ajouter un petit blog à mon application pour
faire de la propagande. En Django, ce n'est pas aussi simple que:

```
blog = nerfed.Blog()
painbio.add_subapp('/blog', blog)
```

En Django, il faut ajouter toutes les app dependantes une par une dans
le bon ordre pour que ça marche dans le `settings.py` en passant par
une indirection sous forme de chaine de caractères. C'est un peu
dommage.  Alors qu'avec `aiohttp`, on a un début de réponse convenable
avec
les
[applications recursives](http://aiohttp.readthedocs.io/en/stable/web.html#nested-applications).

Avec toussa on pourrai ajouter que Django channels va ressoudre le
problème de riches tel que les
websockets,
[voyez vous meme](http://channels.readthedocs.io/en/stable/index.html),
c'est pas simple, pas accessible tout sauf la philosphie Python.

## CQFD

Je vais continuer à travailler sur mon *nouveau*
projet [socialite](https://github.com/amirouche/socialite) et au final
faire quelque chose en me basant sur ce travail l'an prochain, ce qui
je pense aura plus d’intérêt.

> Note: 2018/02/11, en fait ça m'étonnerai que je libère du temps pour
> faire quoi que se soit en Python sur mon temps libre.

## Et demain ?

Python dans ton browser?!

[Commentaires sur le journal du hacker](https://www.journalduhacker.net/s/otns6m/en_avant_le_web_avec_python)
