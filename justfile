default:
    @just --list

# Render Markdown pages and stage the sources and generated HTML.
compile:
    find md -name '*.md' -print0 | xargs -0 -r uv run --script md_to_html.py
    git add -- '*.html'
    find md -name '*.md' -print0 | xargs -0 -r git add --

# Recompile whenever Markdown files are modified or created (requires inotifywait).
watch:
    while true; do inotifywait -qq -r -e modify,create md && just compile; done
