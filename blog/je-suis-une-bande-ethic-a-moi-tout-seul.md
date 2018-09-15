# 2018/01/01 - Je suis une bande éthic à moi tout seul

C'est pas juste que j'ai du cœur à l'ouvrage, sans sens apparat à
apparaitre aux après de celles et ceux qui revaient d'une enigme,
c'est ma passion.

Ce que j'ai fait comme contribution libre en 2017.

## Python

### Combinatorix

J'ai crée une bibliothèque pour écrire des parsers par composition de
fonctions. Au lieu de parser une grammaire, dans le cadre des parseur
par combinaison la grammaire c'est le code!
Vive [combinatorix](https://github.com/amirouche/combinatorix)!
Contrairement à d'autres implementations, il n'est pas
monadic... enfin pas à ma conaissance.

### BeyondJS

J'ai fait un prototype d'un framework inspiré de feu nevow qui permet
d'écrire des applications web sans passer par une ligne de javascript
et sans fichier HTML externe à l'aide d'une API dont je suis très fier
mais que j'ai completement pompé sur nevow. C'est pas exactement nevow
non plus car il utise pas twisted, mais aiohttp. Aussi, il est encore
moins utile (bien que possible) d'écrire du javascript pour faire des
trucs un peu kikoo. Spoiler, ça utilise un virtual dom.  La
connaissance de les API web (cf. [MDN](http://mdn.io/) est encore
requise. [Lisez le code sur github](https://github.com/amirouche/beyondjs)!

### Socialite

J'ai essayé de me lancer dans un gros projet mais j'ai juste integrer
deux trois bibliothèques ensemble pour que ça ressemble à quelque
chose d'utilisable proche de ce que fourni le monolithe Django. Ça
utilise ReactJS. Y a pas grand chose, mais ça m'a value quelques forks
et
étoiles. [Be social, star it](https://github.com/amirouche/xp-socialite)!

### maji

Je sais pas pourquoi j'ai fait
ça. Désolé. [https://github.com/amirouche/xp-maji](https://github.com/amirouche/xp-maji)

## Scheme

### scheme-todomvc

C'est mon plus gros succès de l'année! C'est la
fameuse
[todo app adapté en scheme](https://github.com/amirouche/scheme-todomvc) à
l'aide de snabbdom et inspiré de la version de Elm sans les
signaux. Il y a d'autres versions du "framework" que j'utilise pour
faire ça que je préfére à cette version. Mais cette version est la
plus présentable. Le coeur du truc (inspiré de Elm) est plus
testable. Ce que je retiens de cette experience, c'est que le Scheme à
travers le Scheme XML (aka. SXML) est très compétitif par rapport à JSX.

### guile javascript backend

Suite au GSoC de [Ian Price](http://shift-reset.com/) qui visaient
à adapter le backend JavaScript au nouveau code du compilateur de
Guile, j'ai corrigés deux ou trois bugs et j'ai rendu possible
d'appeller du JavaScript depuis Guile et du Guile depuis JavaScript.
Y a des morceaux du truc du scheme-todomvc la dedans. Malheureusement,
les navigateurs modernes (!) ne supportent toujours pas l'optimisation
des recurences terminales qui est pourtant dans le standard, donc en
gros c'est pas utilisable
jusqu'à
[nouvel ordre](https://kangax.github.io/compat-table/es6/#test-proper_tail_calls_(tail_call_optimisation))
(ou rappel l'ordre ;)).

Le code est
sur
[gitlab.com](https://gitlab.com/amirouche/guile/commits/compile-to-js-2017) cette
fois.

### guile-termbox

J'ai crée
des
[bindings pour la superbe lib termbox](https://github.com/a-guile-mind/azul.scm) (je
recommende
[ce fork](https://github.com/deathlyfrantic/termbox/tree/truecolor)
des vraies couleurs :) et un petit editeur de texte tout rikiki en
guise de documentation.

### Culturia

J'ai pas un, ni deux mais quatre repository culturia, le dernier se trouve
chez [framagit](https://framagit.org/a-guile-mind/culturia.next). Je sais
plus précisement ce que je veux faire. Et le terme pompeux c'est [Personal
Knowledge Base](https://en.wikipedia.org/wiki/Personal_knowledge_base).

## Autres

J'ai passé la barre des 3000 points sur stackoverflow et j'ai
écrit
[un challenge full stack](https://github.com/amirouche/full-stack-challenge) que
personne à ma connaissance n'a reussit. Il y a des étoiles qui se
perdent...
