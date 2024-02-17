from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


# Model dla danych gier
class GraPlanszowa(models.Model):
    nazwa_gry = models.CharField(max_length=100)  # Nazwa gry
    opis = models.TextField()  # Opis gry
    liczba_graczy = models.CharField(max_length=50)
    minimalny_wiek_graczy = models.IntegerField(validators=[MinValueValidator(2)])  # Minimalny wiek graczy
    maksymalny_wiek_graczy = models.IntegerField(validators=[MinValueValidator(2)])  # Maksymalny wiek graczy

    # Długość rozgrywki w minutach
    dlugosc_rozgrywki = models.IntegerField(
        verbose_name='Długość rozgrywki w minutach', validators=[MinValueValidator(1)]  # Nie krócej niż minuta
    )

    # Cena za 24h wypożyczenia
    cena_za_24h = models.DecimalField(max_digits=4, decimal_places=2, verbose_name='Cena za 24h wypożyczenia')

    # Kaucja za wypożyczenie gry
    kaucja = models.DecimalField(max_digits=4, decimal_places=2, verbose_name='Kaucja za wypożyczenie gry')

    def __str__(self):
        return self.nazwa_gry