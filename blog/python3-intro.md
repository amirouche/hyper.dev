# 2015/01/01 - Les bases du langage Python 3

Les bases qui permettent de se servir de Python comme d'une calculette
pour faire les courses et plus si affinités.

Cette note est basée sur
[learn X in Y minutes](http://learnxinyminutes.com/docs/python3/) sous
license Creative Commons by-sa. La license est maintenue à
l'identique.

```
#!/usr/bin/env python3
# Une ligne de commentaire commence par un croisillon

# La PEP8 recommende de laisser un espace après le croisillion
# cf. http://legacy.python.org/dev/peps/pep-0008/

# La PEP8 recommende de ne pas écrire de lignes de plus de 80
# caractères. Si le commentaire ne tiens pas en une ligne
# il est possible d'enchainer les lignes de commentaires.


# 1. Types de bases et leurs opérateurs

# Il existe deux types de nombres:
# - les nombres décimaux dit flottants
# - les nombres entiers

# Les opérations mathématiques ressemblent à des opérations mathématiques
1 + 1  # => 2
8 - 1  # => 7
10 * 2  # => 20

# Les commentaires peuvent aussi se trouvrer à la fin d'une ligne.
# La PEP8 recommende de laisser deux espaces à la fin du code
# avant le croisillon

# Par défaut la division retourne un nombre flottant
35 / 5  # => 7.0

# Il existe un opérateur de division entière (ie. euclidienne)
5 // 3  # => 1
-5 // 3  # => -2

# Si un flottant apparait dans une opération arithmétique
# le resultat sera un flottant
3 * 2.0  # => 6.0

# La division entière de deux flottants va retourner
# la "version" flottant du resultat de la division entière
5.0 // 3.0  # => 1.0 au lieu de 1
-5.0 // 3.0  # => -2.0 au lieu de 2

# Pour réalisé un modulo il faut utiliser le caractère ``%``
7 % 3  # => 1

# Il est possible d'utiliser des parenthèses pour grouper
# les opérations arithmétiques
(1 + 3) * 2  # => 8

# Il existe un type booléen
True
False

# Il est possible de nier une valeur booléene à l'aide de
# l'opérateur ``not``
not True  # => False
not False  # => True

# L'opération d'égalité se fait à l'aide d'un double signe égale
1 == 1  # => True
2 == 1  # => False

# Il existe aussi un opérateur d'inégalité
1 != 1  # => False
2 != 1  # => True

# Ainsi que les opérateurs classiques de comparaisons
1 < 10  # => True
1 > 10  # => False
2 <= 2  # => True
2 >= 2  # => True

# Il est possible d'enchainer les comparaisons
1 < 2 < 3  # => True
2 < 3 < 2  # => False

# Il y a trois façons de rentrer des chaines de caractères
string = 'This is also a string.'
# Dans la chaine suivante le caractère ``'`` apparait
string = "Lil' did you know."
# Dans la chaine suivante les caractères ``'`` et ``"``
# apparaisent dans la chaine. Aussi la chaine peut s'étaler
# sur plusieurs lignes.
string = """This isn't a "mishmash

this pure Python!"""

# Il est possible d'acceder aux élèments de la chaine à l'aide
# de l'opérateur ``spam[]``
"This is a string"[0]  # => 'T'

# Il est possible d'ajouter des chaines de caractères
chaine = "Hello " + "world!"  # => "Hello world!"

# Cela dit ce n'est pas la méthode recommendé, il faut lui preferer
# l'interpolation
"%s can be %s" % ('string', 'interpolated')


# ``None`` est un objet unique, il correspond à ``null`` dans
# d'autres langages
None  # => None

# Il ne faut pas utiliser l'opérateur d'égalité ``==`` pour comparer
# un objet à ``None``. ``is`` est l'opérateur qu'y conviens.
"etc" is None  # => False
None is None  # => True


# 2. Variables et Collections

# Pour créer une variable, il suffit de lui assigner une valeur
some_var = 5
some_var  # => 5

# La PEP8 recommende d'utiliser des lettres_minuscules_separe_par_des_espaces
# pour nommer les variables

# Il est possible d'assigner une nouvelle valeur à une variable sans
# autre forme de procès
some_var = 3.14
some_var = True

# Acceder à une variable qui n'a pas été définit précédemment va
# lever une erreur dites "NameError"
some_unknown_var
# Traceback (most recent call last):
#   File "<stdin>", line 1, in <module>
# NameError: name 'some_unknown_var' is not defined


# Créer une liste ordonnée vide
some_list = list()
# Créer une liste ordonnée avec des élèments
some_other_list = [3, 4, 5, 6]

# Pour acceder à un élèment de la liste, la meme syntaxe vue
# por les chaines peut-etre utilisé
some_other_list[0]  # => 3

# En cas de dépassement, une erreur dite "IndexError" est levé
some_other_list[4]
# Traceback (most recent call last):
#   File "<stdin>", line 1, in <module>
# IndexError: list index out of range


# Il est possible de parcourir la liste en sens
# inverse en utilisant des index négatifs
some_other_list[-1]  # => 6
some_other_list[-2]  # => 5

# Il est possible de retirer des élèments de la liste à l'aide du mot-clef ``del``
del some_other_list[2]  # [3, 4, 6]


# Il est possible d'ajouter une liste à une autre liste
a = [1, 2, 3]
b = [4, 5, 6]
ab = a + b  # [1, 2, 3, 4, 5, 6]

# Il est possible d'ajouter un element à une liste de la façon suivante:
yet_another_list = ab + [7]  # [1, 2, 3, 4, 5, 6, 7]

# Pour savoir si un élèment est inclus dans une liste
# il faut utiliser le mot-clef ``in``
1 in yet_another_list   # => True


# Il est possible assigner les élèments d'une liste
# à des variables à l'aide de la syntaxe suivante
a, b, c = [1, 2, 3]     # a == 1, b == 2 et c == 3


# Un dictionnaire est un ensemble d'association clef -> valeur.
# Dans un certains sens, il est similaire à une liste, sauf que le plus souvent
# pour acceder aux valeur il faut passer par des chaines.
#
# Il est possible de créer un dictionnaire vide à l'aide de la syntaxe suivante
empty_dict = dict()
# Un dictionnaire pre-remplis peut-etre créer de la façon suivante:
filled_dict = {"one": 1, "two": 2, "three": 3}

# Pour acceder aux valeur utiliser la syntaxe ``some_dict[clef]``
filled_dict["one"]   # => 1
# un code équivalent:
key = 'one'
filled_dict[key]

# Pour verifier l'existence d'une clef il faut utiliser
# le mot-clef ``in``
"one" in filled_dict  # => True
1 in filled_dict  # => False

# Acceder à une clef qui n'existe pas va lever une erreur
# dite "KeyError"
filled_dict["four"]
# Traceback (most recent call last):
#   File "<stdin>", line 1, in <module>
# KeyError: 'four'

# Il est possible de supprimer une entrée dans le dictionnaire
# à l'aide de la syntaxe suivante
del filled_dict["one"]


# Un ensemble peux-etre créer à l'aide du code suivant:
empty_set = set()
# Pour créer un ensemble pré-remplit, le code suivant est suffisant:
some_set = {1, 1, 2, 2, 3, 4}
# un ensemble contiens chaque valeur une fois
some_set == {1, 2, 3, 4}  # => True

# Pour connaitre l'intersection entre deux ensembles,
# l'opérateur esperluete ``&`` peut etre utiliser
other_set = {3, 4, 5, 6}
some_set & other_set   # => {3, 4}

# Pour réaliser l'opération d'union il faut utiliser
# L'opérateur trait vertical ``|``
some_set | other_set   # => {1, 2, 3, 4, 5, 6}

# Pour réaliser l'opération de différence, il faut utiliser
# l'opérateur moins ``-``
{1, 2, 3, 4} - {2, 3, 5, 7}   # => {1, 4, 7}

# Le mot-clef ``in`` permet de savoir si un élèment est dans
# un ensemble
2 in some_set   # => True
10 in some_set   # => False

# Il est aussi possible de verifier l'existence d'un objet
# dans une liste a l'aide du meme operateur ``in``
2 in [1, 2, 3]
2 in [4, 5, 6]

# Enfin...
# None, 0, les chaines vides, les listes vides et les dictionnaires vides
# et les ensembles vides sont considérés comme ayant une valeur ``False``
bool(0)  # => False
bool("")  # => False
bool([])  # => False
bool({})  # => False

# Toutes les autres valeurs sont considérées comme équivalentes à ``True``
```

Il y a plein de ressources en français pour apprendre le Python. Voici
une liste qui peux aider:

- [Débuter avec Python au lycée](http://python.lycee.free.fr/)

- [Introduction à Python 3](http://perso.limsi.fr/pointal/python:courspython3) sans oublier [le mémento](http://perso.limsi.fr/pointal/python:memento) qui va avec

Maintenant quelques exercices:

- Etant donnée un livre qui a 250 pages, 60 lignes par page et 15 mots
  par ligne en moyenne. Combien de mot y a t-il a peu pres dans le
  livre?

- Etant donnee la phrase "Quelle belle arbre" ainsi que "Quelle belle
  fleur", calculer le nombre de mots qui apparaissent dans les deux
  phrases.

- On considère deux dictionnaires, le premier est former par
  l'association des chiffres de 0 a 9 avec leur écriture en francais,
  le second est former par les chiffres de 0 a 9 en francais associés
  aux nombres de 0 a 9 en anglais. Mettez en place une suite
  d'operation qui permet de retrouver l'ecriture d'un nombre en
  anglais a partir d'un chiffre.

Good luck!
