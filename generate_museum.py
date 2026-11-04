#!/usr/bin/env python3

from datetime import date
from html import escape
import hashlib
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
LOCATION_PALETTE = (
    ("#d94841", "#fde2e1"),
    ("#2f6fdb", "#dce9ff"),
    ("#2d8a57", "#dff5e8"),
    ("#9b4dca", "#f0defb"),
    ("#d97706", "#ffebc7"),
    ("#00838f", "#d9f4f5"),
    ("#c026d3", "#f8ddfb"),
    ("#4d7c0f", "#e8f5d0"),
    ("#b45309", "#ffedd5"),
    ("#0369a1", "#e0f2fe"),
    ("#be123c", "#ffe4e6"),
    ("#4338ca", "#e0e7ff"),
)
START_MARKER = "      <!-- museum-gallery:start -->"
END_MARKER = "      <!-- museum-gallery:end -->"
REQUIRED_FIELDS = {
    "file",
    "number",
    "title",
    "location",
    "date",
    "author",
    "text",
    "width",
    "height",
}
OPTIONAL_FIELDS = {"description"}
FILENAME_PATTERN = re.compile(
    r"^(\d{8})_\d{2}(?:_[a-ząćęłńóśźż]+(?:_[a-ząćęłńóśźż]+)*)?\.webp$"
)


def fail(message):
    raise SystemExit(f"Błąd: {message}")


def location_colors(location):
    digest = hashlib.sha256(location.encode("utf-8")).digest()
    return LOCATION_PALETTE[digest[0] % len(LOCATION_PALETTE)]


def load_exhibits():
    try:
        exhibits = yaml.safe_load(DATA_FILE.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as error:
        fail(f"nie można odczytać {DATA_FILE.name}: {error}")

    if not isinstance(exhibits, list) or not exhibits:
        fail(f"{DATA_FILE.name} musi zawierać niepustą listę eksponatów")

    seen_files = set()
    seen_numbers = set()
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

        number = exhibit["number"]
        if (
            not isinstance(number, str)
            or not re.fullmatch(r"\d{3}", number)
            or number == "000"
        ):
            fail(f"wpis {file} ma nieprawidłowy numer eksponatu: {number!r}")
        if number in seen_numbers:
            fail(f"numer eksponatu {number} występuje więcej niż raz")
        seen_numbers.add(number)

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

        for field in ("title", "location", "author", "text"):
            if not isinstance(exhibit[field], str):
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
        key=lambda exhibit: (int(exhibit["number"]), exhibit["date"]),
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


def render_card(exhibit, first):
    file = escape(exhibit["file"], quote=True)
    number = escape(exhibit["number"], quote=True)
    author = escape(exhibit["author"], quote=True)
    location = escape(exhibit["location"], quote=True)
    location_color, location_pastel = location_colors(exhibit["location"])
    location_style = (
        f'style="--location-color: {location_color}; '
        f'--location-pastel: {location_pastel};"'
    )
    image_url = f"{IMAGE_URL_PREFIX}{file}"
    thumbnail_url = f"{THUMBNAIL_URL_PREFIX}{file}"
    thumbnail_width, thumbnail_height = generate_thumbnail(exhibit)
    filename = escape(Path(exhibit["file"]).name)
    image_size = (IMAGE_DIR / exhibit["file"]).stat().st_size / 1_000_000
    loading = 'decoding="async" fetchpriority="high"' if first else 'loading="lazy" decoding="async"'
    display_date = exhibit["date"].replace("-", ".")
    description = exhibit.get("description", "")
    text = exhibit["text"]
    text_preview = text if len(text) <= 150 else f"{text[:150].rstrip()}…"
    text_markup = (
        f'              <p class="text" title="{escape(text, quote=True)}">{escape(text_preview)}</p>'
        if text
        else ""
    )
    description_markup = (
        f'              <p class="description">{escape(description)}</p>'
        if description
        else ""
    )

    return "\n".join(
        (
            "        <li>",
            f'          <figure class="card" data-author="{author}" data-location="{location}" {location_style}>',
            f'            <button class="photo" type="button" data-lightbox-open data-image="{image_url}" data-title="{escape(exhibit["title"], quote=True)}" data-number="{number}" data-author="{author}" data-location="{location}" data-date="{exhibit["date"]}" data-text="{escape(text, quote=True)}" data-description="{escape(description, quote=True)}" aria-label="Powiększ zdjęcie: eksponat {number}"><img src="{thumbnail_url}" width="{thumbnail_width}" height="{thumbnail_height}" {loading}></button>',
            "            <figcaption>",
            f'              <span class="number">Eksponat {number}</span><h3>{escape(exhibit["title"])}</h3>',
            f'              <dl><div><dt>Miejsce</dt><dd>{escape(exhibit["location"])}</dd></div><div><dt>Data</dt><dd><time datetime="{exhibit["date"]}">{display_date}</time></dd></div><div><dt>Autor</dt><dd>{escape(exhibit["author"])}</dd></div><div><dt>Plik</dt><dd>{filename}</dd></div><div><dt>Rozmiar</dt><dd>{image_size:.1f} MB</dd></div><div><dt>Rozdzielczość</dt><dd>{exhibit["width"]} × {exhibit["height"]} px</dd></div></dl>',
            text_markup,
            description_markup,
            "            </figcaption>",
            "          </figure>",
            "        </li>",
        )
    )


def render_gallery(exhibits):
    count = len(exhibits)
    from collections import Counter

    author_counts = Counter(exhibit["author"] for exhibit in exhibits)
    location_counts = Counter(exhibit["location"] for exhibit in exhibits)
    authors = sorted(author_counts, key=lambda author: (-author_counts[author], author.casefold()))
    locations = sorted(
        location_counts,
        key=lambda location: (-location_counts[location], location.casefold()),
    )
    cards = [
        render_card(exhibit, index == 0)
        for index, exhibit in enumerate(exhibits)
    ]
    author_filters = [
        f'          <button type="button" data-filter-kind="author" data-filter-value="" aria-pressed="true">Wszyscy ({count})</button>'
    ] + [
        f'          <button type="button" data-filter-kind="author" data-filter-value="{escape(author, quote=True)}" data-author="{escape(author, quote=True)}" aria-pressed="false">{escape(author)} ({author_counts[author]})</button>'
        for author in authors
    ]
    location_filters = [
        f'          <button type="button" data-filter-kind="location" data-filter-value="" aria-pressed="true">Wszystkie ({count})</button>'
    ] + [
        f'          <button type="button" data-filter-kind="location" data-filter-value="{escape(location, quote=True)}" data-location="{escape(location, quote=True)}" style="--location-color: {location_colors(location)[0]}; --location-pastel: {location_colors(location)[1]};" aria-pressed="false">{escape(location)} ({location_counts[location]})</button>'
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
