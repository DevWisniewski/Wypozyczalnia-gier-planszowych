import random
from django.core.management.base import BaseCommand
from games_rental_app.models import BoardGame, Inventory

class Command(BaseCommand):
    help = 'Generuje losową ilość egzemplarzy gier w tabeli Inventory'

    def handle(self, *args, **kwargs):
        for game in BoardGame.objects.all():
            # Losowanie liczby egzemplarzy na podstawie rozkładu
            number = random.choices(
                [1, 2, 3],
                weights=[50, 30, 20],
                k=1
            )[0]

            # Tworzenie odpowiedniej liczby egzemplarzy gry
            for _ in range(number):
                Inventory.objects.create(
                    game=game,
                    is_rented=False
                )

            self.stdout.write(self.style.SUCCESS(f'Wygenerowano {number} egzemplarz(y) gry "{game.name}"'))
