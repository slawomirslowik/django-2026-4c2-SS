# Django: Dodanie Bootstrap 5 do projektu

Źródło: [Bootstrap 5 – dokumentacja](https://getbootstrap.com/docs/5.3/getting-started/introduction/)

---

## Co to jest Bootstrap?

Bootstrap to popularny framework CSS, który umożliwia szybkie tworzenie responsywnych i estetycznych interfejsów użytkownika. Wersja 5 nie wymaga jQuery i oferuje bogaty zestaw gotowych komponentów (przyciski, formularze, karty, nawigacja itp.).

---

## Metoda 1: Bootstrap przez CDN (zalecana dla projektów edukacyjnych)

Najszybszy sposób – nie wymaga pobierania żadnych plików. Wystarczy dodać linki CDN do szablonu bazowego.

### Krok 1: Utwórz szablon bazowy

Utwórz plik `polls/templates/polls/base.html`:

```html
<!DOCTYPE html>
<html lang="pl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Polls{% endblock %}</title>

    <!-- Bootstrap 5 CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"
          rel="stylesheet"
          integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH"
          crossorigin="anonymous">
</head>
<body>

    <!-- Pasek nawigacyjny -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark mb-4">
        <div class="container">
            <a class="navbar-brand" href="{% url 'polls:index' %}">📊 Polls App</a>
        </div>
    </nav>

    <!-- Główna zawartość -->
    <div class="container">
        {% block content %}
        {% endblock %}
    </div>

    <!-- Bootstrap 5 JS (opcjonalne – potrzebne dla dropdownów, modali itp.) -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"
            integrity="sha384-YvpcrYf0tY3lHB60NNkmXc4s9bIOgUxi8T/jzmE/KiXnOGG3mAlWpbPKwnPSvq9"
            crossorigin="anonymous"></script>
</body>
</html>
```

---

## Krok 2: Zaktualizuj szablony polls, aby dziedziczyły po base.html

### `polls/templates/polls/index.html`

```html
{% extends 'polls/base.html' %}

{% block title %}Lista pytań{% endblock %}

{% block content %}
<h1 class="mb-4">Lista pytań</h1>

{% if latest_question_list %}
    <div class="list-group">
        {% for question in latest_question_list %}
            <a href="{% url 'polls:detail' question.id %}"
               class="list-group-item list-group-item-action d-flex justify-content-between align-items-center">
                {{ question.question_text }}
                <span class="badge bg-primary rounded-pill">Głosuj</span>
            </a>
        {% endfor %}
    </div>
{% else %}
    <div class="alert alert-info" role="alert">
        Brak dostępnych pytań.
    </div>
{% endif %}
{% endblock %}
```

---

### `polls/templates/polls/detail.html`

```html
{% extends 'polls/base.html' %}

{% block title %}{{ question.question_text }}{% endblock %}

{% block content %}
<h1 class="mb-4">{{ question.question_text }}</h1>

{% if error_message %}
    <div class="alert alert-danger" role="alert">
        {{ error_message }}
    </div>
{% endif %}

<form action="{% url 'polls:vote' question.id %}" method="post">
    {% csrf_token %}
    <div class="card">
        <div class="card-body">
            {% for choice in question.choice_set.all %}
                <div class="form-check mb-2">
                    <input class="form-check-input" type="radio"
                           name="choice"
                           id="choice{{ forloop.counter }}"
                           value="{{ choice.id }}">
                    <label class="form-check-label" for="choice{{ forloop.counter }}">
                        {{ choice.choice_text }}
                    </label>
                </div>
            {% endfor %}
        </div>
        <div class="card-footer">
            <button type="submit" class="btn btn-primary">Głosuj</button>
            <a href="{% url 'polls:index' %}" class="btn btn-secondary ms-2">Wróć do listy</a>
        </div>
    </div>
</form>
{% endblock %}
```

---

### `polls/templates/polls/results.html`

```html
{% extends 'polls/base.html' %}

{% block title %}Wyniki: {{ question.question_text }}{% endblock %}

{% block content %}
<h1 class="mb-4">{{ question.question_text }}</h1>

<ul class="list-group mb-4">
    {% for choice in question.choice_set.all %}
        <li class="list-group-item d-flex justify-content-between align-items-center">
            {{ choice.choice_text }}
            <span class="badge bg-success rounded-pill">{{ choice.votes }} głosów</span>
        </li>
    {% endfor %}
</ul>

<a href="{% url 'polls:detail' question.id %}" class="btn btn-outline-primary">Głosuj ponownie</a>
<a href="{% url 'polls:index' %}" class="btn btn-outline-secondary ms-2">Wróć do listy</a>
{% endblock %}
```

---

## Metoda 2: Bootstrap jako zależność projektu (django-bootstrap5)

Można zainstalować Bootstrap jako pakiet Pythona za pomocą biblioteki `django-bootstrap5`, która integruje Bootstrap bezpośrednio z systemem szablonów Django.

### Krok 1: Zainstaluj pakiet

```
pip install django-bootstrap5
```

### Krok 2: Dodaj do INSTALLED_APPS w `mysite/settings.py`

```python
INSTALLED_APPS = [
    ...
    'django_bootstrap5',
    ...
]
```

### Krok 3: Użyj w szablonie bazowym

Zaktualizuj plik `polls/templates/polls/base.html`:

```html
{% load django_bootstrap5 %}
<!DOCTYPE html>
<html lang="pl">
<head>
    <meta charset="UTF-8">
    <title>Polls</title>
    {% bootstrap_css %}
</head>
<body>
    <div class="container mt-4">
        {% block content %}{% endblock %}
    </div>
    {% bootstrap_javascript %}
</body>
</html>
```

Tagi dostępne po `{% load django_bootstrap5 %}`:

| Tag | Opis |
|-----|------|
| `{% bootstrap_css %}` | Wstawia tag `<link>` z Bootstrap CSS |
| `{% bootstrap_javascript %}` | Wstawia tag `<script>` z Bootstrap JS |
| `{% bootstrap_form form %}` | Automatycznie renderuje formularz Django ze stylami Bootstrap |
| `{% bootstrap_button "Głosuj" button_type="submit" button_class="btn-primary" %}` | Renderuje przycisk Bootstrap |

Więcej informacji: [django-bootstrap5 dokumentacja](https://django-bootstrap5.readthedocs.io/)

---

## Metoda 3: Bootstrap jako lokalny plik statyczny

Jeśli chcesz hostować Bootstrap lokalnie (np. bez dostępu do internetu):

### Krok 1: Pobierz Bootstrap

Pobierz skompilowane pliki CSS i JS ze strony [https://getbootstrap.com/docs/5.3/getting-started/download/](https://getbootstrap.com/docs/5.3/getting-started/download/) i umieść je w projekcie:

```
polls/
    static/
        polls/
            css/
                bootstrap.min.css
            js/
                bootstrap.bundle.min.js
```

### Krok 2: Załaduj pliki statyczne w base.html

```html
{% load static %}
<!DOCTYPE html>
<html lang="pl">
<head>
    ...
    <link rel="stylesheet" href="{% static 'polls/css/bootstrap.min.css' %}">
</head>
<body>
    ...
    <script src="{% static 'polls/js/bootstrap.bundle.min.js' %}"></script>
</body>
</html>
```

---

## Przydatne klasy Bootstrap użyte w szablonach

| Klasa | Opis |
|-------|------|
| `container` | Wyśrodkowany kontener z marginesami |
| `navbar` / `navbar-dark bg-dark` | Pasek nawigacyjny z ciemnym tłem |
| `list-group` / `list-group-item` | Lista z estetycznym obramowaniem |
| `list-group-item-action` | Element listy klikalny jak link |
| `badge bg-primary` | Kolorowa etykieta/licznik |
| `alert alert-danger` | Komunikat o błędzie (czerwony) |
| `alert alert-info` | Komunikat informacyjny (niebieski) |
| `form-check` / `form-check-input` | Stylizowane pola radio/checkbox |
| `card` / `card-body` / `card-footer` | Karta z zawartością i stopką |
| `btn btn-primary` | Przycisk główny (niebieski) |
| `btn btn-secondary` | Przycisk pomocniczy (szary) |
| `mb-4` | Margines dolny (margin-bottom) |
| `ms-2` | Margines lewy (margin-start) |

---

## Zadanie

1. Utwórz plik `polls/templates/polls/base.html` z Bootstrap 5 przez CDN.
2. Zaktualizuj szablony `index.html`, `detail.html` i `results.html`, aby dziedziczyły po `base.html`.
3. Uruchom serwer i sprawdź wygląd strony pod adresem `http://127.0.0.1:8000/polls/`.
4. (Opcjonalnie) Dodaj do paska nawigacyjnego link do panelu admina: `http://127.0.0.1:8000/admin/`.

---

**Pamiętaj, aby po każdej zmianie zapisać pliki i odświeżyć stronę w przeglądarce oraz na zakończenie wykonać commit i push do repozytorium GitHub.**
