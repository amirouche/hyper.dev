# 2017/01/01 - C'est jamais fini!

Un an et demi à peu près depuis mon dernier post d'humeur. À croire
que je n'ai pas d'humeur. C'est peut-être juste que je préfére passer
par des couloirs peu emprunté pour expliqué mon moi.

On m'a fait la remarque que je ne terminais jamais ce que je faisait.
Au debut je trouvais ça con. Ensuite j'ai compris que j'avais jamais
expliqué ce que j'essayais de faire.

En gros, en master j'ai pas pu rejoindre le master Traitement
Automatique du Langage (TAL) dans mon université et j'ai un master
"bateau" d'intégration logciel. J'ai un peu perdu mon
temps. Heureusement il y avais des cours d'IA quand même. Chemin
faisant je suis rentrée dans le jeu de l'intégrateur logiciel ou la
composition (hierarchique ou pas) d'application à la Django (beaucoup
mieux abordé dans aiohttp). J'ai beaucoup écrit et le contexte
problement m'a amené à me questionner sur l'utilisabilité du
code. Concretement par exemple, comment crée une app Django
generique. Ce qui est bien different d'un travail d'integrateur de
logiciel. Il s'agit de fournir un outils commun pour travailler
ensemble. Quelque part j'ai franchi une frontière. La compétence de se
mettre dans la peau de quelqu'un qui lit votre code est aussi utile
quand vous integrer des logiciels existant. Cela dit integrer c'est
surtout (à mon sens) écouter l'autre donc c'est moins evident de se
rendre compte que quelqu'un sera à votre place quand il relira votre
code.

A cette epoque j'ai decouvert neo4j sur #django-fr. En creusant je
suis tombé sur Tinkperpop Gremlin dont je suis tombé amoureux. J'étais
hyper fan des graphdbs.

Sur le chemin du poid cognitif associé à du code je me suis rendu
compte que le fait que Python ne puissent pas lancer "naturellement"
des chemins de code en parallèle me complexait. Aussi, berkeleydb
ne fonctionne juste pas assez bien en mode multiple processus. Et
dans le cas d'un processus de base de donnée asyncio était pas une
solution. J'ai même participé au projet PyPy STM avant de me rendre
compte que c'était pas pour tout de suite.

Je suis passé de Python à GNU Guile, en gros pour ça (c'est aussi une
façon facile pour moi de contribuer au projet GNU). Du coup, j'ai
ramené mes petits copains wiredtiger, graphdb et idées grandiloquentes

J'ai implementé plusieurs schema pour la graphdb puis j'ai decidé
d'utilisé le schema [EAV](http://bit.ly/2lEpnrK) que j'ai porté en
Python dans [AjguDB](https://github.com/amirouche/AjguDB) (désolé, il
n'y a pas de logo).

En GNU Guile, j'appelle ça UAV un acronyme pour Unique-identifier,
Attribute, Value.

J'ai continuer mes idées un peu loufoques d'implementer un clone de,
et j'ai repris [mes recherches](https://github.com/amirouche/culturia).

C'est jours-ci c'est [culturia](https://amirouche.github.io/Culturia/doc/)
que je vais pas finir.

> Peut-être que quand on franchit une frontière, on oublie tout.
