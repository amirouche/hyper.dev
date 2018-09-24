# 2015/01/01 - Lazy will continue

Cette citation de Bob Marlisp est complètement à propos de
continuation de séquences paresseuses en scheme.

Dans cette article je vais presenter deux constructions:

1. Les séquences paresseuses similaires aux iterables comme xrange ou
   aux générateurs simples.

2. Les coroutines, l'équivalent des generateurs améliorés.

### Sequence paraisseuse


Une sequence est dites paresseuses, si elle ne calcule pas tous les
elements qui la compose à l'avance. L'interet est double, d'une part
on economise la memoire, d'autre part le calcul se fait en plusieurs
fois ce qui repartie la charge CPU dans le temps.

Il existe bien les streams scheme pour faire cela, seulement je veux
explorer ça.

Il existe une autre approche emprunté a clojure nommé lazy-seq. Je
n'est est pas besoin de la mise en cache des resultats (cela peux
consommer beaucoup de memoire (Surtout quand on a pas besoin de cette
memoization)).

La méthode simple est inspiré de lazy-seq, le principe est d'utiliser
une recurrence et une closure qui va retarder le calcul de la
prochaine valeur: Il aussi est possible d'implementer les sequences
paresseuses à l'aide de routines de controle du flow des programmes
comme yield en Python et call/cc en Scheme que j'essaye d'aborder dans
la seconde partie.

```scheme
(define multiples-of-three
  (let next ((n 3))
    (lambda ()
      (values n (next (+ n 3))))))
```

Ligne par ligne cela donne:

1. Definition d'une variable multiples-of-three qui va contenir la
   définition de la séquence.

2. La deuxieme ligne definie une lambda à l'aide de la forme let nommé
   qui encapsule le code de la séquence. Le let nommé est très utile
   pour définir des procédures recurrentes sans utiliser un autre
   define ou let plus lambda. Le let nommé est bien en dehors de la
   lambda definissant la séquence.

3. La lambda definissant le comportement de la séquence.

4. Elle retourne deux valeurs grace à values: la valeur courante n *et* à la lambda retourner par next, qui va permettre de continuer l'iteration.

La procédure multiples-of-three retourne toujours 3 et la lambda de la
deuxième iteration. Après le premier appel, elle n'est plus jamais
appellé. C'est la lambda qui définit la procédure qui est appellé mais
avec un contexte différent.

L'utilisation du let nommé complique les choses en un sens. Voici une
version qui ne l'utilise pas:

```scheme
(define (multiples-of-three-rec n)
  (values n (lambda () (multiple-of-three-rec (+ n 3)))))


(define (multiples-of-three)
  (multiples-of-three-rec 3))
```

Voici comment cela s'utilise:

```scheme
(use-modules (ice-9 receive))


(define multiples-of-three
  (let next ((n 3))
    (lambda ()
      (values n (next (+ n 3))))))


(receive (value next) (multiples-of-three)
  (format #t "~a\n" value)  ;; => 3
  (receive (value next) (next)
    (format #t "~a\n" value)  ;; => 6
    (receive (value next) (next)
      (format #t "~a\n" value))))  ;; => 9
```

On peux utiliser le même principe en Javascript ou Python. Dans le
code suivant je présente une implementation de multiples-of-three en
Javascript:

```javascript
function multiplesOfThree() {

    function next(n) {
	// wrap next call to delay its execution.
	function wrapper () {
	    return next(n + 3);
	};
	return {value: n, next:wrapper};
    }

    return next(3);
}

iter = multiplesOfThree()
console.log(iter)
iter = iter.next()
console.log(iter)
iter = iter.next()
console.log(iter)
```

Et en Python:

```python
def multiple_of_three():

    def next(n):
	return [n, lambda: next(n+3)]

    return next(3);

value, next = multiple_of_three()
print(value)
value, next = next()
print(value)
value, next = next()
print(value)
```

Remarque: les deux langages ont déjà un moyen beaucoup plus simple de
faire ce genre de chose à l'aide de leur yield respectif, exemple en
Python:

```python
def multiple_of_three():
    n = 3
    while True:
        yield n
        n += 3


generator = multiple_of_three()

print(generator.next())
print(generator.next())
print(generator.next())
```

En javascript, avec une version recente de node et le flag --harmony
cela donne:

```javascript
function* multiplesOfThree(){
    var n = 3;
    while (true) {
	yield n;
	n = n + 3;
    }
}


iterator = multiplesOfThree()

console.log(iterator.next())
console.log(iterator.next())
console.log(iterator.next())
```

Cette méthode resoud en scheme le problème de la construction de la
liste paresseuse de façon plus élégante. Ceci dit, il est encore
necessaire de construire des procedures map, fold, for-each, filter
spécifiques.

### Continuations

Au cours de mes lectures il m'a semblé que call-with-continuation
(call/cc pour les intimes) était la procedure (?) qui cristalise
l'identité minimaliste de scheme dans le sens où il s'agit d'une
construction très puissante et simple . Elle n'exsite pas ailleurs, on
lui préfére des constructions spécialisés comme yield ou goto. En
effet, call/cc peux emuler la plus part si ce n'est pas toutes les
constructions de controles. Le support de call/cc se fait au prix de
compilateurs/interpreteur plus compliqués.

Sans autres formes de procès voilà une procédure permettant
d'implementer des coroutines:

```scheme
(define (coroutine routine)
  (let ((current routine)
	(status 'new))
    (lambda* (#:optional value)
      (let ((continuation-and-value
	     (call/cc (lambda (return)
			(let ((returner
			       (lambda (value)
				 (call/cc (lambda (next)
					    (return (cons next value)))))))
			  (if (equal? status 'new)
			      (begin
				(set! status 'running)
				(current returner))
			      (current (cons value returner)))
			  (set! status 'dead))))))
	(if (pair? continuation-and-value)
	    (begin (set! current (car continuation-and-value))
		   (cdr continuation-and-value))
	    continuation-and-value)))))
```

Dans les grandes lignes, un appel call/cc va créer un "label"
dynamiquement referencé par la variable passé à la callback de
call/cc. La callback est appellé immediatement. Si l'envie lui prend
de "quitter/revenir" mais plus precisement the continuer sa vie avec
la continuation elle va l'appeller (avec un argument si sa lui
chante). Ce comportement de base est illustré dans le code suivant:

```scheme
(define why (call/cc (lambda (return)
		       (format #t "love me or leave me!")
		       (return "I leave!")
		       ;; the program never reach this part
		       (format #t "it probably left :("))))
(format #t "return actually populates WHY variable\n")
(format #t "WHY: ~a\n" why)
```

Avec cette exemple, on dirait que c'est rien de plus qu'un return. En
fait c'est bien plus que ça. La continuation est une variable et pas
un keyword, elle peux etre gardé en mémoire, passé à une autre
procedure. Elle est dynamique contrairement à goto, qui attend un
label qui peut-être resolue par le compilateur.

Mon implementation est loin d'être aussi facile à utiliser que le
yield Python. En effet chaque yield crée une nouvelle continuation et
donc un nouveau yield cf. second-yield:

```scheme
(define example-coroutine
  (coroutine (lambda (yield)
	       (display "coroutine says: HELLO!")
	       (newline)
	       (let ((second-yield (cdr (yield 1))))
		 (display "coroutine says: WORLD!")
		 (second-yield 2)
		 (newline)
		 (display "coroutine says: SORRY, I'M OUT")))))


(display (example-coroutine))
(newline)
(display (example-coroutine))
(newline)
```

Clairement cela necessite un peu plus de travail. J'ai tourné en rond
un certain temps pour résoudre le problème de la creation des yield
pour avoir une syntax moins imbriqué et plus lineaire.

Les *delimited continuations* et la procédure *amb* sont deux formes de
controles qui peuvent être implementé à l'aide de *call/cc*.
