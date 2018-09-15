#!/usr/bin/env python3
"""maji.

Usage:
  maji init
  maji make <base-url>
  maji render <template>
"""
import logging
import os
import sys
from pathlib import Path

import daiquiri
from docopt import docopt
from datetime import datetime
from datetime import timezone
from lxml.html import fromstring as string2html
from feedgen.feed import FeedGenerator

from jinja2 import Environment
from jinja2 import FileSystemLoader

import mistune
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import html


daiquiri.setup(logging.DEBUG, outputs=('stderr',))
log = daiquiri.getLogger(__name__)


class HighlightRenderer(mistune.Renderer):
    def block_code(self, code, lang):
        if not lang:
            out = '\n<div><pre>{}</pre></div>\n'
            return out.format(mistune.escape(code.strip()))
        lexer = get_lexer_by_name(lang, stripall=True)
        formatter = html.HtmlFormatter()
        return highlight(code, lexer, formatter)


renderer = HighlightRenderer()
markdown = mistune.Markdown(renderer=renderer)


def jinja(template, templates, **context):
    templates = os.path.abspath(templates)
    env = Environment(loader=FileSystemLoader((templates,)))
    template = env.get_template(template)
    out = template.render(**context)
    return out


# make

def make(root, base):
    root = Path(root)
    log.info('getting started at: %s', root)
    blog = root / 'blog'
    paths = blog.glob('*.md')
    posts = []
    for path in paths:
        log.info('markdown: %r', path)
        with path.open('r') as f:
            body = f.read()
        body = markdown(body)
        html = '<div>{}</div>'.format(body)
        div = string2html(html)
        try:
            title = div.xpath('h1/text()')[0]
        except IndexError:
            msg = "Seems like there is not title in: %s"
            log.critical(msg, path)
            sys.exit(1)
        log.debug('title is: %s', title)
        date = title[:len('2017/03/01')]
        date = datetime.strptime(date, '%Y/%m/%d')
        date = date.replace(tzinfo=timezone.utc)
        log.debug('publication date is: %s', date)
        post = {
            'title': title,
            'date': date,
            'html': html,
            'path': path,
        }
        log.debug('rendering blog post')
        page = jinja('post.jinja2', os.getcwd(), base=base, **post)
        filename = path.name.split('.')
        filename[-1] = 'html'
        filename = '.'.join(filename)
        post['filename'] = filename
        output = path.parent / filename
        with output.open('w') as f:
            f.write(page)
        log.debug('wrote: %s', output)
        posts.append(post)
    posts.sort(key=lambda x: x['date'], reverse=True)
    # populate feed
    output = root / 'feed.xml'
    log.info('generating feed at: %s', output)
    feed = FeedGenerator()
    feed.id(base)
    feed.title('hyperdev.fr')
    feed.subtitle('forward and beyond')
    feed.link(href=base + '/feed.xml', rel='self')
    for post in posts:
        entry = feed.add_entry()
        url = base + '/blog/' + post['filename']
        entry.id(url)
        entry.title(post['title'])
        entry.link(href=url)
        entry.published(post['date'].isoformat())
    feed.rss_file(str(output))
    log.info('rendering index')
    page = jinja('index.jinja2', os.getcwd(), base=base, posts=posts)
    output = Path(os.getcwd()) / 'index.html'
    with output.open('w') as f:
        f.write(page)


def main():
    args = docopt(__doc__, version='maji 0.1')
    if args.get('init'):
        raise NotImplementedError()
    elif args.get('make'):
        base = args['<base-url>']
        make(os.getcwd(), base)
    elif args.get('render'):
        # render markdown to html
        content = markdown(sys.stdin.read())
        # render template with `content`
        template = args['<template>']
        templates = os.path.abspath(template)
        templates = os.path.dirname(templates)
        out = jinja(template, templates, content=content)
        print(out)


if __name__ == '__main__':
    main()
