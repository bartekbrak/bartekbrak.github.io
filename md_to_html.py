#!/usr/bin/env -S uv run --script
# /// script
# dependencies = ["markdown"]
# ///

from argparse import ArgumentParser
from pathlib import Path

import markdown
from io import BytesIO


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
    output = Path(filename).with_suffix('.html').name
    template = Path('template_index' if output == 'index.html' else 'template').read_text()
    output = Path(output) if output == 'index.html' else Path('blog/archive') / output
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open('w') as f:
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
