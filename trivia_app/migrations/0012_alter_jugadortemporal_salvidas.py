# Generated by Django 4.2.5 on 2023-11-29 02:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trivia_app', '0011_jugadortemporal_salvidas'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jugadortemporal',
            name='Salvidas',
            field=models.IntegerField(default=10),
        ),
    ]