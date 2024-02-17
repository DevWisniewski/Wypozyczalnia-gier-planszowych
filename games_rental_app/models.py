from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.utils import timezone


class BoardGame(models.Model):
    """Reprezentuje grę planszową z informacjami o grze."""
    name = models.CharField(max_length=50)  # Nazwa gry
    description = models.TextField()  # Opis gry
    number_of_players = models.CharField(max_length=10)  # Liczba graczy
    minimum_age = models.IntegerField(validators=[MinValueValidator(2)])  # Minimalny wiek graczy
    maximum_age = models.IntegerField(validators=[MinValueValidator(120)])  # Maksymalny wiek graczy
    duration = models.IntegerField(validators=[MinValueValidator(1)])  # Czas trwania gry w minutach
    rental_price_per_day = models.DecimalField(max_digits=4, decimal_places=2)  # Cena wynajmu za 24h
    deposit = models.DecimalField(max_digits=4, decimal_places=2)  # Wysokość kaucji za wypożyczenie gry


class Inventory(models.Model):
    """Stan magazynowy konkretnego modelu gry planszowej."""

    inventory_id = models.AutoField(primary_key=True)  # Unikalny identyfikator dla każdego egzemplarza gry

    # Klucz obcy do modelu BoardGame, odnoszący się do konkretnej gry planszowej
    game = models.ForeignKey(BoardGame, on_delete=models.CASCADE)

    # Ilość dostępnych egzemplarzy danej gry planszowej
    quantity = models.IntegerField(validators=[MinValueValidator(0)])


class Address(models.Model):
    """Model adresowy, przechowujący informacje o adresie klienta."""
    street = models.CharField(max_length=100)  # Ulica
    house_number = models.CharField(max_length=10)  # Numer domu/mieszkania
    postal_code = models.CharField(max_length=10)  # Kod pocztowy
    city = models.CharField(max_length=50)  # Miasto
    country = models.CharField(max_length=50)  # Kraj


class CustomUser(AbstractUser):
    """Niestandardowy model użytkownika, zawierający dodatkowe informacje: numer telefonu i adres."""

    # Regex dla numeru telefonu; opcjonalny '+' i od 9 do 15 cyfr
    phone_regex = RegexValidator(
        regex=r'^\+?\d{9,15}$',
        message="Numer telefonu musi być w formacie: '+999999999'. Dozwolone do 15 cyfr."
    )

    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)  # Numer telefonu, opcjonalny

    # Klucz obcy do modelu Address; ustawia NULL, gdy adres jest usunięty; opcjonalny
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)

    # Pole email jest wymaganego, unikalne
    email = models.EmailField(unique=True, blank=False, null=False)


class Rental(models.Model):
    """Szczegóły wypożyczeń gier przez klientów."""

    rental_id = models.AutoField(primary_key=True)  # Unikalny identyfikator wypożyczenia

    # Klucz obcy do tabeli użytkowników (klientów)
    customer = models.ForeignKey(
        'CustomUser', on_delete=models.CASCADE
    )  # Usunięcie klienta powoduje usunięcie jego wypożyczeń

    # Klucz obcy do tabeli Inventory, określający, który egzemplarz gry został wypożyczony
    inventory = models.ForeignKey(
        'Inventory', on_delete=models.CASCADE
    )  # Usunięcie gry z magazynu powoduje usunięcie zapisu o jej wypożyczeniu

    rental_date = models.DateTimeField(default=timezone.now)  # Data wypożyczenia
    planned_return_date = models.DateTimeField(verbose_name='Planned Return Date')  # Planowana data zwrotu
    actual_return_date = models.DateTimeField(null=True, blank=True)  # Rzeczywista data zwrotu
    total_cost = models.DecimalField(max_digits=6, decimal_places=2)  # Całkowity koszt wypożyczenia
