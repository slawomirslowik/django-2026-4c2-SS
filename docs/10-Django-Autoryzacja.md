# Django: Logowanie i autoryzacja użytkowników

Źródło: [Django – Uwierzytelnianie użytkowników](https://docs.djangoproject.com/en/6.0/topics/auth/)

---

## Wstęp

Django posiada wbudowany system uwierzytelniania (`django.contrib.auth`), który jest już dodany do projektu w `INSTALLED_APPS`. Umożliwia on:
- rejestrację użytkowników,
- logowanie i wylogowanie,
- ochronę widoków przed niezalogowanymi użytkownikami,
- sprawdzanie uprawnień.

---

## Krok 1: Dodaj URL-e logowania do `mysite/urls.py`

Django dostarcza gotowe widoki logowania i wylogowania. Wystarczy podpiąć je w głównym pliku URLi:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('polls/', include('polls.urls')),
    path('accounts/', include('django.contrib.auth.urls')),  # ← dodaj tę linię
]
```

Podpięcie `django.contrib.auth.urls` rejestruje automatycznie następujące adresy:

| URL | Nazwa | Opis |
|-----|-------|------|
| `/accounts/login/` | `login` | Formularz logowania |
| `/accounts/logout/` | `logout` | Wylogowanie |
| `/accounts/password_change/` | `password_change` | Zmiana hasła |
| `/accounts/password_reset/` | `password_reset` | Reset hasła przez e-mail |

---

## Krok 2: Skonfiguruj przekierowania po logowaniu w `mysite/settings.py`

```python
# Dokąd przekierować po zalogowaniu (domyślnie: /accounts/profile/)
LOGIN_REDIRECT_URL = '/polls/'

# Dokąd przekierować po wylogowaniu
LOGOUT_REDIRECT_URL = '/accounts/login/'

# Dokąd przekierować niezalogowanych użytkowników (używane przez @login_required)
LOGIN_URL = '/accounts/login/'
```

---

## Krok 3: Utwórz szablon formularza logowania

Django szuka szablonu logowania pod ścieżką `registration/login.html`. Utwórz plik:

`polls/templates/registration/login.html`

```html
{% extends 'polls/base.html' %}

{% block title %}Logowanie{% endblock %}

{% block content %}
<div class="row justify-content-center">
    <div class="col-md-5">
        <div class="card mt-5">
            <div class="card-header">
                <h4 class="mb-0">Logowanie</h4>
            </div>
            <div class="card-body">
                <form method="post">
                    {% csrf_token %}
                    {% for field in form %}
                        <div class="mb-3">
                            <label for="{{ field.id_for_label }}" class="form-label">
                                {{ field.label }}
                            </label>
                            <input type="{{ field.field.widget.input_type }}"
                                   name="{{ field.html_name }}"
                                   id="{{ field.id_for_label }}"
                                   class="form-control {% if field.errors %}is-invalid{% endif %}"
                                   {% if field.value %}value="{{ field.value }}"{% endif %}>
                            {% for error in field.errors %}
                                <div class="invalid-feedback">{{ error }}</div>
                            {% endfor %}
                        </div>
                    {% endfor %}
                    <button type="submit" class="btn btn-primary w-100">Zaloguj się</button>
                </form>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

> **Uwaga:** Katalog `registration/` musi znajdować się w miejscu, gdzie Django szuka szablonów. Ponieważ używamy `APP_DIRS: True`, możemy go umieścić w `polls/templates/registration/`.

---

## Krok 4: Chroń widoki – dekorator `@login_required`

Aby wymagać zalogowania do konkretnych widoków, użyj dekoratora `@login_required` w `polls/views.py`:

```python
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Question, Choice

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

@login_required  # ← tylko zalogowani użytkownicy mogą głosować
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "Nie wybrano odpowiedzi.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
```

Niezalogowany użytkownik próbujący głosować zostanie automatycznie przekierowany na stronę logowania.

---

## Krok 5: Wyświetl informacje o użytkowniku w szablonie bazowym

Zaktualizuj `polls/templates/polls/base.html`, aby w pasku nawigacyjnym pokazywać aktualnie zalogowanego użytkownika i przycisk wylogowania:

```html
<nav class="navbar navbar-expand-lg navbar-dark bg-dark mb-4">
    <div class="container">
        <a class="navbar-brand" href="{% url 'polls:index' %}">📊 Polls App</a>

        <div class="ms-auto d-flex align-items-center">
            {% if user.is_authenticated %}
                <span class="text-light me-3">👤 {{ user.username }}</span>
                <form method="post" action="{% url 'logout' %}">
                    {% csrf_token %}
                    <button type="submit" class="btn btn-outline-light btn-sm">Wyloguj</button>
                </form>
            {% else %}
                <a href="{% url 'login' %}" class="btn btn-outline-light btn-sm">Zaloguj się</a>
            {% endif %}
        </div>
    </div>
</nav>
```

---

## Krok 6: Rejestracja nowych użytkowników (opcjonalnie)

Django nie dostarcza gotowego widoku rejestracji – trzeba go napisać samodzielnie. Dodaj w `polls/views.py`:

```python
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import redirect

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # automatyczne logowanie po rejestracji
            return redirect('polls:index')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
```

Dodaj URL w `polls/urls.py`:

```python
path('register/', views.register, name='register'),
```

Utwórz szablon `polls/templates/registration/register.html`:

```html
{% extends 'polls/base.html' %}

{% block title %}Rejestracja{% endblock %}

{% block content %}
<div class="row justify-content-center">
    <div class="col-md-6">
        <div class="card mt-5">
            <div class="card-header"><h4 class="mb-0">Rejestracja</h4></div>
            <div class="card-body">
                <form method="post">
                    {% csrf_token %}
                    {% for field in form %}
                        <div class="mb-3">
                            <label class="form-label">{{ field.label }}</label>
                            <input type="{{ field.field.widget.input_type }}"
                                   name="{{ field.html_name }}"
                                   class="form-control {% if field.errors %}is-invalid{% endif %}">
                            {% for error in field.errors %}
                                <div class="invalid-feedback">{{ error }}</div>
                            {% endfor %}
                            {% if field.help_text %}
                                <div class="form-text text-muted">{{ field.help_text }}</div>
                            {% endif %}
                        </div>
                    {% endfor %}
                    <button type="submit" class="btn btn-success w-100">Zarejestruj się</button>
                </form>
                <hr>
                <p class="text-center mb-0">
                    Masz już konto? <a href="{% url 'login' %}">Zaloguj się</a>
                </p>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

---

## Podsumowanie – co zostało dodane

| Element | Opis |
|---------|------|
| `django.contrib.auth.urls` | Gotowe URLe logowania/wylogowania/zmiany hasła |
| `LOGIN_REDIRECT_URL` | Przekierowanie po zalogowaniu |
| `LOGOUT_REDIRECT_URL` | Przekierowanie po wylogowaniu |
| `@login_required` | Dekorator chroniący widok głosowania |
| `registration/login.html` | Szablon formularza logowania |
| `user.is_authenticated` | Zmienna dostępna w każdym szablonie |
| `user.username` | Nazwa zalogowanego użytkownika w szablonie |
| Widok rejestracji | Własny widok z `UserCreationForm` (opcjonalnie) |

---

## Zadanie

1. Podepnij `django.contrib.auth.urls` w `mysite/urls.py`.
2. Dodaj `LOGIN_REDIRECT_URL`, `LOGOUT_REDIRECT_URL` i `LOGIN_URL` do `settings.py`.
3. Utwórz szablon `registration/login.html`.
4. Dodaj dekorator `@login_required` do widoku `vote` w `polls/views.py`.
5. Zaktualizuj `base.html` – wyświetl nazwę zalogowanego użytkownika i przycisk wylogowania.
6. (Opcjonalnie) Dodaj widok i szablon rejestracji nowych użytkowników.
7. Przetestuj: zaloguj się, zagłosuj, wyloguj się i spróbuj zagłosować ponownie.

---

**Pamiętaj, aby po każdej zmianie zapisać pliki i odświeżyć stronę w przeglądarce oraz na zakończenie wykonać commit i push do repozytorium GitHub.**

---

## Moduł rozszerzony: Powiązanie głosów z użytkownikami (model Vote)

### Problem z obecną implementacją

W obecnej wersji model `Choice` przechowuje jedynie licznik głosów:

```python
class Choice(models.Model):
    votes = models.IntegerField(default=0)  # tylko liczba, nie kto głosował
```

Widok `vote` jedynie inkrementuje ten licznik, co oznacza że:
- nie wiadomo, kto głosował,
- jeden użytkownik może głosować wielokrotnie,
- nie można cofnąć głosu konkretnej osoby.

---

### Krok 1: Dodaj model `Vote` do `polls/models.py`

```python
from django.contrib.auth.models import User

class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    voted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'choice')  # jeden głos na daną odpowiedź

    def __str__(self):
        return f"{self.user.username} → {self.choice.choice_text}"
```

---

### Krok 2: Utwórz i zastosuj migracje

```
py manage.py makemigrations polls
py manage.py migrate
```

---

### Krok 3: Zaktualizuj widok `vote` w `polls/views.py`

```python
from .models import Question, Choice, Vote

@login_required
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "Nie wybrano odpowiedzi.",
        })

    # Sprawdź czy użytkownik już głosował na to pytanie
    already_voted = Vote.objects.filter(
        user=request.user,
        choice__question=question
    ).exists()

    if already_voted:
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "Już oddałeś głos na to pytanie.",
        })

    # Zapisz głos powiązany z użytkownikiem
    Vote.objects.create(user=request.user, choice=selected_choice)
    selected_choice.votes += 1
    selected_choice.save()
    return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
```

---

### Krok 4: Zarejestruj model Vote w panelu admina (`polls/admin.py`)

```python
from django.contrib import admin
from .models import Question, Choice, Vote

admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Vote)
```

Dzięki temu w panelu `/admin/` będzie widać listę wszystkich głosów z informacją, kto i na co głosował.

---

### Podsumowanie zmian

| Element | Przed | Po |
|---------|-------|----|
| Przechowywanie głosu | Licznik w `Choice.votes` | Oddzielny rekord `Vote` z relacją do `User` |
| Wielokrotne głosowanie | Możliwe | Zablokowane (`unique_together`) |
| Kto głosował | Nieznane | Zapisane w bazie |
| Panel admina | Brak podglądu głosów | Pełna lista głosów z użytkownikami |

---

### Zadanie

1. Dodaj model `Vote` do `polls/models.py`.
2. Wykonaj migracje.
3. Zaktualizuj widok `vote` – sprawdzaj czy użytkownik już głosował.
4. Zarejestruj `Vote` w `admin.py`.
5. Zaloguj się jako dwa różne konta i sprawdź, czy system blokuje podwójne głosowanie.
6. Sprawdź w panelu admina listę oddanych głosów.

---

**Pamiętaj, aby po każdej zmianie zapisać pliki i odświeżyć stronę w przeglądarce oraz na zakończenie wykonać commit i push do repozytorium GitHub.**
