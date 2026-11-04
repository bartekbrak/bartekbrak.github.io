# Instrukcje dla agentów

## Typowe zadanie: dodanie zdjęcia do muzeum

Najczęstszym zadaniem w tym projekcie jest dodanie nowego zdjęcia do muzeum włazów kanalizacyjnych.

1. Ustal datę zdjęcia, autora i lokalizację. Jeśli lokalizacja jest znana, użyj jej także w nazwie pliku.
2. Nazwij plik według `naming_pattern.md`:
   `YYYYMMDD_NN[_location].webp`
   - `NN` to chronologiczny numer zdjęcia z danego dnia, zaczynający się od `01`.
   - Lokalizację zapisuj małymi literami, bez polskich znaków, a spacje zastępuj podkreśleniami.
3. Skonwertuj zdjęcie do WebP, zachowując proporcje, ograniczając dłuższy bok do 2000 px i używając jakości 85.
4. Umieść obraz w `obrazy/muzeum-włazów-kanalizacyjnych/`.
5. Dodaj wpis do `muzeum-włazów-kanalizacyjnych.yaml`:
   - `number` to kolejny trzycyfrowy numer eksponatu,
   - `text` to opcjonalny, także wielowierszowy tekst związany ze zdjęciem; dla braku tekstu użyj pustej wartości,
   - podaj rzeczywiste `width` i `height` obrazu WebP,
   - `title` może pozostać pusty, jeśli zdjęcie nie ma tytułu,
   - opcjonalne `description` dodawaj tylko, gdy nie jest puste.
6. Wygeneruj galerię poleceniem:
   `just museum`

Generator tworzy miniatury w `obrazy/muzeum-włazów-kanalizacyjnych/thumbnails/`, sortuje eksponaty od
najnowszych i aktualizuje generowaną sekcję w `muzeum-włazów-kanalizacyjnych.html`. Wypełnione pole `text`
jest wyświetlane na karcie i w popupie. Nie edytuj ręcznie
tej sekcji HTML.

## Ważne pliki

- `naming_pattern.md` — konwencja nazw i parametrów obrazów.
- `muzeum-włazów-kanalizacyjnych.yaml` — źródło danych eksponatów.
- `generate_museum.py` — walidacja danych, generowanie miniatur i HTML.
- `muzeum-włazów-kanalizacyjnych.html` — wygenerowana strona galerii.
- `obrazy/muzeum-włazów-kanalizacyjnych/` — obrazy główne i miniatury.

## Walidacja

Po zmianach uruchom `just museum`. Generator sprawdza między innymi unikalność plików i numerów,
zgodność daty z nazwą pliku, format WebP, wymiary oraz istnienie obrazów. Na koniec sprawdź:

```sh
git diff --check
git status --short
```

Zachowuj niezwiązane zmiany użytkownika w YAML-u i innych plikach — nie resetuj ich ani nie nadpisuj.
