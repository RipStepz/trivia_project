# trivia_app/models.py
from django.db import models

class Pregunta(models.Model):
    enunciado = models.CharField(max_length=255)
    opcion_mala = models.CharField(max_length=100)
    puntaje_mala = models.IntegerField(default=1)
    opcion_media = models.CharField(max_length=100)
    puntaje_media = models.IntegerField(default=2)
    opcion_buena = models.CharField(max_length=100)
    puntaje_buena = models.IntegerField(default=3)

class JugadorTemporal(models.Model):
    nombre = models.CharField(max_length=50)
    puntaje = models.IntegerField(default=0)

class JugadorPermanente(models.Model):
    nombre = models.CharField(max_length=50)
    puntaje = models.IntegerField(default=0)

    def __str__(self):
        return self.nombre

class PreguntaBaja(models.Model):
    enunciado = models.CharField(max_length=255)
    opcion_mala = models.CharField(max_length=100)
    puntaje_mala = models.IntegerField(default=1)
    opcion_media = models.CharField(max_length=100)
    puntaje_media = models.IntegerField(default=2)
    opcion_buena = models.CharField(max_length=100)
    puntaje_buena = models.IntegerField(default=3)

    def __str__(self):
        return self.enunciado

class PreguntaMedia(models.Model):
    enunciado = models.CharField(max_length=255)
    opcion_mala = models.CharField(max_length=100)
    puntaje_mala = models.IntegerField(default=1)
    opcion_media = models.CharField(max_length=100)
    puntaje_media = models.IntegerField(default=2)
    opcion_buena = models.CharField(max_length=100)
    puntaje_buena = models.IntegerField(default=3)

    def __str__(self):
        return self.enunciado

class PreguntaAlta(models.Model):
    enunciado = models.CharField(max_length=255)
    opcion_mala = models.CharField(max_length=100)
    puntaje_mala = models.IntegerField(default=1)
    opcion_media = models.CharField(max_length=100)
    puntaje_media = models.IntegerField(default=2)
    opcion_buena = models.CharField(max_length=100)
    puntaje_buena = models.IntegerField(default=3)

    def __str__(self):
        return self.enunciado