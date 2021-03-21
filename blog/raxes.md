# 2021/01/12 - raxes: review & rework of searx

[searx](https://github.com/searx/searx) is privacy-respecting
metasearch engine. It is search engine that does not have its own
index, but rely on other search engines to deliver its results. It
rely on Flask, requests and lxml.

## Review

According to the Makefile, the entry point of the web application, is
./searx/webapp.py. The main problem with searx is that it is not easy
to use it as library.

Looking up @app.route yield only 13 routes/

Let's look through each from least interesting to the most clever,
that is approximately a bottom-up read.

### `/translations.js`

There is two small issues with this code:

1. It is easier to debug code when return is followed by a simple variable e.g.
return foobar. Here things are made worse, because the returned value span
multiple lines.

2. the return is multiple line statement. That requires to zigzag the code.
Instead of reading top-down left-right you need to zigzag and reconfigure your
brain to also do read down-top (and even right-left in more problematic
cases).

### `/config`

The use of underscores _ in variable names is odd. In this case, it is
a way to avoid to think and overload the reader with useless and
poorly named variables names. I do that a lot with Scheme, but with
Scheme you can use more readable and better looking characters for
naming variables. underscore is difficult to read, and sometime it
disappears because of poor resolution or image scaling. The following
code:

```python
_engines = []
for name, engine in engines.items():
    something = process(name, engine)
    _engines.append(something)
```

Can be reworked into a list comprehension:

```python
engines = [process(name, engine) for (name, engine) in engines.items()]
```

That much more obvious that one can use a list comprehension instead
of the following code:

```python
_plugins = []
for _ in plugins:
    _plugins.append({'name': _.name, 'enabled': _.default_on})
```

Mind the use of `_` as variable name. When used as variable name
placeholder, `_` should not be accessed. It would be trivial to
replace `_` with item and bundle it inside a list comprehension.

### `/favicon.ico`

That is a complex one-liner:

```python
@app.route('/favicon.ico') def favicon():
    return send_from_directory(
        os.path.join(app.root_path, static_path, 'themes', get_current_theme_name(), 'img'),
        'favicon.png',
        mimetype='image/vnd.microsoft.icon'
    )
```

I will not repeat that multi-line return statements are difficult to read.

In that case, the code is trivial enough, but nesting calls is a evil habit.

Things like:

```python
out = qwe(asd(zxc(iop)), jkl(bnm))
```

Are not only difficult to read (even with normal variable names) but
also more complex to debug, because the intermediate result does
not get their own variable.

### `/opensearch.xml`

That is nice code. I like the following pattern that is used twice in
that function:

```python
out = default_value if not nominal: out = something
```

It is odd to see the HTTP method spelled lower case but that might be
something specific to opensearch. Otherwise I try to avoid shortcut
variables names in that function ret and response could both be
renamed out since it is the output of the function.

### `/robots.txt`

Not very interesting, except maybe it would be easier to create a
global constant (and in some case, but prolly not here, use an
external text file).

### `/stats/errors`

Again, factoring the body of the for and using a list comprehension
could be nice.

The following code:

```python
foobar = list(something.keys()) foobar.sort()
```

That is equivalent to:

```python
foobar = sorted(something.keys())
```

When you use the key keyword argument in list.sort, sorted or others,
you might want to rely on the standard library
[operators](https://docs.python.org/3/library/operator.html#mapping-operators-
to-functions).

### `/stats`

Nothing interesting to say about this function.

### `/image_proxy`

The following code:

```python
headers = dict_subset(request.headers, {'If-Modified-Since', 'If-None-Match'})
```

Can be rewritten to be more readable with a **single-line** dictionary
comprehension:

```python
headers = {key: headers[key] for key in headers if key in ['foo', 'bar']}
```

I still do not understand why everybody use the variable name logger.

The following:

```python
counter = 0 for item in foobar: counter += 1 do_something(counter, item)
```

Can be rewritten:

```python
for counter, item in enumrate(foobar): do_something(counter, item)
```

enumerate is builtin function, hence always available.

### `/preferences`

I will not repeat what I already wrote about comprehensions. There is good
pattern in there. But the last line of the function kills everything.

### `/autocompleter`

An idea here about how to avoid to use a class and sadly hide the
interesting logic away from the where the action happens:

RawTextQuery return an object with a public interface that has 4 methods
include some that have side-effects like the following call to changeQuery:

```python
for result in raw_results:
    raw_text_query.changeQuery(result) # add parsed result
    results.append(raw_text_query.getFullQuery())
```

That is necessarily a side-effect because it does not assign a
variable otherwise it would be dead-code. Here raw_text_query is
mutated, mutable objects are difficult to debug.

Following the spirit of the code, the function searx_bang could be a
method of RawTextQuery especially since it is used only once in the
whole code base.

Anyway the full function could rewritten as follow:

```python
def autocompleter():
    """Return autocompleter results"""
    query = request.form.get('q', '')
    try:
        query, parts, languages, specific = query_parse(query)
    except BadQuery:
        return '', 400

    # parse searx specific autocompleter results like !bang
    hits = searx_bang(query, parts, languages, specific)

    backend_name = request.preferences.get_value('autocomplete')
    try:
        completer = autocomplete_backends[backend_name]
    except KeyError:
        pass
    else:
        if not hits and (len(parts) > 1 or (len(languages) == 0 and not specific)):
            # get language from cookie
            language = request.preferences.get_value('language')
            language = language.split('-')[0] if (language or language == 'all') else 'en'
            # run autocompletion
            more = completer(query, language)
            hits += more

    # parse results (write :language and !engine back to result string)
    hits = [do_something(hit) for hit in hits]

    response = hits_to_response(request, hits)
    return reponse
```

Mind the fact:

1. I dropped the disabled_engine variable, because I am not sure where
it is useful.

2. It is not clear what happens in the last for loop especially with
the mutated raw query, so I replaced the whole thing with a
comprehension and factored the body in a function called do_something.

But that is not everything we can do. To make the project usable as a
library, it will be nice to extract the logic and keep environment
specifics in the flask view.

If you do it yourself, you might end up with something like that as
the view function autocompleter:

```python
@app.route('/autocompleter', methods=['GET', 'POST'])
def autocompleter():
    """Return autocompleter results"""
    query = request.form.get('q', '')

    if query.isspace():
        return 'thanks, but no thanks!', 400

    backend_name = request.preferences.get_value('autocomplete')
    language = request.preferences.get_value('language')
    language = language.split('-')[0] if (language or language == 'all') else 'en'

    try:
        hits = autocomplete(query, backend_name, language)
    except BadQuery:
        return 'invalid query because...', 400

    response = hits_to_response(request, hits)
    return reponse
```

### `/about`

It is a static page so not much to say, except the indentation is not
good.

### `/search`

That is the gist of the project. Here is the big problem: validation,
logic and rendering is mixed into a giant view function, factorization
was done, but there is room for more especially regarding the output
generation.

Here is the code that execute the meta search:

```python
# search
search_query = None
raw_text_query = None
result_container = None
try:
    search_query, raw_text_query, _, _ = get_search_query_from_webapp(request.preferences, request.form)
    # search = Search(search_query) #  without plugins
    search = SearchWithPlugins(search_query, request.user_plugins, request)
    result_container = search.search()
except SearxParameterException as e:
    logger.exception('search error: SearxParameterException')
    return index_error(output_format, e.message), 400
except Exception as e:
    logger.exception('search error')
    return index_error(output_format, gettext('search error')), 500
```

There is no point into defining as None the first three variables
since it is useless without an actual result, the code that follow
expect something that is not None.

Something that is always odd: multiples statements inside the try
block.

SearchWithPlugins is used only once in the whole code base and the
only public method is search. That begs to become a function, it will
make clear how do a search!

### How meta search works wit searx?

After jumping around definitions I end in the class Search at the method
search_multiple_requests:

```python
    def search_multiple_requests(self, requests):
        search_id = uuid4().__str__()

        for engine_name, query, request_params in requests:
            th = threading.Thread(
                target=processors[engine_name].search,
                args=(query, request_params, self.result_container, self.start_time, self.actual_timeout),
                name=search_id,
            )
            th._timeout = False
            th._engine_name = engine_name
            th.start()

        for th in threading.enumerate():
            if th.name == search_id:
                remaining_time = max(0.0, self.actual_timeout - (time() - self.start_time))
                th.join(remaining_time)
                if th.is_alive():
                    th._timeout = True
                    self.result_container.add_unresponsive_engine(th._engine_name, 'timeout')
                    logger.warning('engine timeout: {0}'.format(th._engine_name))

```

It does trigger simultaneously, using threads, a search query against
a search engine based on user preference and the last `for` block will
retrieve the result under a timeout. That is if a search engine does
not reply under less that some configured time, it is considered an
error.

The part that interest me is:

```
target=processors[engine_name].search,
```

After some jumping around, I find the mighty directory `searx/engines`
that contains all the logic to query and scrape results.

### Rework

This is a very quick rework of searx, it is very far from as feature
parity.

[forge](https://git.sr.ht/~amirouche/raxes).
