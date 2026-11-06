default:
    @just --list

save:
    git pull
    -git commit . -m "$(date +%Y.%m.%d)" -e && git push

# Render Markdown pages and stage the sources and generated HTML.
compile:
    find md -name '*.md' -print0 | xargs -0 -r uv run --script md_to_html.py
    git add -- '*.html'
    find md -name '*.md' -print0 | xargs -0 -r git add --

# Generate the museum gallery from YAML data.
museum:
    uvx --from pyyaml --with pillow python generate_museum.py

# Serve the site locally so browser features such as cookies work.
serve port="8000":
    uv run python -m http.server {{port}} --bind 127.0.0.1

# Recompile whenever Markdown files are modified or created (requires inotifywait).
watch:
    while true; do inotifywait -qq -r -e modify,create md && just compile; done
