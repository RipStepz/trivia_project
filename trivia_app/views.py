# trivia_app/views.py
from django.shortcuts import render, redirect
from .models import Pregunta, JugadorTemporal, JugadorPermanente, PreguntaBaja, PreguntaMedia, PreguntaAlta
from django.http import HttpResponse
from django.db import connections

# def obtener_categoria(puntaje, numero_pregunta):

#     if numero_pregunta <= 5:    
#         return Pregunta
    
#     if 5 < numero_pregunta < 10:
#         if  0 <= puntaje < 5:
#             return PreguntaBaja
#         elif 5 <= puntaje < 10:
#             return PreguntaMedia
#         elif 10 <= puntaje < 15:
#             return PreguntaAlta
        
#     if 10 <= numero_pregunta < 15:
#         if 15 <= puntaje < 20:
#             return PreguntaBaja
#         elif 20 <= puntaje < 25:
#             return PreguntaMedia
#         elif 25 <= puntaje < 30:
#             return PreguntaAlta
#     if 15 <= numero_pregunta < 20:
#         if 30 <= puntaje < 35:
#             return PreguntaBaja
#         elif 35 <= puntaje < 40:
#             return PreguntaMedia
#         elif 40 <= puntaje < 45:
#             return PreguntaAlta
#     if 20 <= numero_pregunta < 25:
#         if 45 <= puntaje < 50:
#             return PreguntaBaja
#         elif 50 <= puntaje < 55:
#             return PreguntaMedia
#         elif 55 <= puntaje <= 60:
#             return PreguntaAlta
    
#     if 25 <= numero_pregunta:
#         if 60 <= puntaje < 65:
#             return PreguntaBaja
#         elif 65 <= puntaje < 70:
#             return PreguntaMedia
#         elif 70 <= puntaje <= 75:
#             return PreguntaAlta
    
#     # En caso de que ninguna condición anterior sea verdadera, retornamos Pregunta por defecto
#     return Pregunta
    

# def obtener_preguntas_categoria(request, numero_pregunta):
#     jugador_temporal_id = request.session.get('jugador_temporal_id')
#     puntaje_acumulado = request.session.get('puntaje_acumulado', 0)
#     cantidad_preguntas = request.session.get('cantidad_preguntas', 0)

#     # Obtener la categoría actual del jugador
#     categoria_actual = obtener_categoria(puntaje_acumulado, cantidad_preguntas)

#     # Obtener las preguntas de la categoría correspondiente
#     preguntas_categoria = categoria_actual.objects.all()

#     if request.method == 'POST':
#         pregunta_actual_id = request.POST['numero_pregunta']
#         pregunta_actual = preguntas_categoria.get(id=pregunta_actual_id)
#         opcion_seleccionada = request.POST['respuesta_' + str(pregunta_actual.id)]

#         # Lógica para manejar las respuestas (similar a la versión anterior)
#         if opcion_seleccionada in ['mala', 'media', 'buena']:
#             if opcion_seleccionada == 'mala':
#                 puntaje_acumulado += pregunta_actual.puntaje_mala
#             elif opcion_seleccionada == 'media':
#                 puntaje_acumulado += pregunta_actual.puntaje_media
#             elif opcion_seleccionada == 'buena':
#                 puntaje_acumulado += pregunta_actual.puntaje_buena

#             request.session['puntaje_acumulado'] = puntaje_acumulado

#             # Actualizamos el puntaje acumulado en la base de datos temporal
#             jugador_temporal = JugadorTemporal.objects.get(id=jugador_temporal_id)
#             jugador_temporal.puntaje = puntaje_acumulado
#             jugador_temporal.save()

#             # Incrementar la cantidad de preguntas respondidas
#             cantidad_preguntas += 1
#             request.session['cantidad_preguntas'] = cantidad_preguntas

#             # Redirigimos a la próxima pregunta si aún no hemos llegado a la pregunta 30
#             if cantidad_preguntas < 5000:
#                 return redirect('obtener_preguntas_categoria', numero_pregunta=cantidad_preguntas + 1)
#             else:
#                 # Si hemos respondido todas las preguntas, vamos a la página de finalización
#                 return redirect('finalizar_juego')

#     # Resto de la lógica para mostrar la pregunta actual
#     pregunta_actual = preguntas_categoria.get(id=numero_pregunta)
#     return render(request, 'preguntas.html', {'preguntas': [pregunta_actual], 'numero_pregunta': numero_pregunta})


def obtener_categoria(puntaje):

    if 0 <= puntaje < 5:
        return PreguntaBaja
    
    elif 5 <= puntaje < 10:
        return PreguntaMedia
    
    elif 10 <= puntaje < 15:
        return PreguntaAlta
    
    elif 15 <= puntaje < 20:
        return PreguntaBaja
    
    elif 20 <= puntaje < 25:
        return PreguntaMedia
    
    elif 25 <= puntaje < 30:
        return PreguntaAlta
    
    elif 30 <= puntaje < 35:
        return PreguntaBaja
    
    elif 35 <= puntaje < 40:
        return PreguntaMedia
    
    elif 40 <= puntaje < 45:
        return PreguntaAlta

    elif 45 <= puntaje < 50:
        return PreguntaBaja
    
    elif 50 <= puntaje < 55:
        return PreguntaMedia
    
    elif 55 <= puntaje < 60:
        return PreguntaAlta
    
    elif 60 <= puntaje < 65:
        return PreguntaBaja
    
    elif 65 <= puntaje < 70:
        return PreguntaMedia
    
    elif 70 <= puntaje < 75:
        return PreguntaAlta
    
    elif 75 <= puntaje < 80:
        return PreguntaBaja
    
    elif 80 <= puntaje < 85:
        return PreguntaMedia
    
    elif 85 <= puntaje < 90:
        return PreguntaAlta
   
        
      

def obtener_preguntas_categoria(request, numero_pregunta):
    jugador_temporal_id = request.session.get('jugador_temporal_id')
    puntaje_acumulado = request.session.get('puntaje_acumulado', 0)

    # Obtener la categoría actual del jugador
    categoria_actual = obtener_categoria(puntaje_acumulado)

    # Obtener las preguntas de la categoría correspondiente
    preguntas_categoria = categoria_actual.objects.all()

    if request.method == 'POST':
        pregunta_actual_id = request.POST['numero_pregunta']
        pregunta_actual = preguntas_categoria.get(id=pregunta_actual_id)
        opcion_seleccionada = request.POST['respuesta_' + str(pregunta_actual.id)]

        # Lógica para manejar las respuestas (similar a la versión anterior)
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
            jugador_temporal.puntaje = puntaje_acumulado
            jugador_temporal.save()

            # Redirigimos a la próxima pregunta si aún no hemos llegado a la pregunta 30
            if int(pregunta_actual_id) < 30:
                return redirect('obtener_preguntas_categoria', numero_pregunta=int(pregunta_actual_id) + 1)
            else:
                # Si hemos respondido todas las preguntas, vamos a la página de finalización
                return redirect('finalizar_juego')

    # Resto de la lógica para mostrar la pregunta actual
    pregunta_actual = preguntas_categoria.get(id=numero_pregunta)
    return render(request, 'preguntas.html', {'preguntas': [pregunta_actual], 'numero_pregunta': numero_pregunta})

def inicio(request):
    if request.method == 'POST':
        nombre_jugador = request.POST['nombre']

        # Cierra todas las conexiones a la base de datos temporal
        connections['default'].close()
        
        # Borra la información temporal antes de crear un nuevo jugador temporal
        JugadorTemporal.objects.all().delete()

        jugador_temporal = JugadorTemporal.objects.create(nombre=nombre_jugador, puntaje=0)
        request.session['jugador_temporal_id'] = jugador_temporal.id
        request.session['puntaje_acumulado'] = 0
        return redirect('obtener_preguntas_categoria', numero_pregunta=1)

    return render(request, 'inicio.html')

def finalizar_juego(request):
    jugador_temporal_id = request.session.get('jugador_temporal_id')

    if jugador_temporal_id:
        jugador_temporal = JugadorTemporal.objects.get(id=jugador_temporal_id)
        puntaje_acumulado = jugador_temporal.puntaje

        # Asegúrate de guardar el puntaje en la base de datos permanente antes de borrar el jugador temporal
        jugador_permanente, created = JugadorPermanente.objects.get_or_create(nombre=jugador_temporal.nombre)
        jugador_permanente.puntaje += puntaje_acumulado
        jugador_permanente.save()

        # Obtén el leaderboard (los primeros 5 jugadores ordenados por puntaje descendente)
        leaderboard = JugadorPermanente.objects.order_by('-puntaje')[:5]

        # Limpia la información temporal después de completar las 30 preguntas
        request.session.pop('jugador_temporal_id', None)

        # Renderiza la página final con la información del jugador y el leaderboard
        return render(request, 'finalizar_juego.html', {'jugador_temporal': jugador_temporal, 'leaderboard': leaderboard})
    else:
        # Maneja el caso en que no se encuentra un jugador temporal
        return render(request, 'error_sin_jugador_temporal.html')