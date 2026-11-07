# Specyfikacja prototypu 3D — Muzeum włazów kanalizacyjnych

## Cel

`proto.html` jest niezależnym prototypem trójwymiarowego muzeum zdjęć włazów kanalizacyjnych. Ma służyć jako baza do dalszego projektowania budynku, nawigacji i interakcji.

Prototyp nie zastępuje obecnej strony `muzeum-włazów-kanalizacyjnych.html`. Istniejąca strona oraz generator galerii powinny pozostać nietknięte.

## Uruchamianie

- Plik: `proto.html`.
- Można otworzyć go bezpośrednio przez `file://`.
- Three.js jest pobierany z CDN, więc wymagane jest połączenie z Internetem.
- Przy `file://` obrazy są kierowane do `https://bartekbrak.github.io/`, ponieważ przeglądarka blokuje część lokalnych zasobów z originu `null`.
- Na stronie HTTPS używane są ścieżki względne.
- Lokalna tekstura podłogi jest dodatkowo osadzona w HTML jako Data URI, żeby działała również bez serwera.
- Przy problemach `THREE.WebGLRenderer: Error creating WebGL context` należy zamknąć inne karty z prototypem i zrestartować przeglądarkę. Jest to limit/utrata kontekstu WebGL, a nie błąd układu muzeum.

## Technologie

- Vanilla HTML/CSS/JavaScript.
- Three.js `0.171.0` z CDN przez import map.
- WebGL renderer bez antyaliasingu, z `powerPreference: 'low-power'`.
- Brak frameworka i bundlera.
- Dane eksponatów są osadzone bezpośrednio w `proto.html` jako `museumExhibits`.

## Start i kamera

Po załadowaniu widoczny jest overlay:

> kliknij, żeby zwiedzać

Pierwsze kliknięcie uruchamia Pointer Lock na canvasie. Tekst znika, kursor zostaje ukryty, a kamera może obracać się bez ograniczenia krawędziami ekranu.

Po przechwyceniu kamery:

- ruch myszy obraca kamerę,
- `W` / `S` lub `↑` / `↓` — ruch do przodu i do tyłu,
- `A` / `D` — strafe w lewo i prawo,
- `←` / `→` — obrót klawiaturą,
- `Shift` — bieg, prędkość 2× względem chodu.

Aktualne prędkości:

- chód: `16.5` jednostki/s,
- bieg: `33` jednostki/s.

`Esc` jest natywnym mechanizmem przeglądarki do opuszczenia Pointer Lock. Po jego użyciu ponowne przechwycenie następuje po kliknięciu overlayu/sceny.

## Układ budynku

Budynek ma układ typu **grzebień**:

- wąski korytarz główny o szerokości około 8 m,
- sale po lewej i prawej stronie korytarza,
- poprzeczne ściany działowe z przejściem w osi korytarza,
- każda lokalizacja z kolekcji dostaje własną salę,
- pary lokalizacji są układane po przeciwnych stronach korytarza.

Rozmiar sal jest wyliczany dynamicznie na podstawie liczby eksponatów danej lokalizacji. Sale z większą kolekcją są głębsze.

Ruch jest ograniczony do budynku i ma podstawową kolizję z poprzecznymi ścianami. Przez ścianę można przejść tylko w centralnym przejściu.

## Eksponaty

- Eksponaty są grupowane według `location`.
- Każdy eksponat jest obrazem na ścianie zewnętrznej właściwej sali.
- Obrazy są rozmieszczane z odstępem co najmniej `4.4` jednostki, dzięki czemu nie nachodzą na siebie.
- Dla większych kolekcji stosowane są dwa rzędy obrazów.
- Pod każdym obrazem znajduje się tekst 3D w formacie:

  `numer · lokalizacja · data · autor`

- Nad salą znajduje się nazwa lokalizacji.
- Obrazy na ścianach są ładowane z miniaturek.
- Kliknięcie obrazu wskazanego centralnym celownikiem otwiera popup.

## Celownik i popup

Na środku ekranu znajduje się prosty celownik. Raycaster sprawdza obiekt przecinający środek kamery.

Gdy celownik trafia obraz:

- obraz i jego rama są delikatnie powiększane,
- obraz staje się aktywnym celem kliknięcia.

Popup:

- pokazuje pełny obraz, tytuł i metadane,
- globalny `mouseup` zamyka popup, jeśli jest otwarty,
- event zamykający popup jest zatrzymywany, żeby to samo kliknięcie nie otworzyło od razu kolejnego obrazu,
- przy zamknięciu czyszczone są `src`, alt, tytuł i metadane, więc poprzedni obraz nie miga przy kolejnym otwarciu.

## Tekst na ścianie wejściowej

Za początkową pozycją użytkownika znajduje się czarna ściana z tekstem szkockiej pieśni. Tekst:

- jest odwrócony tak, żeby był czytelny od strony użytkownika,
- jest rozmieszczony w trzech kolumnach,
- zaczyna się wysoko nad podłogą, ale cały panel znajduje się w dolnej części ściany,
- jest renderowany do CanvasTexture.

Kliknięcie tej ściany po przechwyceniu kamery przełącza muzykę `kath.mp3`.

## Muzyka

Plik audio:

`kath.mp3`

Zachowanie:

- kliknięcie ściany wejściowej włącza zapętloną muzykę,
- fade-in trwa 2 sekundy,
- ponowne kliknięcie ściany wyłącza muzykę,
- fade-out trwa 2 sekundy.

## Materiały i wygląd

- Zewnętrzne ściany: czarne i nieprzezroczyste.
- Ściany działowe: czarne, lekko przezroczyste, z materiałem dwustronnym.
- Sufit: całkowicie czarny.
- Podłoga: zdjęcie kamiennej nawierzchni `podloga.webp`, powtarzane z `MirroredRepeatWrapping`.
- Tekstura podłogi jest powtarzana dwa razy gęściej niż początkowo, żeby kamienie były mniejsze.
- Materiał podłogi jest przyciemniony kolorem `0x3d3d3d`.
- Obecnie nie ma mgły.
- Obecnie nie ma czerwonych reflektorów ani dodatkowych czerwonych świateł — zostały usunięte z powodu braku widocznego efektu i pogorszenia wydajności.

## Ładowanie i wydajność

Podczas startu:

- scena uruchamia się zanim wszystkie obrazy zostaną załadowane,
- ruch jest dostępny w trakcie ładowania,
- widoczny jest tekst:

  `psst, stwarzam, za chwilę...`

- pasek pokazuje postęp miniaturek oraz tekstury podłogi,
- obrazy są ładowane asynchronicznie, maksymalnie 4 równolegle,
- po zakończeniu ładowania overlay wykonuje fade-out przez 3 sekundy.

Dodatkowe zabezpieczenia wydajności:

- wyłączony antialiasing,
- wyłączone cienie rendererera,
- jedna tekstura sufitu zamiast setek kafli geometrii,
- brak aktywnych czerwonych reflektorów.

## Klawiatura i zabezpieczenie przed zacinaniem

Stan klawiszy jest oparty o `event.code`, a nie `event.key`.

Stan jest czyszczony:

- przy `keyup`,
- przy utracie fokusu okna,
- przy ukryciu karty,
- przy zmianie Pointer Lock,
- przez watchdog po 750 ms bez kolejnego zdarzenia dla zwykłych klawiszy ruchu.

`ShiftLeft` i `ShiftRight` nie są wygaszane przez watchdog, ponieważ przeglądarki często nie wysyłają dla nich powtarzanych zdarzeń `keydown`. Są czyszczone przy `keyup`, utracie fokusu i zmianie karty.

## Ważne pliki

- `proto.html` — cały prototyp.
- `kath.mp3` — muzyka ściany wejściowej.
- `obrazy/muzeum-włazów-kanalizacyjnych/podloga.webp` — tekstura podłogi.
- `muzeum-włazów-kanalizacyjnych.html` — istniejąca klasyczna galeria, nie modyfikować ręcznie sekcji generowanej.
- `muzeum-włazów-kanalizacyjnych.yaml` — źródło danych eksponatów.

## Następne możliwe kroki

1. Dodać minimapę lub schemat budynku.
2. Przenieść dane eksponatów do osobnego pliku JSON generowanego z YAML-a.
3. Dodać prawdziwy system kolizji dla wszystkich ścian i narożników.
4. Dodać animowane, widoczne źródła światła bez zwiększania liczby kosztownych świateł WebGL.
5. Dodać przejścia między salami i osobne scenografie lokalizacji.
6. Dodać ekran ustawień jakości grafiki.
7. Rozważyć lokalne bundlowanie Three.js, jeśli prototyp ma działać offline bez CDN.
