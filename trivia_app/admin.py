from django.contrib import admin
from .models import Pregunta

class PreguntaAdmin(admin.ModelAdmin):
    model = Pregunta
    extra = 3  # Puedes ajustar esto según la cantidad de respuestas que quieras añadir por pregunta

admin.site.register(Pregunta, PreguntaAdmin)