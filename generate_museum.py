#!/usr/bin/env python3

from datetime import date
from html import escape
from pathlib import Path
import re

import yaml
from PIL import Image


ROOT = Path(__file__).resolve().parent
DATA_FILE = ROOT / "muzeum-włazów-kanalizacyjnych.yaml"
HTML_FILE = ROOT / "muzeum-włazów-kanalizacyjnych.html"
IMAGE_DIR = ROOT / "obrazy" / "muzeum-włazów-kanalizacyjnych"
IMAGE_URL_PREFIX = "obrazy/muzeum-włazów-kanalizacyjnych/"
THUMBNAIL_DIR = IMAGE_DIR / "thumbnails"
THUMBNAIL_URL_PREFIX = f"{IMAGE_URL_PREFIX}thumbnails/"
THUMBNAIL_MAX_SIZE = 800
THUMBNAIL_QUALITY = 75
START_MARKER = "      <!-- museum-gallery:start -->"
END_MARKER = "      <!-- museum-gallery:end -->"
REQUIRED_FIELDS = {
    "file",
    "title",
    "location",
    "date",
    "author",
    "width",
    "height",
    "alt",
}
OPTIONAL_FIELDS = {"description"}
FILENAME_PATTERN = re.compile(r"^(\d{8})_\d{2}(?:_[a-ząćęłńóśźż]+)?\.webp$")


def fail(message):
    raise SystemExit(f"Błąd: {message}")


def load_exhibits():
    try:
        exhibits = yaml.safe_load(DATA_FILE.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as error:
        fail(f"nie można odczytać {DATA_FILE.name}: {error}")

    if not isinstance(exhibits, list) or not exhibits:
        fail(f"{DATA_FILE.name} musi zawierać niepustą listę eksponatów")

    seen_files = set()
    for index, exhibit in enumerate(exhibits, start=1):
        if not isinstance(exhibit, dict):
            fail(f"wpis {index} nie jest mapą YAML")

        missing = REQUIRED_FIELDS - exhibit.keys()
        unknown = exhibit.keys() - REQUIRED_FIELDS - OPTIONAL_FIELDS
        if missing:
            fail(f"wpis {index} nie ma pól: {', '.join(sorted(missing))}")
        if unknown:
            fail(f"wpis {index} ma nieznane pola: {', '.join(sorted(unknown))}")

        file = exhibit["file"]
        if not isinstance(file, str) or Path(file).is_absolute() or ".." in Path(file).parts:
            fail(f"wpis {index} ma nieprawidłową ścieżkę pliku: {file!r}")
        if file in seen_files:
            fail(f"plik {file} występuje więcej niż raz")
        seen_files.add(file)

        filename_match = FILENAME_PATTERN.fullmatch(Path(file).name)
        if not filename_match:
            fail(f"plik {file} nie pasuje do wzorca YYYYMMDD_NN[_location].webp")

        exhibit["date"] = str(exhibit["date"])
        try:
            parsed_date = date.fromisoformat(exhibit["date"])
        except ValueError:
            fail(f"wpis {file} ma nieprawidłową datę: {exhibit['date']!r}")
        if filename_match.group(1) != parsed_date.strftime("%Y%m%d"):
            fail(f"data wpisu {file} nie zgadza się z nazwą pliku")

        for field in ("title", "location", "author", "alt"):
            if not isinstance(exhibit[field], str) or not exhibit[field].strip():
                fail(f"wpis {file} ma puste lub nieprawidłowe pole {field}")

        if "description" in exhibit and (
            not isinstance(exhibit["description"], str)
            or not exhibit["description"].strip()
        ):
            fail(f"wpis {file} ma puste lub nieprawidłowe pole description")

        for field in ("width", "height"):
            value = exhibit[field]
            if not isinstance(value, int) or isinstance(value, bool) or value <= 0 or value > 2000:
                fail(f"wpis {file} ma nieprawidłowe pole {field}: {value!r}")

        image_path = IMAGE_DIR / file
        if not image_path.is_file():
            fail(f"nie istnieje obraz {image_path.relative_to(ROOT)}")
        try:
            with Image.open(image_path) as image:
                if image.format != "WEBP":
                    fail(f"obraz {file} nie jest plikiem WebP")
                if image.size != (exhibit["width"], exhibit["height"]):
                    fail(
                        f"wymiary obrazu {file} to {image.width} × {image.height}, "
                        f"a w YAML-u {exhibit['width']} × {exhibit['height']}"
                    )
        except OSError as error:
            fail(f"nie można odczytać obrazu {file}: {error}")

    return sorted(
        exhibits,
        key=lambda exhibit: (exhibit["date"], Path(exhibit["file"]).name),
        reverse=True,
    )


def generate_thumbnail(exhibit):
    source = IMAGE_DIR / exhibit["file"]
    thumbnail = THUMBNAIL_DIR / exhibit["file"]
    thumbnail.parent.mkdir(parents=True, exist_ok=True)

    if thumbnail.is_file() and thumbnail.stat().st_mtime_ns >= source.stat().st_mtime_ns:
        try:
            with Image.open(thumbnail) as image:
                if image.format == "WEBP" and max(image.size) <= THUMBNAIL_MAX_SIZE:
                    return image.size
        except OSError:
            pass

    try:
        with Image.open(source) as image:
            image.thumbnail(
                (THUMBNAIL_MAX_SIZE, THUMBNAIL_MAX_SIZE),
                Image.Resampling.LANCZOS,
            )
            image.save(
                thumbnail,
                format="WEBP",
                quality=THUMBNAIL_QUALITY,
                method=6,
            )
            return image.size
    except OSError as error:
        fail(f"nie można wygenerować miniatury dla {exhibit['file']}: {error}")


def photo_word(count):
    if count == 1:
        return "fotografia"
    if count % 10 in (2, 3, 4) and count % 100 not in (12, 13, 14):
        return "fotografie"
    return "fotografii"


def render_card(exhibit, number, first):
    file = escape(exhibit["file"], quote=True)
    author = escape(exhibit["author"], quote=True)
    location = escape(exhibit["location"], quote=True)
    image_url = f"{IMAGE_URL_PREFIX}{file}"
    thumbnail_url = f"{THUMBNAIL_URL_PREFIX}{file}"
    thumbnail_width, thumbnail_height = generate_thumbnail(exhibit)
    filename = escape(Path(exhibit["file"]).name)
    image_size = (IMAGE_DIR / exhibit["file"]).stat().st_size / 1_000_000
    loading = 'decoding="async" fetchpriority="high"' if first else 'loading="lazy" decoding="async"'
    display_date = exhibit["date"].replace("-", ".")
    description = exhibit.get("description", "")
    description_markup = (
        f'              <p class="description">{escape(description)}</p>'
        if description
        else ""
    )

    return "\n".join(
        (
            "        <li>",
            f'          <figure class="card" data-author="{author}" data-location="{location}">',
            f'            <button class="photo" type="button" data-lightbox-open data-image="{image_url}" data-title="{escape(exhibit["title"], quote=True)}" data-alt="{escape(exhibit["alt"], quote=True)}" data-author="{author}" data-location="{location}" data-date="{exhibit["date"]}" data-description="{escape(description, quote=True)}" aria-label="Powiększ zdjęcie: {escape(exhibit["title"], quote=True)}"><img src="{thumbnail_url}" width="{thumbnail_width}" height="{thumbnail_height}" alt="" {loading}></button>',
            "            <figcaption>",
            f'              <span class="number">Eksponat {number:03d}</span><h3>{escape(exhibit["title"])}</h3>',
            f'              <dl><div><dt>Miejsce</dt><dd>{escape(exhibit["location"])}</dd></div><div><dt>Data</dt><dd><time datetime="{exhibit["date"]}">{display_date}</time></dd></div><div><dt>Autor</dt><dd>{escape(exhibit["author"])}</dd></div><div><dt>Nazwa</dt><dd>{filename} ({image_size:.1f} MB)</dd></div><div><dt>Rozdzielczość</dt><dd>{exhibit["width"]} × {exhibit["height"]} px</dd></div></dl>',
            description_markup,
            "            </figcaption>",
            "          </figure>",
            "        </li>",
        )
    )


def render_gallery(exhibits):
    count = len(exhibits)
    authors = sorted({exhibit["author"] for exhibit in exhibits}, key=str.casefold)
    locations = sorted({exhibit["location"] for exhibit in exhibits}, key=str.casefold)
    cards = [
        render_card(exhibit, count - index, index == 0)
        for index, exhibit in enumerate(exhibits)
    ]
    author_filters = [
        '          <button type="button" data-filter-kind="author" data-filter-value="" aria-pressed="true">Wszyscy</button>'
    ] + [
        f'          <button type="button" data-filter-kind="author" data-filter-value="{escape(author, quote=True)}" data-author="{escape(author, quote=True)}" aria-pressed="false">{escape(author)}</button>'
        for author in authors
    ]
    location_filters = [
        '          <button type="button" data-filter-kind="location" data-filter-value="" aria-pressed="true">Wszystkie</button>'
    ] + [
        f'          <button type="button" data-filter-kind="location" data-filter-value="{escape(location, quote=True)}" aria-pressed="false">{escape(location)}</button>'
        for location in locations
    ]
    return "\n".join(
        (
            '      <section class="filters" aria-label="Filtruj eksponaty">',
            '        <div class="filter-row" role="group" aria-label="Filtruj według autora">',
            '          <span class="filter-label">Autor</span>',
            *author_filters,
            "        </div>",
            '        <div class="filter-row" role="group" aria-label="Filtruj według lokalizacji">',
            '          <span class="filter-label">Lokalizacja</span>',
            *location_filters,
            "        </div>",
            "      </section>",
            '      <div class="collection-bar">',
            f'        <h2 class="collection-heading" aria-live="polite">{count} {photo_word(count)} / od najnowszych</h2>',
            "        <p>Wybierz zdjęcie, aby je powiększyć.</p>",
            "      </div>",
            "      <!-- Ta sekcja jest generowana z muzeum-włazów-kanalizacyjnych.yaml. -->",
            '      <ol class="gallery">',
            *cards,
            "      </ol>",
        )
    )


def update_html(gallery):
    html = HTML_FILE.read_text(encoding="utf-8")
    if html.count(START_MARKER) != 1 or html.count(END_MARKER) != 1:
        fail(f"{HTML_FILE.name} musi zawierać dokładnie jedną parę znaczników generatora")

    before, remainder = html.split(START_MARKER, 1)
    _, after = remainder.split(END_MARKER, 1)
    generated = f"{before}{START_MARKER}\n{gallery}\n{END_MARKER}{after}"
    HTML_FILE.write_text(generated, encoding="utf-8")


if __name__ == "__main__":
    exhibits = load_exhibits()
    update_html(render_gallery(exhibits))
    print(f"Wygenerowano {len(exhibits)} eksponatów w {HTML_FILE.name}")
