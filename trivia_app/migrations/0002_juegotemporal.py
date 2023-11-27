# Generated by Django 4.2.5 on 2023-11-27 02:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trivia_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='JuegoTemporal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jugador', models.CharField(max_length=50)),
                ('puntaje', models.IntegerField(default=0)),
                ('pregunta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trivia_app.pregunta')),
            ],
        ),
    ]
