# 2021/01/09 - noontide: review & rework of loconotion

![locomotive](https://images.unsplash.com/photo-1598645259510-08d6b5ffd7ac?ixlib=rb-1.2.1&q=85&fm=jpg&crop=entropy&cs=srgb&w=1024)

[Loconotion](https://github.com/leoncvlt/loconotion/) is a python
program that allows to generate a static website from a
[notion.so](http://notion.so/) page.

## Review

Loconotion is a great tool to build a website from a notion page. The
only user experience problem is the absence of
[pypi.org](http://pypi.org/) package so that you can just `pip install`
loconotion and then call
loconotion to create a website. Another slight cognitive
overhead is the optional configuration file. It is optional, hence not
required, but FOMO...

Overall, the code is classic Python code: not evil, but not great either.
Let's dive in.

Here is the source code organization:

```
loconotion/
├── conditions.py (52 sloc)
├── __main__.py (128 sloc)
├── notionparser.py (467 sloc)
```

First thing I notice is that it looks small, sloccount reports 647
lines of code, so that could definitely be a single module file. Again
sloccount reports 128 lines in `__main__`. I recommend against having
code inside `__main__` and `__init__` outside imports or a trivial main
function, because I rarely see code in those files, which in turn
makes it difficult to remember to check that it is in fact trivial or
empty files, and check in particular that it does not contain import
time logic. Relying on code executing at import time is notoriously
evil as it breaks various tools e.g. pydoc. Not only it breaks
essential tooling, but because the code executes at import time,
depending on how imports happen, the code will execute in some order
instead of another without having touched the file where the code is,
making the behavior of an application or worse a library
unpredictable.

Executing code at import time is evil

I do not recommend Flask for that reason. The order of imports change the
order used to resolve URL into views which can break an application in
unpredictable ways.

Luckily, in the case of loconotion `__main__.py` contains only command
line interface logic, it is wrapped inside a function and only
executed when `__name__ == "__main__"`, so that is OK

Let's move to `loconotion/conditions.py`. It is a very tiny file with
52 lines of code. I do not create files before refactoring. Predicting
whether a file will be useful help for the reader is difficult to do
before the code is written. Also it is much easier to navigate a
single file than a directory and many small files. A file is not a
zero-cost abstraction in terms of cognitive load for the reader or the
writer (if there is such a thing such as "zero cognitive cost
abstraction"). The writer needs to figure a good name for the file,
and the reader must keep track of where objects definitions are
located with the supplementary vocabulary that was invented ad-hoc to
host in the case of `loconotion.conditions` two classes each of which
contains one method called... `__call__`! By the way, whether you use a
"code navigator" so called jump-to-definition or just a grep-like tool
does not matter: one file with only 600 lines will ALWAYS beat one
directory and three files.

YAGNI complex or clever hierarchy, that is premature optimization.

Further reading `loconotion.conditions`, the thing that strikes in
this particular case, but that dominates the world wide python
mainstream mind-share: `class`. You might disagree with me about the
broader Python ecosystem (this is not the last review!). So, let's
just focus on this case:

```python
class notion_page_loaded(object):
    """An expectation for checking that a notion page has loaded."""

    def __call__(self, driver):
        notion_presence = len(
            driver.find_elements_by_class_name("notion-presence-container")
        )
        if (notion_presence):
            unknown_blocks = len(driver.find_elements_by_class_name("notion-unknown-block"))
            loading_spinners = len(driver.find_elements_by_class_name("loading-spinner"))
            scrollers = driver.find_elements_by_class_name("notion-scroller")
            scrollers_with_children = [];
            for scroller in scrollers:
                children = len(scroller.find_elements_by_tag_name("div"))
                if children > 0:
                    scrollers_with_children.append(scroller)
            log.debug(
                f"Waiting for page content to load"
                f" (pending blocks: {unknown_blocks},"
                f" loading spinners: {loading_spinners},"
                f" loaded scrollers: {len(scrollers_with_children)} / {len(scrollers)})"
            )
            all_scrollers_loaded = len(scrollers) == len(scrollers_with_children)
            if (all_scrollers_loaded and not unknown_blocks and not loading_spinners):
                return True
            else:
                return False
        else:
            return False
```

What this function does *ahem* I mean to write `class` is: "check
whether a page is fully loaded" because notion will load lazily a page
and its content, so loconotion need the page to be fully loaded by the
headless browser (in the snippet, that is the variable `driver`),
before reading the complete html and writing it to a local
file. Something is strange. I mean, even if you do not know the
semantic of `SomeClass.__call__` a class that inherits nothing and has
a single method is "prolly evil".

My first take would be to replace this class with one or more function, it
does not loose generality or expressive power.

One thing that I do systematically: first return trivial cases, so that I do
not need to think about it while reading the rest of the code, for instance:

```python
if value:
    # ...
    # something something
    # ...
    return complexity
else:
    return triviality
```

The above is much more readable as follow:

```python
if not value:
    return triviality
# ...
# something something...
# ...
return complexity
```

Do not be fooled by the `not` operator, it does not matter whether the
predicate is "reversed", deal with simple cases first. Also, it saves
a level of indentation.

The following:

```python
if whatever:
    return True
else: return False
```

If you really need a boolean, it is equivalent to:

```python
return not not whatever
```

All things considered, the following is fine:

```python
return whatever
```

In the second class from the same file
[condition.py](http://condition.py/) there is constructor method
`__init__` which might trick you into thinking that class is
useful. Think twice! The class `toggle_block_has_opened` (verbatim
snake case), can be rewritten as follow:

```python
def toggle_block_has_opened(driver, toggle_block):
    # ...
    # something...
    # ...
```

About `loconotion/notionparser.py`:

- There is single class that is around 600 lines,
- The name of the class is Parser but it does much more,
- Too much indentation, that can be reduced with the previous trick where first
the code deal with simple cases,
- Scraping the page which includes loading the complete page should be separated
into different functions to make it more testable,
- Recursion is not pythonic.
- There is several small nitpicks to do about e.g. multi-line assignments to
multiple variables, and in general multi-line statements: that hurts
readability.

The code is well documented and it is easy to figure what happens. Also, it
does the job!

## Rework

It is not a drop-in replacement for loconotion, and does not support the same
features.

- It 280 lines of code
- It use lxml and xpath instead of beautiful soup
- It use httpx instead of requests
- It use pyppeteer instead of selenium
- There is no configuration file
- There is no "nice urls" and some urls are definitly ugly e.g. a page
inside a table.

It took me 8 hours

I do not believe the code is perfect, but that is a code base I can
work with.  There is one thing to change to make really testable: move
the code fetching the page outside crawl function. It is not perfect,
but that is what I used to use to render this website

The only feature I miss is a feed :)

[noontide forge](https://github.com/amirouche/python-noontide).
