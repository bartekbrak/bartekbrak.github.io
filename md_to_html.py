#!/usr/bin/env python3
from argparse import ArgumentParser

import markdown
from io import BytesIO

template = open('template').read()


def render(filename):
    body = BytesIO()
    markdown.markdownFromFile(
        input=filename,
        output=body, 
        output_format='html5',
        extensions=[
            # "markdown.extensions.def_list",
            "markdown.extensions.fenced_code",
            # "markdown.extensions.codehilite",
            # "markdown.extensions.tables",
            # "markdown.extensions.toc",
            # "fontawesome_markdown",
        ],
        extension_configs={
            # 'markdown.extensions.codehilite': {'css_class': 'highlight'},
            # 'markdown.extensions.extra': {},
            # 'markdown.extensions.meta': {},
            # 'markdown.extensions.toc': {'permalink': True},
        },
    )
    with open(filename.replace('.md', '.html').split('/')[-1], 'w') as f:
        f.write(template % dict(body=body.getvalue().decode("utf-8")))


def parse_args():
    parser = ArgumentParser(__doc__)
    parser.add_argument('filename', nargs='+')
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    for one_filename in args.filename:
        print('processing', one_filename)
        render(one_filename)
