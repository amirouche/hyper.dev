# 2019/02/01 - Comment choisir une base de donnee?

Pour choisir une base de donnee vous pouvez vous aidez de StackOverflow
et du tag [database-design](https://stackoverflow.com/questions/tagged/database-design).

Dans votre question il est preferable d'apporter des elements de
reponses en decrivant votre besoin:

1. Ganranties: Cela ce definit en remettant en question les differents
   proprietees ACID: Atomic, Consistent, Isolation, Durability. Voir
   la documentation PostgreSQL sur le [controle de la
   concurrence](https://www.postgresql.org/docs/9.1/transaction-iso.html)
   ou en autre le [le chapitre sur les transactions dans
   wiredtiger](http://source.wiredtiger.com/3.1.0/transactions.html).
   Voir si [BASE](https://en.wikipedia.org/wiki/Eventual_consistency)
   vous convient.
1. Taille
1. Modele de donnee : A quoi ressemble les donnees. Est ce qu'elles
   sont de formes heterogenes ou bien il y as des types bien
   identifies.
1. Workload : Surtout des read, surtout des write, melange ou encore
   write once, then read-only. Ainsi que les types de requetes qui
   vont etre executees: recursive / profondes, colonne / lignes ou par
   proximites.
