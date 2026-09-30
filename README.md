source code for http://bartekbrak.github.io

## Development

Install [uv](https://docs.astral.sh/uv/) and [just](https://just.systems/).
uv automatically installs the Python dependencies declared inline in `md_to_html.py`.

- `just` lists available recipes.
- `just compile` renders all files under `md/` and stages the Markdown sources and HTML output in Git.
- `just watch` recompiles on Markdown changes (requires `inotifywait` from `inotify-tools`).

`md/index.md` renders to `index.html` at the site root. All other pages render to
`blog/archive/`. Images remain in `images/` at the site root.

The homepage uses `template_index` and shows only a dot linking to the archive's
unlisted page. Other pages use `template`, which includes the contact email.

To render individual pages without staging them:

```sh
uv run --script md_to_html.py md/aboutme.md
```

## Manhole-cover museum

`muzeum-włazów-kanalizacyjnych.html` is a standalone, hand-edited HTML gallery at
the site root. Its CSS and small style-switching script are inline; it needs no
build step. Photos live in `obrazy/muzeum-włazów-kanalizacyjnych/`.

To add a photograph, copy a `<li>` in `.gallery`, update the image link and source,
dimensions, alt text, title, and caption metadata (including filename and size in
decimal MB), then update the photo count. Dates and locations currently come from
filenames; all photographs are credited to Bartek Brak.
The five style buttons at the bottom of the page remember the selection when
browser storage is available.
