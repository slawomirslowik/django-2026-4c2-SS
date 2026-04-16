# Django: Pliki statyczne – Manual i Zadania (na podstawie tutoriala cz. 6)

Źródło: [Django Tutorial cz. 6 – Pliki statyczne](https://docs.djangoproject.com/en/6.0/intro/tutorial06/)

---

## Do czego służą pliki statyczne w Django?

Oprócz HTML generowanego przez serwer, aplikacje webowe potrzebują dodatkowych plików – obrazków, JavaScriptu lub CSS – niezbędnych do poprawnego renderowania strony. W Django pliki tego typu nazywamy **plikami statycznymi** (static files).

Do zarządzania nimi służy wbudowana aplikacja `django.contrib.staticfiles`, która zbiera pliki statyczne ze wszystkich aplikacji projektu w jedno miejsce, co ułatwia ich obsługę zarówno podczas developmentu, jak i na serwerze produkcyjnym.

---

## Instrukcja: Dodanie stylów CSS do aplikacji polls

### 1. Utwórz katalog na pliki statyczne

W katalogu `polls` utwórz strukturę folderów:

```
polls/
    static/
        polls/
            style.css
```

> **Uwaga o przestrzeni nazw:** Podobnie jak szablony, pliki statyczne należy umieszczać w podkatalogu o nazwie aplikacji (`polls/static/polls/`), aby uniknąć konfliktów nazw między różnymi aplikacjami.

### 2. Dodaj style CSS

W pliku `polls/static/polls/style.css` wpisz:

```css
li a {
    color: green;
}
```

### 3. Załaduj plik CSS w szablonie

Na początku pliku `polls/templates/polls/index.html` dodaj tag `{% load static %}` i link do arkusza stylów:

```html
{% load static %}

<link rel="stylesheet" href="{% static 'polls/style.css' %}">
```

> Tag `{% static %}` generuje bezwzględny URL do pliku statycznego. Dzięki temu nie musisz ręcznie wpisywać ścieżki – URL jest obliczany na podstawie ustawienia `STATIC_URL` w `settings.py`.

### 4. Uruchom serwer i sprawdź efekt

```
py manage.py runserver
```

Przejdź do `http://127.0.0.1:8000/polls/` – linki do pytań powinny być teraz zielone.

---

## Instrukcja: Dodanie obrazka tła

### 1. Utwórz katalog na obrazki

W katalogu `polls/static/polls/` utwórz podkatalog `images`:

```
polls/
    static/
        polls/
            images/
                background.png
```

Umieść w nim dowolny plik obrazka (np. `background.png`).

### 2. Dodaj odwołanie do obrazka w CSS

W pliku `polls/static/polls/style.css` dodaj:

```css
body {
    background: white url("images/background.png") no-repeat;
}
```

> **Ważne:** W plikach statycznych (np. CSS) **nie używaj** tagu `{% static %}` – jest on dostępny wyłącznie w szablonach Django. Do łączenia plików statycznych między sobą używaj **ścieżek względnych**, co pozwala na łatwą zmianę `STATIC_URL` bez modyfikowania plików CSS.

### 3. Sprawdź efekt

Przeładuj stronę `http://127.0.0.1:8000/polls/` – w lewym górnym rogu powinieneś zobaczyć obrazek tła.

---

## Pełna struktura plików po wykonaniu zadania

```
polls/
    static/
        polls/
            style.css
            images/
                background.png
    templates/
        polls/
            index.html   ← zawiera {% load static %} i <link>
```

---

## Podsumowanie – najważniejsze zasady

| Zasada | Opis |
|--------|------|
| Katalog statyczny | `polls/static/polls/` – przestrzeń nazw jak w szablonach |
| Tag w szablonie | `{% load static %}` na początku pliku, `{% static 'ścieżka' %}` do generowania URL |
| W plikach CSS/JS | Używaj ścieżek względnych, NIE tagu `{% static %}` |
| Ustawienie | `STATIC_URL` w `settings.py` określa bazowy URL plików statycznych |

---

## Zadanie: Ostyluj aplikację polls

1. Utwórz plik `polls/static/polls/style.css` i dodaj własne style:
   - Zmień kolor linków na wybrany przez siebie.
   - Dodaj styl dla nagłówka `<h1>`.
   - Dodaj obramowanie lub tło do listy pytań.

2. Załaduj arkusz stylów w szablonie `index.html` za pomocą `{% load static %}` i tagu `{% static %}`.

3. (Opcjonalnie) Dodaj obrazek tła w katalogu `polls/static/polls/images/` i podlinkuj go w CSS.

4. Uruchom serwer i sprawdź efekt w przeglądarce.

5. Ostyluj również szablony `detail.html` i `results.html`.

---

**Pamiętaj, aby po każdej zmianie w kodzie zapisać pliki i odświeżyć stronę w przeglądarce oraz na zakończenie wykonać commit i push do repozytorium GitHub.**
