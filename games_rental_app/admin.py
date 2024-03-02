from django.contrib import admin
from .models import BoardGame, Address, Inventory, Rental, CustomUser

# Rejestracja modeli w panelu administracyjnym
admin.site.register(BoardGame)
admin.site.register(Address)
admin.site.register(Inventory)
admin.site.register(Rental)
admin.site.register(CustomUser)
