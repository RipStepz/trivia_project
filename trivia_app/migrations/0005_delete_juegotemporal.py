# Generated by Django 4.2.5 on 2023-11-27 03:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trivia_app', '0004_jugadortemporal_rename_jugador_jugadorpermanente_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='JuegoTemporal',
        ),
    ]
