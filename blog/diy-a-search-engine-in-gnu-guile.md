# 2017/02/01 - Do It Yourself: a search engine in Scheme Guile

Search engines are really funny beast they are a mix of algorithm,
architecture and other domain knowledge from databases, linguistic,
machine learning and graph theory.

I don't have the prentention to know all of those but with a help of
background knowledge, NLP coursera and another description of a search
engine I will try to buiolg ahem build and blog about a search engine
mocking the different parts and hopefully make a proper release at
some point.

### Taking orders from space

To get started let's focus and the high level view of the
problem. What we want is to be able to search for documents. There is
two tasks that must be tackled.

First is the task of return a ranked list of results for a given
query. A query is a set of words that we look in a database. We will
massively simplify the problem of matching a query to documents by
considering that a document is a match if every word from the query
appears in it. We will put aside the fact that they might be relevant
synonyms or that the query has typos.

The more times words from the query appear in a document higher the
score of the document.

The second task is the task of gathering and pre-processsing the
documents into the database.

### Puting ones and zeros together

The first task, querying, comes backward because in reality we must
first store the documents in the database otherwise there is nothing
to query. Building the query engine without having the datastructure
of the data written won't work.

That's why we will start with the second task of storing the data
inside wiredtiger tables and then implement the querying and then
ranking.

It can be built with a RDBMS database with or without LIKE but I don't
want to use a RDBMS. If you want you can follow using you prefered SQL
ninja foo but at least do not use LIKE to make the exercise more
interesting. In wiredtiger there is no LIKE, part of the task is to
implement it.

We will implement unit tests, but it's really nice to have a real
corpus to test the application. One good candidate are browser
bookmarks but html requires preprocessing and more code is required to
retrieve the documents... To cut the chase, we will use the bbc news
articles dataset as real corpus. You can use whatever plain text
documents you have. It's best to use a corpus you know well.

Before reading the solution, think a little while about how you would
implement it yourself. Read about wiredtiger (it's basically a
hashmap). Imagine a solution in some language whether it's diagrams,
scheme or another programming language.

### Turning plain text files to scheme data

#### Going through a set of files

First download the bbc dataset. Extract it somewhere, for instance in
~/src/guile/artafath. artafath means share the light, literaly ar is
give back and tafath is light so it reads literally give back the
light.

We need a procedure to iterate over all the files, we will use file
tree walk procedure to implement a (for-each-file directory extension
proc) procedure that will iterate over all files that have EXTENSION
as extension inside DIRECTORY and execute a procedure PROC which is
passed the path of a matching file:

```scheme
(define (for-each-file directory extension proc)
  (ftw directory (lambda (filename statinfo flag)
                   (match flag
                     ('regular (proc filename)
                                #true)
                     ('directory #true)))))
```

I choosed to do pattern matching.

for-each-file only excutes proc (just like for-each) and doesn't
return anything useful (like fold or map) so onward we will only think
in terms of file.

#### Naive parsing of text files

We could simply store the content of the file in a column associated
with its filename. The problem with that solution is that we can not
easily count the number of times a word appears in the text without
going through the text which has a algorithmic complexity of O(n)
instead we will convert the text into a sparse matrix counting the
number of times a word a appears in the text. We will call this sparse
matrix the bag of words or simply bag.

We must read the content of the file and turn it into a scheme string,
reading file as string is done with (ice-9 rdelim) module. For this
operation we can simply do:

```scheme
(define (file->string filepath)
  (call-with-input-file filepath read-string))
```

Save this procedure it's useful.

Now we need to 1) lowercase the string so that queries will be case
insensitive, words of the query will also be lower case. 2) turn the
string into token, which in this case means parsing words. We will
adopt a simple approach which works great, most of the time, for
english by removing punctuation and splitting by space 3) count the
words and store everything in an association.

Let's implement 1) and 2) in (string->tokens text) procedure:

```scheme
(use-modules (srfi srfi-26)) ;; for cut

(define punctuation (string->list "!\"#$%&\\'()*+,-./:;<=>?@[\\]^_`{|}~"))

(define (clean text)
  "Replace punctuation characters from TEXT with a space character"
  (string-map (lambda (char) (if (list-index punctuation char) #\space char)) text))

(define split (cut string-split <> #\space))

(define (sanitize words)
  "Only keep words that have length bigger than one"
  (filter (lambda (word) (< 1 (string-length word))) words))

;; compose must be read from right to left
(define string->tokens (compose sanitize split string-downcase clean))
```

srfi 26 provides the handy cut form.

The third steps is to build the bag of words, a mapping between a word
and the number of time it appears. It's a sparse vector. We use this
to 1) avoid to store all the text 2) we make the data more computer
friendly, kind of... 3) we pre-compute the values that we will need
later to match the query against the documents.

The following procedures takes an association BAG and increment a the
integer associated with WORD in a persistent way ie. without mutation,
it creates a new association (no exclamation mark ! as suffix):

```scheme
(define (bag-increment bag word)
  (let ((count (assoc-ref bag word)))
    (if count
        (let ((bag (alist-delete word bag)))
          (acons word (1+ count) bag))
        (acons word 1 bag))))
```

Now we will have to use recursive loop thanks to a named let to
iterate over the words to create the bag of words:

```scheme
(define (words->bag text)
  (let loop ((bag '())
             (text text))
    (if (null? text)
        bag
        (loop (bag-increment bag (car text)) (cdr text)))))
```

Check point. The following program:

```scheme
(define tokens (string->tokens "Janet eat a kiwi! A kiwi!"))
(pk (words->bag tokens))
```

Outputs the following:

```scheme
(("kiwi" . 2) ("eat" . 1) ("janet" . 1))
```

This must be turned into a unit test. Use this template to create one:

```scheme
(use-modules (srfi srfi-64)) ;; unit test framework

(use-modules (artafath))


(test-begin "artafath")

(test-group "string->tokens"
    (test-equal "integration" (string->tokens "Janet eat a kiwi! a kiwy!") '()))
(test-end "artafath")
```

Remains to store the data in wiredtiger and rank a query against the database.

DIY.
