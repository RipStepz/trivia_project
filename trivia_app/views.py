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

        # Asegurémonos de que las opciones sean válidas
        if opcion_seleccionada in ['mala', 'media', 'buena']:
            if opcion_seleccionada == 'mala':
                puntaje_acumulado += pregunta_actual.puntaje_mala
            elif opcion_seleccionada == 'media':
                puntaje_acumulado += pregunta_actual.puntaje_media
            elif opcion_seleccionada == 'buena':
                puntaje_acumulado += pregunta_actual.puntaje_buena

            request.session['puntaje_acumulado'] = puntaje_acumulado

            # Actualizamos el puntaje acumulado en la base de datos temporal
            jugador_temporal = JugadorTemporal.objects.get(id=jugador_temporal_id)
            jugador_temporal.puntaje = puntaje_acumulado  # Corregido el nombre del atributo
            jugador_temporal.save()

            # Redirigimos a la próxima pregunta si aún no hemos llegado a la pregunta 30
            if numero_pregunta < 30:
                return redirect('preguntas', numero_pregunta=numero_pregunta + 1)
            else:
                # Si hemos respondido todas las preguntas, vamos a la página de finalización
                return redirect('finalizar_juego')
    
    # Resto de la lógica para mostrar la pregunta actual
    pregunta_actual = Pregunta.objects.get(id=numero_pregunta)
    return render(request, 'preguntas.html', {'preguntas': [pregunta_actual], 'numero_pregunta': numero_pregunta})


# Función de finalizar juego
def finalizar_juego(request):
    jugador_temporal_id = request.session.get('jugador_temporal_id')

    if jugador_temporal_id:
        jugador_temporal = JugadorTemporal.objects.get(id=jugador_temporal_id)
        puntaje_acumulado = jugador_temporal.puntaje  # Corregido el nombre del atributo

        # Asegúrate de guardar el puntaje en la base de datos permanente antes de borrar el jugador temporal
        jugador_permanente, created = JugadorPermanente.objects.get_or_create(nombre=jugador_temporal.nombre)
        jugador_permanente.puntaje += puntaje_acumulado
        jugador_permanente.save()

        # Limpia la información temporal después de completar las 30 preguntas
        request.session.pop('jugador_temporal_id', None)

        # Utiliza el método pop() solo si deseas eliminar la sesión puntaje_acumulado
        # request.session.pop('puntaje_acumulado', None)

        # Ahora puedes redirigir a la página final con el puntaje acumulado
        return render(request, 'finalizar_juego.html', {'jugador_temporal': jugador_temporal})
    else:
        # Maneja el caso en que no se encuentra un jugador temporal
        return render(request, 'error_sin_jugador_temporal.html')



