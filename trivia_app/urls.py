# trivia_app/urls.py
from django.urls import path

# trivia_app/urls.py
from django.urls import path
from .views import inicio, preguntas, finalizar_juego

urlpatterns = [
    path('', inicio, name='inicio'),
    path('preguntas/<int:numero_pregunta>/', preguntas, name='preguntas'),
    path('finalizar-juego/', finalizar_juego, name='finalizar_juego'),
]