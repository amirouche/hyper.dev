# 2018/09/24 - Comment on justifie un ORM ?

Reponse a l'article de Sam [Les critiques des ORM sont à côté de la
plaque](http://sametmax.com/les-critiques-des-orm-sont-a-cote-de-la-plaque/).

Ma position actuel est que les ORM c'est inutile voir dangereux par
rapport a l'utilisation de SQL. Et que cela ne scale pas du tout au
gros projet qui doivent etre maintenable et performant.

Mais d'abord faisont une etude du texte originale.

# Etude de la plaque

> Rappel: qu’est-ce qu’un ORM ?

Dans cette partie Sam essaye d'expliquer ce qu'est un ORM.
Il oublie que le principale ORM Python, l'ORM de Django
fait un pot pourrit de differents patrons:

- Object-Relational Mapper a proprement dit qui fait le lien
  entre la base de donnee et le code Python. A vrai dire, dans
  l'usage, c'est surtout le code Python qui indique a la base
  quelle table, quelle colonne avec un type.

- Observable: le model Django a des methodes qui sont appellees au
  cours du cycle de vie du modele qui permettent en pratique de
  modifier le model pour une raison x ou y. On verra plus tard que
  c'est pas utile, pire c'est dangeureux.

- Validation: Et oui, il y a une petite astuce, c'est que le ~form~,
  je veux dire le model sait se valider mais juste un peu pas trop,
  car sinon les `Form` il saurait pas quoi faire.

- Facade: il abstrait le langage de requete SQL a travers le tandem
  `QuerySet` et bien sur son manager.

Aussi, ce qu'on appelle vulgairement un ORM, gere les migrations
automagiquement.

> Tout est ecrit en Python

Je suis completement d'accord avec cette idee. Je veux ecrire un
maximum de code en Python. Mais je suis oblige de reconnaitre que ce
qu'on appelle ORM apporte plus de probleme que de solution.

> SQLAlchemy (pour les gros projets)

Voila un petit commentaire facile qui moutonne encore un peu plus le
public. Mon adage prefere c'est les problemes simples doivent etre
simple a resoudre et les problemes compliques possible. Ce qui n'est
pas le cas de SQAlechemy la derniere fois que je l'ai utilise. En
effet, le cout de mise en place fait que vous voulez pas utiliser cela
dans un petit projet. Une API qui part dans tous les sens fait que
vous vous y retrouvez jamais ni dans la documentation, ni dans les
blogs qui ventent ses merites.

> Que reproche-t-on aux ORM ?

Je suis d'accord avec les elements de reponses apportes par Sam dans
cette section.

> Heu?

Demarre la critique qui visent a convaincre que les ORM c'est bien.

L'argumentation est mal construire a mon sens mais les arguments sont
interessants.

> Les ORM ne servent pas à éviter d’écrire du SQL. Ça, c’est vaguement
> un effet de bord.

Malheureusement, c'est comme cela comme presente au premier abord les
ORM. Et c'est principalement pour cela qu'on les utilisent. C'est
une tentative de moutonage.

> Ils servent à créer une API unifiée inspectable, une expérience
> homogène, un point d’entrée unique, un socle de référence explicite
> et central, pour le modèle de données.

L'abstraction universelle en un seul mot pour gerer vos data.

Prenons un part un les arguments:

- API unifiée: entre plusieurs bases de donnee, mais comme il en parle
  pas plus les gens ne saurons pas que personne ou presque n'utilise
  cette fonctionalite des ORM qui permet de passer d'une base a une
  autre avec moins de douleurs. D'ailleurs, il ecrit plus tot que SQL
  fait deja le taf de ce point de vue la...

- inspectable: je ne connais pas mysql, mais postgresql est completement
  inspectable en SQL.

- une experience homogene: il repete le premier argument

- un point d'entree unique, un socle de référence explicite et
  central, pour le modèle de données: Ici, il dit deux fois la meme
  chose et glisse un mot de passe python bien connu "explicite". En
  quoi le SQL n'est pas explicite? En quoi le fichier de schema n'est
  pas un point d'entree unique? Au contraire avec cette abstraction on
  a l'information duplique dans le code Python et dans la base.

> Une fois qu’on a passé pas mal de temps à faire des projets...

Ici il met un coup de guitare a la Django. DRY. Application
re-utilisables.

> quelqu’un dans l’équipe va commencer à écrire une abstraction...

C'est ca le truc, l'abstraction, selon moi dont on a besoin est
tellement simple quelle defit le sens commun.

Pas besoin d'abstraction complique.

*On separe la vue du model ainsi que le controller. On valide les
entrees dans le controller. On decrit l'acces au model a l'aide du SQL
dans une petite fonction ou methode.*

Et voila!

> L’exemple de Django

Apres Sam va continuer a justifier l'interet d'un ORM parce que Django
c'est bien! Donc l'argument c'est Django == bien donc ORM ==
bien. Wat!  Un coup de moutonage au passage, il y a plein de projet
Django donc c'est bien Django.

Django et son ecosysteme merite un article a proprement parler.

C'est le moment ou je baisse les bras car l'article est mal construit.
Au lieu de faire une serie d'argument, couvrir l'argument completement
et donner un exemple. Ici, il repasse sur certains de ses arguments pour
faire semblant de les demonter, c'est rigolo.

# Pas d'ORM, c'est possible

Je vais pas vous moutoner en disant un truc du genre regardez comment
les autres font pour scaler leur Systeme d'Information. C'est uniquement
des indices. Et encore c'est parfois des fausses pistes.

Essayez de prendre du recule. Etudier votre code. Oubliez ce que vous
croyez savoir. Essayez de comprendre les difficultees liees a votre base
de code.  Tenez un journal des incidents et bugs. Essayez de faire des
rapprochements entre ces elements.

Vous arriverez a une meilleur solution qui resoud le probleme que vous
avez et pas celui que croyais avoir les developpeurs de Django.

Indice: quand on tourne toujours a gauche et qu'on se rend compte
qu'on tourne en rond. Qu'est ce qu'on doit faire?
