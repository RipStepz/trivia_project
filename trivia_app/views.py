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

def pregunta(request, numero_pregunta):
    jugador_temporal_id = request.session.get('jugador_temporal_id')
    puntaje_acumulado = request.session.get('puntaje_acumulado', 0)

    if request.method == 'POST':
        pregunta_actual = Pregunta.objects.get(id=request.POST['numero_pregunta'])
        opcion_seleccionada = request.POST['respuesta_' + str(pregunta_actual.id)]

        puntaje_respuesta = 0  # Inicializamos el puntaje de la respuesta

        if opcion_seleccionada == 'mala':
            puntaje_respuesta = pregunta_actual.puntaje_mala
        elif opcion_seleccionada == 'media':
            puntaje_respuesta = pregunta_actual.puntaje_media
        elif opcion_seleccionada == 'buena':
            puntaje_respuesta = pregunta_actual.puntaje_buena

        puntaje_acumulado += puntaje_respuesta

        request.session['puntaje_acumulado'] = puntaje_acumulado

        jugador_temporal = JugadorTemporal.objects.get(id=jugador_temporal_id)
        jugador_temporal.puntaje_acumulado = puntaje_acumulado
        jugador_temporal.save()

        if numero_pregunta < 30:
            return redirect('preguntas', numero_pregunta=numero_pregunta + 1)
        else:
            jugador_permanente, created = JugadorPermanente.objects.get_or_create(nombre=jugador_temporal.nombre)
            jugador_permanente.puntaje += puntaje_acumulado
            jugador_permanente.save()

            request.session.pop('jugador_temporal_id', None)
            request.session.pop('puntaje_acumulado', None)

            return redirect('finalizar_juego')

    else:
        pregunta_actual = Pregunta.objects.get(id=numero_pregunta)
        return render(request, 'preguntas.html', {'preguntas': [pregunta_actual], 'numero_pregunta': numero_pregunta})


def finalizar_juego(request):
    # Obtener información del jugador temporal
    jugador_temporal_id = request.session.get('jugador_temporal_id')
    puntaje_acumulado = request.session.get('puntaje_acumulado', 0)

    # Validar la existencia del jugador temporal
    if jugador_temporal_id is not None:
        try:
            # Obtener el jugador temporal y su nombre
            jugador_temporal = JugadorTemporal.objects.get(id=jugador_temporal_id)
            nombre_jugador = jugador_temporal.nombre

            # Actualizar el puntaje del jugador temporal
            jugador_temporal.puntaje += puntaje_acumulado
            jugador_temporal.save()

            # Obtener o crear el jugador permanente y actualizar su puntaje
            jugador_permanente, created = JugadorPermanente.objects.get_or_create(nombre=nombre_jugador)
            jugador_permanente.puntaje += puntaje_acumulado
            jugador_permanente.save()

            # Limpiar la información temporal después de completar las 30 preguntas
            request.session.pop('jugador_temporal_id', None)
            request.session.pop('puntaje_acumulado', None)

            # Renderizar el template con la información del jugador
            return render(request, 'finalizar_juego.html', {'nombre_jugador': nombre_jugador, 'puntaje_acumulado': puntaje_acumulado})

        except JugadorTemporal.DoesNotExist:
            # Si no se encuentra un jugador temporal, redirigir a la página de inicio o manejar de otra manera
            return redirect('inicio')

    else:
        # Si no se encuentra un jugador temporal, redirigir a la página de inicio o manejar de otra manera
        return redirect('inicio')


