from django.views.generic import CreateView, FormView, ListView, RedirectView
from django.urls import reverse, reverse_lazy
from django.contrib.auth import get_user_model, login, logout
from django.views.generic import TemplateView
from .forms import LoginForm, AddUserForm, GameFilterForm
from django.views.generic.detail import DetailView
from .models import BoardGame
from django.shortcuts import render, redirect
from django.views import View
from .forms import UserEditForm, AddressForm
from django.contrib.auth.mixins import LoginRequiredMixin

User = get_user_model()

class LoginView(FormView):
    template_name = "games_rental_app/login.html"
    form_class = LoginForm
    success_url = reverse_lazy("my_account")

    def form_valid(self, form):
        user = form.user
        login(self.request, user)
        return super().form_valid(form)


class LogoutView(RedirectView):
    url = reverse_lazy("login")

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)


class AddUserView(CreateView):
    template_name = "games_rental_app/add_user.html"
    model = User
    form_class = AddUserForm
    success_url = reverse_lazy("login")


class MyAccountView(LoginRequiredMixin, TemplateView):
    template_name = 'games_rental_app/my_account.html'

    def get_context_data(self, **kwargs):
        context = super(MyAccountView, self).get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


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
        Pobiera listę gier dostępnych w serwisie, uwzględniając wybory
        użytkownika w formularzu filtrowania.
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


# Klasa widoku do edycji danych użytkownika
class UserEditView(LoginRequiredMixin, View):
    def get(self, request):
        form = UserEditForm(instance=request.user)
        return render(request, 'games_rental_app/user_edit.html', {'form': form})

    def post(self, request):
        form = UserEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('my_account')
        return render(request, 'games_rental_app/user_edit.html', {'form': form})

# Klasa widoku do edycji adresu
class AddressEditView(LoginRequiredMixin, View):
    def get(self, request):
        try:
            address = request.user.address
        except Address.DoesNotExist:
            address = None
        form = AddressForm(instance=address)
        return render(request, 'games_rental_app/address_edit.html', {'form': form})

    def post(self, request):
        try:
            address = request.user.address
        except Address.DoesNotExist:
            address = None
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            new_address = form.save(commit=False)
            new_address.user = request.user
            new_address.save()
            return redirect('my_account')
        return render(request, 'games_rental_app/address_edit.html', {'form': form})