# trivia_app/views.py
from django.shortcuts import render, redirect
from .models import Pregunta, JugadorTemporal, JugadorPermanente, PreguntaBaja, PreguntaMedia, PreguntaAlta
from django.http import HttpResponse
from django.db import connections

def obtener_categoria(puntaje_ronda):

    if 0 <= puntaje_ronda <= 3:
        return PreguntaBaja
    
    elif 3 < puntaje_ronda <= 6:
        return PreguntaMedia
    
    elif 6 < puntaje_ronda <= 9:
        return PreguntaAlta
    
def obtener_mensaje_segun_puntaje(puntaje):
    if 15 <= puntaje < 25:
        return "Has tomado malas decisiones para cuidar el medio ambiente."
    elif 25 <= puntaje < 40:
        return "Has tomado decisiones neutras para el medio ambiente."
    elif 40 <= puntaje < 45:
        return "Has cuidado el medio ambiente. ¡Bien hecho!"
    elif puntaje >= 45:
        return "¡Eres un defensor del medio ambiente! Has tomado decisiones excepcionales."
    else:
        return "Mensaje por defecto o sin definir para este rango."
    
def obtener_preguntas_categoria(request, numero_pregunta):
    
    jugador_temporal_id = request.session.get('jugador_temporal_id')
    puntaje_acumulado = request.session.get('puntaje_acumulado', 0)
    puntaje_ronda = request.session.get('PutanjeRonda', 0)
    
    # Obtener las preguntas de la categoría correspondiente

    obtener_numeroP = JugadorTemporal.objects.first()
    NumeroP = obtener_numeroP.Preguntas

    if NumeroP <=3:
        categoria_actual = Pregunta
        preguntas_categoria = categoria_actual.objects.all()
    else:
        jugador_temporal = JugadorTemporal.objects.get(id=jugador_temporal_id)
        comdin = jugador_temporal.Comdin
        categoria_actual = obtener_categoria(comdin)
        preguntas_categoria = categoria_actual.objects.all()
        print("Else categoria")
        print(str(categoria_actual))
      
    
    if request.method == 'POST':
        #print("puntaje ronda:")
        #print(int(puntaje_ronda))
        jugador_temporal = JugadorTemporal.objects.get(id=jugador_temporal_id)
        puntaje_ronda = jugador_temporal.PutanjeRonda
        #print("categoria actual:")
        #print(str(categoria_actual))
        
        pregunta_actual_id = request.POST['numero_pregunta']
        pregunta_actual = preguntas_categoria.get(id=pregunta_actual_id)
        opcion_seleccionada = request.POST['respuesta_' + str(pregunta_actual.id)]
    
        # Lógica para manejar las respuestas (similar a la versión anterior)
        if opcion_seleccionada in ['mala', 'media', 'buena']:
            if opcion_seleccionada == 'mala':
                puntaje_acumulado += pregunta_actual.puntaje_mala
                jugador_temporal = JugadorTemporal.objects.get(id=jugador_temporal_id)
                jugador_temporal.PutanjeRonda += pregunta_actual.puntaje_mala
                jugador_temporal.Preguntas +=1
                jugador_temporal.save()
                
            elif opcion_seleccionada == 'media':
                puntaje_acumulado += pregunta_actual.puntaje_media
                jugador_temporal = JugadorTemporal.objects.get(id=jugador_temporal_id)
                jugador_temporal.PutanjeRonda += pregunta_actual.puntaje_media
                jugador_temporal.Preguntas +=1
                jugador_temporal.save()
            elif opcion_seleccionada == 'buena':
                puntaje_acumulado += pregunta_actual.puntaje_buena
                jugador_temporal = JugadorTemporal.objects.get(id=jugador_temporal_id)
                jugador_temporal.PutanjeRonda += pregunta_actual.puntaje_buena
                jugador_temporal.Preguntas +=1
                jugador_temporal.save()

            request.session['puntaje_acumulado'] = puntaje_acumulado

            # Actualizamos el puntaje acumulado en la base de datos temporal
            jugador_temporal = JugadorTemporal.objects.get(id=jugador_temporal_id)
            jugador_temporal.puntaje = puntaje_acumulado
            jugador_temporal.save()
            
            #jugador_temporal.PutanjeRonda = puntaje_debug
            

            print("puntaje ronda")
            print(int(jugador_temporal.PutanjeRonda))
            print("puntaje acumulado")
            print(puntaje_acumulado)
            # Redirigimos a la próxima pregunta si aún no hemos llegado a la pregunta 30
            if int(pregunta_actual_id) < 15:
                #print(pregunta_actual_id)
                # if int(pregunta_actual_id) == 1:
                #     categoria_actual = Pregunta

                if int(str(pregunta_actual_id)) % 3 ==0:
                    #print("categoria en % 3")
                    Guardar_numeroC = JugadorTemporal.objects.first()
                    Guardar_numeroC.Comdin = jugador_temporal.PutanjeRonda
                    Guardar_numeroC.save()
                    print("puntaje en %3")
                    print(int(jugador_temporal.PutanjeRonda))
                    #print(str(categoria_actual))
                    categoria_actual = obtener_categoria(jugador_temporal.PutanjeRonda)
                    print("categoria en % 3")
                    print(str(categoria_actual))
                    JugadorTemporal.objects.all().update(PutanjeRonda=0)
                    print("puntaje en %3 post borrar")
                    print(int(jugador_temporal.PutanjeRonda))
                    "jugadorTemporal"
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
        # Abrir_flag = JugadorTemporal.objects.first()
        # Abrir_flag.Bool = "True"
        # Abrir_flag.save() 

        jugador_temporal = JugadorTemporal.objects.create(nombre=nombre_jugador, puntaje=0, PutanjeRonda=0, Comdin=0, Preguntas=1)
        request.session['jugador_temporal_id'] = jugador_temporal.id
        request.session['puntaje_acumulado'] = 0
        Abrir_flag = JugadorTemporal.objects.first()
        Abrir_flag.Preguntas = 1
        Abrir_flag.save() 

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

        # Obtener el mensaje según el puntaje
        mensaje = obtener_mensaje_segun_puntaje(puntaje_acumulado)

        # Renderiza la página final con la información del jugador y el leaderboard
        return render(request, 'finalizar_juego.html', {'jugador_temporal': jugador_temporal, 'leaderboard': leaderboard, 'mensaje': mensaje})
    else:
        # Maneja el caso en que no se encuentra un jugador temporal
        return render(request, 'error_sin_jugador_temporal.html')
