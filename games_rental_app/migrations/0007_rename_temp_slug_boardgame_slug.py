# Generated by Django 4.2.10 on 2024-02-28 02:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('games_rental_app', '0006_boardgame_temp_slug'),
    ]

    operations = [
        migrations.RenameField(
            model_name='boardgame',
            old_name='temp_slug',
            new_name='slug',
        ),
    ]