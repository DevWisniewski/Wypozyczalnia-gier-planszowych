from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import CreateView, FormView, ListView, RedirectView, TemplateView
from django.views.generic.detail import DetailView

from .forms import LoginForm, AddUserForm, GameFilterForm
from .models import BoardGame, Address, Inventory

User = get_user_model()


class LoginView(FormView):
    """
    Obsługuje wyświetlanie formularza logowania oraz proces logowania.
    """
    template_name = "games_rental_app/login.html"
    form_class = LoginForm
    success_url = reverse_lazy("my_account")

    def form_valid(self, form):
        """
        Loguje użytkownika, jeśli formularz jest poprawnie wypełniony.
        """
        user = form.user
        login(self.request, user)
        return super().form_valid(form)


class LogoutView(RedirectView):
    """
    Widok wylogowania użytkownika.
    Obsługuje proces wylogowania użytkownika i przekierowuje go na stronę logowania.
    """
    url = reverse_lazy("login")

    def get(self, request, *args, **kwargs):
        """
        Wylogowuje użytkownika po wejściu na ten widok.
        """
        logout(request)
        return super().get(request, *args, **kwargs)


class AddUserView(CreateView):
    """
    Widok tworzenia nowego użytkownika.
    Obsługuje wyświetlanie formularza rejestracji i tworzenie nowego konta użytkownika.
    """
    template_name = "games_rental_app/add_user.html"
    model = User
    form_class = AddUserForm
    success_url = reverse_lazy("login")


class MyAccountView(LoginRequiredMixin, TemplateView):
    """
    Widok strony 'Moje konto' dostępny tylko dla zalogowanych użytkowników.
    Umożliwia wyświetlanie i edycję danych osobowych oraz adresu użytkownika.

    Dziedziczy po:
    - LoginRequiredMixin: - powoduje, że tylko zalogowani użytkownicy mają dostęp do tego widoku.
    - TemplateView: - umożliwia korzystanie z generycznego widoku opartego na szablonie.
    """

    template_name = 'games_rental_app/my_account.html'

    def get_context_data(self, **kwargs):
        """
        Zwraca kontekst danych dla szablonu, dodaje obiekt zalogowanego użytkownika do kontekstu.
        """
        context = super(MyAccountView, self).get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

    def post(self, request, *args, **kwargs):
        """
        Obsługuje żądania POST z formularza. Umożliwia aktualizację danych osobowych oraz adresu użytkownika.
        """
        user = request.user  # Pobranie aktualnie zalogowanego użytkownika
        user = request.user  # do zmiennej user przypisujemy aktualnie zalogowanego użytkownika

        # Pobieranie z formularza danych osobowych wprowadzonych przez zalogowanego użytkownika
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.phone_number = request.POST.get('phone_number', user.phone_number)
        # Zapisanie nowych danych użytkownika
        user.save()

        # Pobieranie z formularza adresu wprowadzonego przez zalogowanego użytkownika
        street = request.POST.get('street')
        house_number = request.POST.get('house_number')
        postal_code = request.POST.get('postal_code')
        city = request.POST.get('city')
        country = request.POST.get('country')

        # Sprawdzenie, czy użytkownik podał wszystkie dane w formularzu
        if street and house_number and postal_code and city and country:

            if user.address:            # Sprawdzenie, czy użytkownik ma już przypisany adres,
                address = user.address  # Jeśli tak, używany do modyfikacji istniejący obiekt adresu
            else:
                address = Address()     # Jeśli nie, tworzony jest nowy obiekt adresu

            # Aktualizacja lub ustawienie nowych danych adresowych
            address.street = street
            address.house_number = house_number
            address.postal_code = postal_code
            address.city = city
            address.country = country
            address.save()

            # Przypisanie nowego obiektu adresu do profilu użytkownika
            user.address = address
            user.save()

        return redirect('my_account')


class StaticGameDetailsView(TemplateView):
    """
    Widok testowy; pokazuje statyczne informacje o grze.
    """
    template_name = 'games_rental_app/static_game_details.html'


class GameDetailsView(DetailView):
    """
    Pokazuje szczegółowe informacje o grze na podstawie danych z bazy danych.
    Używa 'slug' jako identyfikatora do wyszukania gry.
    """
    model = BoardGame
    template_name = 'games_rental_app/dynamic_game_details.html'
    context_object_name = 'game'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super(GameDetailsView, self).get_context_data(**kwargs)
        game = context['game']
        inventory_items = Inventory.objects.filter(game=game, is_rented=False)
        context['is_available'] = inventory_items.exists()
        return context

class ContactView(TemplateView):
    """
    Widok strony kontaktowej. Wyświetla informacje kontaktowe i formularz do kontaktu.
    """
    template_name = 'games_rental_app/contact.html'


class WelcomeView(TemplateView):
    """
    Widok strony powitalnej. Pokazuje informacje ogólne o serwisie.
    """
    template_name = 'games_rental_app/welcome.html'


class GameListView(ListView):
    """
    Widok listy gier. Wyświetla gry dostępne w serwisie z możliwością filtrowania wyników.
    """
    model = BoardGame
    template_name = 'games_rental_app/game_list.html'
    context_object_name = 'games'

    def get_queryset(self):
        """
        Pobiera listę gier dostępnych w serwisie, uwzględniając wybory użytkownika w formularzu filtrowania.
        """
        # Pobiera domyślną listę wszystkich gier
        queryset = super().get_queryset()

        # Tworzy formularz filtrowania gier na podstawie wyborów użytkownika
        form = GameFilterForm(self.request.GET)

        # Warunek sprawdzający, czy dane wprowadzone przez użytkownika są zgodnie z regułami formularza
        if form.is_valid():
            # Pobiera wartości wybrane przez użytkownika
            number_of_players = form.cleaned_data.get('number_of_players')
            min_age = form.cleaned_data.get('min_age')
            min_duration = form.cleaned_data.get('min_duration')
            max_duration = form.cleaned_data.get('max_duration')
            min_price = form.cleaned_data.get('min_price')
            max_price = form.cleaned_data.get('max_price')

            # Filtruje listę gier na podstawie wyborów użytkownika
            if number_of_players and int(number_of_players) != 0:
                queryset = queryset.filter(number_of_players__contains=[int(number_of_players)])
            if min_age:
                queryset = queryset.filter(minimum_age__gte=min_age)
            if min_duration and int(min_duration) != 0:
                queryset = queryset.filter(min_duration__gte=int(min_duration))
            if max_duration and int(max_duration) != 0:
                queryset = queryset.filter(max_duration__lte=int(max_duration))
            if min_price and int(min_price) != 0:
                queryset = queryset.filter(rental_price_per_day__gte=float(min_price))
            if max_price and int(max_price) != 0:
                queryset = queryset.filter(rental_price_per_day__lte=float(max_price))

        return queryset

    def get_context_data(self, **kwargs):
        """
        Pobiera i dostarcza dane kontekstowe dla szablonu.
        Dodaje formularz filtrowania gier do kontekstu.
        """
        # Pobiera domyślne dane kontekstowe
        context = super().get_context_data(**kwargs)

        # Tworzy formularz filtrowania gier na podstawie danych przekazanych przez użytkownika
        context['form'] = GameFilterForm(self.request.GET or None)

        return context
