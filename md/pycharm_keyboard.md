# [pl] PyCharm klawiaturą. Warsztat dla kolegów.

# Wstęp.

0. Ja tak myślę, to wszystko jest subiektywne ale wierz mi, robie to dla
siebie i dla Ciebie.
1. Filozofia tegoż, potrzebujesz decyzji, ona się zwróci, tylko musisz mądrą decyzje podjąć.
1. Da się prawie wszystko, prawie wszystko warto.
2. Korzystaj ze standardowego rozkładu skrutów tak bardzo jak tylko możesz,
jest to przemyślany układ -
   będziesz mógł wymieniać się doświadczeniem z kolegami i koleżanką.

   Moje modyfikacje to:
   - `Alt + a` - annotacje
   - `Alt + w` - zamknij zakładkę, bo `Ctrl + F4` łamie palce.

3. Wydrukuj sobie ściągę (ma tylko standardowy układ). `Help -> Keymap
Reference`.
4. Dowiedz się co zasłania skróty.

    W Ubuntu, gnome-shell-classic:

    ```
    gsettings set org.gnome.desktop.wm.keybindings switch-to-workspace-left
    "[]"
    ```

    Moje doświadczenia spisałem [o
    tu](http://bartekbrak.github.io/notes.html#how-to-disable-mate-workspace-key-shortcuts)

5. Wiedz o `Command Palette` pod `Ctrl+Shift+A`.

    Wyszukaj tam:
    - `Settings`, jest kilka, jeden ma skrót
    - `Run Conflict Resolver`, o... nie ma skrótu

6. Naucz sie wyszukiwać w `Settings -> Keymap`, w obie strony.

7. [Mnemonics (keyboard)](https://en.wikipedia.org/wiki/Mnemonics_(keyboard))
raczej znasz?
8. To wszystko nie ma sensu jak sobie Interpretera nie ustawisz, no weź se ustaw
9. Filozofia 2, Że niby programista co duzo pisze albo dużo z IDE musi korzystać robi cos nie tak... tak, ale

# Jedziemy:

## Ogólne
* `Alt 1, 2, 3`, ... - panele numerowane, dodałbym sobie bazę danych na zero
czy co tam lubisz, (tu demo wyszukiwanie w tę druga strone w Keymap, `Alt + 0`)
* Powyższe podwójnie przełącza.
* `Shift + Esc` - wróć do edycji, raz na 177 razy nie działa.

## Nawigacja w kodzie
* `Ctrl + n`, `Ctrl + Shift + n`, `Ctrl + Alt + Shift + n`,
    - jak działają przy zaznaczonym tekście,
    - że nawet da się w szablonach
    - że nawet coś spoza znajdziesz
    - to powinien byc Twój główny sposób nawigacji

* `Ctrl + b`, `Ctrl + Alt + ◀`, `Ctrl + Alt + ▶`, wgłąb i z powrotem
* `Ctrl + tab`, The switcher, `Alt + ◀`, `Alt + ▶`, pomiędzy zakładkami,
* `Alt + ▲`, `Alt + ▼`, pomiędzy metodami, a między klasami nie ma, ale jak się złoży wszystko to łatwo kursorem jechać, a
  miałeś `Ctrl + n` robić
* `F2`, `Alt + Enter`, lint + naprawianie
* `Alt + j`, `Ctrl + Alt + Shif + j`, `Ctrl + Ctrl`, - multikursor
* `Ctrl + g` idź do linii
* _Implementation_ - `Ctrl + Alt + b`, co dziedziczy?
* `Ctrl + Shift + b` - _Type Declaration_, co to?
* `Ctrl + F12` - struktura, najłatwiej wyszukac tak metodę bo jets fuzzy

> In PyCharm, this action is only applicable to JavaScript.

* `Ctrl + Shift + Numpad-`, `Ctrl + Shift + Numpad+`, składanie
* `Ctrl + Shift + M` - _Move Caret to Matching Brace_ wow, lata po nawiasach!
* Historia wklejania:  `Ctrl + Shift + v`
* kopiowanie referencji, po co to? importy, testy, `Ctrl + Shift + C`, `Ctrl + Alt + Shift + C`
* nawigowanie po zmianach - `Ctrl + Alt + Shift + ▲▼`

# Refactoring menu
`Ctrl + Alt + Shift + T`  i eksploruj
- Move
- Rename
- extract variable  - reporting.views.report_edit
- extract constant
- extract method - reporting.chargeable_report.format_for_output
- inline - po co?


