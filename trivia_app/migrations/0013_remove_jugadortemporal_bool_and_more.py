# Generated by Django 4.2.5 on 2023-11-29 03:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trivia_app', '0012_alter_jugadortemporal_salvidas'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jugadortemporal',
            name='Bool',
        ),
        migrations.RemoveField(
            model_name='jugadortemporal',
            name='Salvidas',
        ),
        migrations.AddField(
            model_name='jugadortemporal',
            name='Comdin',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='jugadortemporal',
            name='Preguntas',
            field=models.IntegerField(default=1),
        ),
    ]
