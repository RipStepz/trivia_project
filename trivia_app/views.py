# trivia_app/views.py
from django.shortcuts import render, redirect
from .models import Pregunta, JugadorTemporal, JugadorPermanente
from django.http import HttpResponse

def inicio(request):
    if request.method == 'POST':
        nombre_jugador = request.POST['nombre']
        jugador_temporal = JugadorTemporal.objects.create(nombre=nombre_jugador, puntaje=0)
        request.session['jugador_temporal_id'] = jugador_temporal.id
        request.session['puntaje_acumulado'] = 0
        return redirect('preguntas', numero_pregunta=1)

    return render(request, 'inicio.html')


def preguntas(request, numero_pregunta):
    jugador_temporal_id = request.session.get('jugador_temporal_id')
    puntaje_acumulado = request.session.get('puntaje_acumulado', 0)

    if request.method == 'POST':
        pregunta_actual = Pregunta.objects.get(id=request.POST['numero_pregunta'])
        opcion_seleccionada = request.POST['respuesta_' + str(pregunta_actual.id)]

        if opcion_seleccionada == 'mala':
            puntaje_acumulado += pregunta_actual.puntaje_mala
        elif opcion_seleccionada == 'media':
            puntaje_acumulado += pregunta_actual.puntaje_media
        elif opcion_seleccionada == 'buena':
            puntaje_acumulado += pregunta_actual.puntaje_buena

        request.session['puntaje_acumulado'] = puntaje_acumulado

        jugador_temporal = JugadorTemporal.objects.get(id=jugador_temporal_id)
        jugador_temporal.puntaje_acumulado = puntaje_acumulado
        jugador_temporal.save()

        if numero_pregunta < 30:
            return redirect('preguntas', numero_pregunta=numero_pregunta + 1)
        else:
            return redirect('finalizar_juego')

    else:
        pregunta_actual = Pregunta.objects.get(id=numero_pregunta)
        return render(request, 'preguntas.html', {'preguntas': [pregunta_actual], 'numero_pregunta': numero_pregunta, 'puntaje_acumulado': puntaje_acumulado})


def finalizar_juego(request):
    jugador_temporal_id = request.session.get('jugador_temporal_id')
    puntaje_acumulado = request.session.get('puntaje_acumulado', 0)

    if not jugador_temporal_id:
        return redirect('inicio')

    jugador_temporal = JugadorTemporal.objects.get(id=jugador_temporal_id)

    # Mostrar el puntaje acumulado
    return render(request, 'finalizar_juego.html', {'puntaje_acumulado': puntaje_acumulado, 'jugador_temporal': jugador_temporal})

    # Operaciones en la base de datos permanente
    jugador_permanente, created = JugadorPermanente.objects.get_or_create(nombre=jugador_temporal.nombre)
    jugador_permanente.puntaje += puntaje_acumulado
    jugador_permanente.save()

    # Limpiar la información temporal después de completar las 30 preguntas
    jugador_temporal.delete()
    request.session.pop('jugador_temporal_id', None)
    request.session.pop('puntaje_acumulado', None)


