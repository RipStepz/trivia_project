from django.contrib import admin
from .models import Pregunta, PreguntaBaja, PreguntaMedia, PreguntaAlta

class PreguntaAdmin(admin.ModelAdmin):
    model = Pregunta
    extra = 3  # Puedes ajustar esto según la cantidad de respuestas que quieras añadir por pregunta

class PreguntaBajaAdmin(admin.ModelAdmin):
    model = PreguntaBaja
    extra = 3  # Ajusta según la cantidad de respuestas que quieras añadir por pregunta

class PreguntaMediaAdmin(admin.ModelAdmin):
    model = PreguntaMedia
    extra = 3  # Ajusta según la cantidad de respuestas que quieras añadir por pregunta

class PreguntaAltaAdmin(admin.ModelAdmin):
    model = PreguntaAlta
    extra = 3  # Ajusta según la cantidad de respuestas que quieras añadir por pregunta

admin.site.register(PreguntaBaja, PreguntaBajaAdmin)
admin.site.register(PreguntaMedia, PreguntaMediaAdmin)
admin.site.register(PreguntaAlta, PreguntaAltaAdmin)
admin.site.register(Pregunta, PreguntaAdmin)