# 2015/01/01 - Python: subscript rencontre un générateur

Python a un certains nombre de méthodes dites «magiques», notamment
__getitem__. C'est la méthode qui est appellé lorsque on fait quelque
chose comme make[some_fun], c'est l'opérateur «subscript».

Voyons voir:

```
class SubScript:

    def __getitem__(self, value):
        return 'value est %s' % str(value)


subscript = SubScript()
print(subscript[42])  # value est 42

# mais aussi
print(subscript[42:52])  # value est slice(42, 52, None)

# et encore
print(subscript[42:52:102])  # value est slice(42, 52, 102)
```

Vous allez me dire mais à quoi ça sert? Et bien c'est simple:
implémenter une classe qui ressemble à une liste. Comme range en
Python 3, qui est générateur qui accepte de se faire découper
[to slice].

Le code suivant montre comment crée ce type de générateur:

```
class SubscriptableGenerator:

    def __init__(self, n=None, slice=None):
        self.n = n
        self.slice = slice

    def __getitem__(self, i):
        if isinstance(i, slice):
            return GeneratorSubscriptable(None, i)
        else:
            return self._compute_fibonacci(i)

    def __iter__(self):
        if self.slice:
            if self.slice.step:
                step = self.slice.step
            else:
                step = 1
            n = step
            while n <= self.slice.stop:
                yield self._compute_fibonacci(n)
                n += step
        else:
            n = 0
            while n <= self.n:
                yield self._compute_fibonacci(n)
                n += 1

    def _compute_fibonacci(self, n):
        if n == 0:
            return 0
        elif n == 1:
            return 1
        else:
            a = self._compute_fibonacci(n-1)
            b = self._compute_fibonacci(n-2)
            return a + b

fibo15 = SubscriptableGenerator(15)

print(list(fibo15))

print(fibo15[5])

print(list(fibo15[0:10]))

print(list(fibo15[0:10:2]))
```

Cette construction me laisse bouche béh (!) mais je sais pas trop à
quoi cela pourrait servir.
