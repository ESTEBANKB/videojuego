# inicio.py - Bucle principal mejorado con estructura modular

import pygame
import constantes
from pantalla_inicio import mostrar_pantalla_inicio
from inicializador_juego import InicializadorJuego
from gestor_escenas import TipoEscena
from sistema_pausa_reinicio import SistemaPausaReinicio
from sonidos import SistemaSonido
from pantalla_controles import mostrar_controles
from sistema_misiones import SistemaMisiones

# Porcentaje de energía que recupera el gato al alimentarse
PORCENTAJE_COMIDA_GATO = 0.05  # 5%, cambia este valor para ajustar

def dibujar_texto(ventana, texto, fuente, x, y, color):
    """Función auxiliar para dibujar texto en pantalla"""
    img = fuente.render(texto, True, color)
    ventana.blit(img, (x, y))

def manejar_eventos_npcs(evento, personaje, gestor_escenas, gestor_npcs):
    """Maneja los eventos relacionados con NPCs"""
    if evento.type != pygame.KEYDOWN:
        return
    
    # DEBUG: Agregar monedas con la tecla H
    if evento.key == pygame.K_h:
        personaje.score += 10
        print(f"Monedas actuales: {personaje.score}")  # Para verificar que funciona
        return
    
    escena_actual_obj = gestor_escenas.obtener_escena_actual()
    if gestor_escenas.obtener_tipo_escena_actual() != TipoEscena.MAPA_PRINCIPAL:
        return
    
    # Interacción con NPCs (tecla E)
    if evento.key == pygame.K_e:
        # Verificar colisión con NPC de bienvenida
        if (gestor_npcs.npc_bienvenida and 
            personaje.rect.colliderect(gestor_npcs.npc_bienvenida.rect)):
            if not gestor_npcs.npc_bienvenida.dialogo_activo:
                gestor_npcs.npc_bienvenida.mostrar_dialogo()
        # Verificar colisión con NPC humano
        elif (gestor_npcs.npc_humano and 
              personaje.rect.colliderect(gestor_npcs.npc_humano.rect)):
            if not gestor_npcs.npc_humano.dialogo_activo:
                gestor_npcs.npc_humano.mostrar_dialogo()
        # Verificar colisión con NPC de misión (Rodrigo)
        elif (gestor_npcs.npc_mision and 
              personaje.rect.colliderect(gestor_npcs.npc_mision.rect)):
            refugio_comprado = (hasattr(escena_actual_obj, 'puerta_refugio') and 
                                escena_actual_obj.puerta_refugio.refugio_comprado)
            if hasattr(gestor_npcs.npc_mision, 'mostrar_dialogo'):
                if refugio_comprado and hasattr(gestor_npcs.npc_mision, 'mostrar_dialogo_refugio_comprado'):
                    gestor_npcs.npc_mision.mostrar_dialogo_refugio_comprado()
                else:
                    gestor_npcs.npc_mision.mostrar_dialogo()
        # Verificar colisión con NPC de información
        elif (gestor_npcs.npc_informacion and 
              personaje.rect.colliderect(gestor_npcs.npc_informacion.rect)):
            if not gestor_npcs.npc_informacion.dialogo_activo:
                gestor_npcs.npc_informacion.mostrar_dialogo()
    
    # Avanzar diálogos (tecla P)
    elif evento.key == pygame.K_p:
        gestor_npcs.manejar_evento_tecla(evento)

def manejar_cambios_escena(teclas, personaje, gestor_escenas, ventana):
    """Maneja los cambios entre escenas"""
    escena_actual_obj = gestor_escenas.obtener_escena_actual()
    tipo_escena_actual = gestor_escenas.obtener_tipo_escena_actual()
    
    # Cambio al refugio desde mapa principal
    if tipo_escena_actual == TipoEscena.MAPA_PRINCIPAL:
        if hasattr(escena_actual_obj, 'puerta_refugio'):
            # Solo verificar entrada si no está comprado o si tiene suficientes monedas
            if not escena_actual_obj.puerta_refugio.refugio_comprado:
                if personaje.score >= escena_actual_obj.puerta_refugio.monedas_requeridas:
                    if escena_actual_obj.puerta_refugio.verificar_entrada(personaje):
                        if teclas[pygame.K_z]:
                            personaje.score -= escena_actual_obj.puerta_refugio.monedas_requeridas
                            escena_actual_obj.puerta_refugio.refugio_comprado = True
                            # Hacer visible al gato solo aquí
                            if hasattr(escena_actual_obj, 'gestor_npcs') and escena_actual_obj.gestor_npcs.gato:
                                gato = escena_actual_obj.gestor_npcs.gato
                                gato.visible = True
                                gato.fue_rescatado = False
                                gato.siguiendo = False
                            print(f"Monedas restantes después de comprar el refugio: {personaje.score}")
                            
                            # APARICIÓN DEL VENDEDOR
                            if hasattr(escena_actual_obj, 'gestor_npcs') and escena_actual_obj.gestor_npcs.npc_vendedor is None:
                                from npc_vendedor import NPCVendedor
                                escena_actual_obj.gestor_npcs.npc_vendedor = NPCVendedor()
                            
                            if hasattr(escena_actual_obj, 'gestor_npcs') and escena_actual_obj.gestor_npcs.gato:
                                gato = escena_actual_obj.gestor_npcs.gato
                                # Al comprar el refugio, el gato aparece en la posición inicial y es visible
                                gato.rect.x = 2430
                                gato.rect.y = 600
                                gato.visible = True
                                gato.fue_rescatado = False
                                gato.siguiendo = False
                                if not hasattr(escena_actual_obj, 'gato_posicion_mapa'):
                                    escena_actual_obj.gato_posicion_mapa = None
                                if not hasattr(escena_actual_obj, 'gato_posicion_refugio'):
                                    escena_actual_obj.gato_posicion_refugio = None
                                if not gato.siguiendo:
                                    escena_actual_obj.gato_posicion_mapa = (gato.rect.x, gato.rect.y)
                                    gato.visible = False
                                else:
                                    gato.visible = True
                                    mostrar_mensaje_gato(ventana)
                            # Actualizar el estado del refugio en el NPC de bienvenida
                            if hasattr(escena_actual_obj, 'gestor_npcs') and escena_actual_obj.gestor_npcs.npc_bienvenida:
                                escena_actual_obj.gestor_npcs.npc_bienvenida.actualizar_estado_refugio(True)
                            gestor_escenas.cambiar_escena(TipoEscena.REFUGIO, personaje)
                            # Al entrar al refugio, restaurar la posición del gato en el refugio
                            refugio_obj = gestor_escenas.obtener_escena_actual()
                            if hasattr(refugio_obj, 'gestor_npcs') and refugio_obj.gestor_npcs.gato:
                                gato = refugio_obj.gestor_npcs.gato
                                if gato.fue_rescatado:
                                    if gato.siguiendo:
                                        # Si está siguiendo, ponerlo cerca del personaje y visible
                                        gato.rect.x = personaje.rect.x + 50
                                        gato.rect.y = personaje.rect.y
                                        gato.visible = True
                                    else:
                                        # Solo aparece si ya fue rescatado y tiene posición guardada
                                        if hasattr(refugio_obj, 'gato_posicion_refugio') and refugio_obj.gato_posicion_refugio:
                                            gato.rect.x, gato.rect.y = refugio_obj.gato_posicion_refugio
                                            gato.visible = True
                                        else:
                                            gato.visible = False
                                else:
                                    gato.visible = False

                            # Sumar 15 monedas solo la primera vez que el gato entra al refugio
                            if hasattr(refugio_obj, 'gestor_npcs') and refugio_obj.gestor_npcs.gato:
                                gato = refugio_obj.gestor_npcs.gato
                                if not hasattr(gato, 'moneda_entregada') or not gato.moneda_entregada:
                                    personaje.score += 15
                                    gato.moneda_entregada = True  # Para que no se repita
                                    print('¡Has encontrado al gato! +15 monedas')
                                    # Mostrar mensaje en pantalla
                                    fuente_mensaje = pygame.font.Font(None, 36)
                                    mostrar_mensaje_mision(ventana, fuente_mensaje)
            else:
                # Si ya está comprado, solo verificar entrada
                if escena_actual_obj.puerta_refugio.verificar_entrada(personaje):
                    if teclas[pygame.K_z]:
                        if hasattr(escena_actual_obj, 'gestor_npcs') and escena_actual_obj.gestor_npcs.gato:
                            gato = escena_actual_obj.gestor_npcs.gato
                            if not hasattr(escena_actual_obj, 'gato_posicion_mapa'):
                                escena_actual_obj.gato_posicion_mapa = None
                            if not hasattr(escena_actual_obj, 'gato_posicion_refugio'):
                                escena_actual_obj.gato_posicion_refugio = None
                            if not gato.siguiendo:
                                escena_actual_obj.gato_posicion_mapa = (gato.rect.x, gato.rect.y)
                                gato.visible = False
                            else:
                                gato.visible = True
                                mostrar_mensaje_gato(ventana)
                        gestor_escenas.cambiar_escena(TipoEscena.REFUGIO, personaje)
                        # Al entrar al refugio, restaurar la posición del gato en el refugio
                        refugio_obj = gestor_escenas.obtener_escena_actual()
                        if hasattr(refugio_obj, 'gestor_npcs') and refugio_obj.gestor_npcs.gato:
                            gato = refugio_obj.gestor_npcs.gato
                            if gato.fue_rescatado:
                                if gato.siguiendo:
                                    # Si está siguiendo, ponerlo cerca del personaje y visible
                                    gato.rect.x = personaje.rect.x + 50
                                    gato.rect.y = personaje.rect.y
                                    gato.visible = True
                                else:
                                    # Solo aparece si ya fue rescatado y tiene posición guardada
                                    if hasattr(refugio_obj, 'gato_posicion_refugio') and refugio_obj.gato_posicion_refugio:
                                        gato.rect.x, gato.rect.y = refugio_obj.gato_posicion_refugio
                                        gato.visible = True
                                    else:
                                        gato.visible = False
    
    # Salida del refugio al mapa principal
    elif tipo_escena_actual == TipoEscena.REFUGIO and teclas[pygame.K_ESCAPE]:
        personaje.rect.x = 460  # Coordenada X específica
        personaje.rect.y = 300  # Coordenada Y específica
        refugio_obj = escena_actual_obj
        if hasattr(refugio_obj, 'gestor_npcs') and refugio_obj.gestor_npcs.gato:
            gato = refugio_obj.gestor_npcs.gato
            if not hasattr(refugio_obj, 'gato_posicion_refugio'):
                refugio_obj.gato_posicion_refugio = None
            if not hasattr(refugio_obj, 'gato_posicion_mapa'):
                refugio_obj.gato_posicion_mapa = None
            if not gato.siguiendo:
                refugio_obj.gato_posicion_refugio = (gato.rect.x, gato.rect.y)
            else:
                gato.visible = True
        gestor_escenas.cambiar_escena(TipoEscena.MAPA_PRINCIPAL, personaje)
        mapa_obj = gestor_escenas.obtener_escena_actual()
        if hasattr(mapa_obj, 'gestor_npcs') and mapa_obj.gestor_npcs.gato:
            gato = mapa_obj.gestor_npcs.gato
            if not gato.siguiendo:
                if not gato.fue_rescatado:
                    # Solo mostrar en posición inicial si nunca fue rescatado
                    gato.rect.x = 2430
                    gato.rect.y = 600
                    gato.visible = True
                else:
                    # Si ya fue rescatado, no mostrarlo en el mapa principal
                    gato.visible = False
            else:
                # Si está siguiendo, ponerlo cerca del personaje y visible
                gato.rect.x = personaje.rect.x + 50
                gato.rect.y = personaje.rect.y
                gato.visible = True
        if hasattr(mapa_obj, 'camara'):
            mapa_obj.camara.update(personaje)

def actualizar_juego(teclas, personaje, gestor_escenas, gestor_npcs, sistema_sonido, ventana):
    """Actualiza la lógica del juego según la escena activa"""
    tipo_escena_actual = gestor_escenas.obtener_tipo_escena_actual()
    escena_actual_obj = gestor_escenas.obtener_escena_actual()
    
    if not escena_actual_obj:
        return
    
    # Manejar cambios de escena
    manejar_cambios_escena(teclas, personaje, gestor_escenas, ventana)
    
    # Actualizar escena actual
    if tipo_escena_actual == TipoEscena.MAPA_PRINCIPAL:
        escena_actual_obj.actualizar(teclas)
        # Verificar entrada a la puerta continuamente
        if hasattr(escena_actual_obj, 'puerta_refugio'):
            escena_actual_obj.puerta_refugio.verificar_entrada(personaje)
        
        # Actualizar NPC de información
        if hasattr(escena_actual_obj, 'gestor_npcs') and escena_actual_obj.gestor_npcs.npc_informacion:
            escena_actual_obj.gestor_npcs.npc_informacion.actualizar(personaje, teclas)
        
        # Reproducir sonido de pasos si el personaje se está moviendo
        if (teclas[pygame.K_w] or teclas[pygame.K_s] or 
            teclas[pygame.K_a] or teclas[pygame.K_d] or
            teclas[pygame.K_UP] or teclas[pygame.K_DOWN] or
            teclas[pygame.K_LEFT] or teclas[pygame.K_RIGHT]):
            sistema_sonido.reproducir_pasos()
    elif tipo_escena_actual == TipoEscena.REFUGIO:
        escena_actual_obj.actualizar(teclas)

def dibujar_juego(ventana, fuente, personaje, gestor_escenas, barra_energia_gato_permanente, comida_disponible):
    """Dibuja todos los elementos del juego"""
    # Limpiar pantalla
    ventana.fill(constantes.VERDE)
    
    # Obtener escena actual
    escena_actual_obj = gestor_escenas.obtener_escena_actual()
    tipo_escena_actual = gestor_escenas.obtener_tipo_escena_actual()
    
    if not escena_actual_obj:
        return
    
    # Dibujar escena
    escena_actual_obj.dibujar(ventana)
    
    # Dibujar personaje con cámara apropiada
    if hasattr(escena_actual_obj, 'camara'):
        ventana.blit(
            personaje.imagenes[personaje.direccion_actual][personaje.indice_imagen], 
            escena_actual_obj.camara.aplicar(personaje)
        )
        
        # Dibujar gato si existe
        if hasattr(escena_actual_obj, 'gato'):
            escena_actual_obj.gato.dibujar(ventana, escena_actual_obj.camara)
        
        # Dibujar NPCs y sus diálogos
        if hasattr(escena_actual_obj, 'gestor_npcs'):
            # Dibujar NPC de información y su diálogo
            if escena_actual_obj.gestor_npcs.npc_informacion:
                escena_actual_obj.gestor_npcs.npc_informacion.dibujar(ventana, escena_actual_obj.camara)
            
            # Dibujar NPC vendedor y su diálogo
            if escena_actual_obj.gestor_npcs.npc_vendedor:
                escena_actual_obj.gestor_npcs.npc_vendedor.dibujar(ventana, escena_actual_obj.camara)
            
            # Dibujar indicadores de interacción de NPCs
            escena_actual_obj.gestor_npcs.dibujar_indicadores_interaccion(ventana, escena_actual_obj.camara, personaje)
    
    # Dibujar UI
    dibujar_texto(ventana, f"Monedas: {personaje.score}", fuente, 650, 5, (255, 255, 0))
    
    # Mostrar el contador de comida SIEMPRE
    dibujar_texto(ventana, f"COMIDA = {comida_disponible}", fuente, 650, 35, (255, 255, 255))
    
    # Dibujar barra de energía del gato en la parte superior SOLO si corresponde
    if barra_energia_gato_permanente and hasattr(escena_actual_obj, 'gestor_npcs') and escena_actual_obj.gestor_npcs.gato:
        gato = escena_actual_obj.gestor_npcs.gato
        energia = gato.energia
        energia_max = gato.energia_max
        barra_ancho = 150
        barra_alto = 18
        x = 10
        y = 40  # Debajo de las monedas
        pygame.draw.rect(ventana, (60, 60, 60), (x, y, barra_ancho, barra_alto))
        energia_actual = int(barra_ancho * (energia / energia_max))
        pygame.draw.rect(ventana, (0, 255, 0), (x, y, energia_actual, barra_alto))
        pygame.draw.rect(ventana, (0, 0, 0), (x, y, barra_ancho, barra_alto), 2)
        fuente_barra = pygame.font.Font(None, 28)
        texto = fuente_barra.render(f"Energía Gato: {energia}/{energia_max}", True, (255, 255, 255))
        ventana.blit(texto, (x + 10, y - 22))
    
    # Instrucciones según la escena
    if tipo_escena_actual == TipoEscena.REFUGIO:
        dibujar_texto(ventana, "Presiona ESC para salir del refugio", fuente, 10, 50, (255, 255, 255))

def mostrar_mensaje_gato(ventana):
    """Muestra el mensaje sobre el estado del gato"""
    # Crear un fondo semitransparente
    overlay = pygame.Surface((constantes.ANCHO_VENTANA, constantes.ALTO_VENTANA))
    overlay.set_alpha(180)
    overlay.fill((0, 0, 0))
    ventana.blit(overlay, (0, 0))
    
    # Configurar fuente y mensajes
    fuente_mensaje = pygame.font.Font(None, 32)
    mensaje1 = "¡ALERTA! El gato muestra signos de maltrato:"
    mensaje2 = "Tiene heridas visibles, golpes y desnutrición severa."
    mensaje3 = "Necesitará cuidados especiales y atención veterinaria."
    mensaje4 = "Tendremos que cuidarlo mucho para ayudarlo a recuperarse."
    
    # Crear superficies para cada línea
    superficie_mensaje1 = fuente_mensaje.render(mensaje1, True, (255, 0, 0))  # Rojo para alerta
    superficie_mensaje2 = fuente_mensaje.render(mensaje2, True, (255, 255, 255))
    superficie_mensaje3 = fuente_mensaje.render(mensaje3, True, (255, 255, 255))
    superficie_mensaje4 = fuente_mensaje.render(mensaje4, True, (255, 255, 255))
    
    # Calcular dimensiones del recuadro
    padding = 40
    ancho_max = max(superficie_mensaje1.get_width(), superficie_mensaje2.get_width(),
                   superficie_mensaje3.get_width(), superficie_mensaje4.get_width())
    alto_total = superficie_mensaje1.get_height() * 4 + padding * 3
    
    # Crear el recuadro
    recuadro = pygame.Surface((ancho_max + padding * 2, alto_total + padding * 2))
    recuadro.fill((50, 50, 50))  # Color de fondo del recuadro
    
    # Dibujar borde del recuadro
    pygame.draw.rect(recuadro, (255, 0, 0), (0, 0, recuadro.get_width(), recuadro.get_height()), 3)
    
    # Calcular posiciones centradas
    x = (constantes.ANCHO_VENTANA - recuadro.get_width()) // 2
    y = (constantes.ALTO_VENTANA - recuadro.get_height()) // 2
    
    # Dibujar el recuadro
    ventana.blit(recuadro, (x, y))
    
    # Dibujar los mensajes dentro del recuadro
    ventana.blit(superficie_mensaje1, (x + padding, y + padding))
    ventana.blit(superficie_mensaje2, (x + padding, y + padding * 2 + superficie_mensaje1.get_height()))
    ventana.blit(superficie_mensaje3, (x + padding, y + padding * 3 + superficie_mensaje1.get_height() * 2))
    ventana.blit(superficie_mensaje4, (x + padding, y + padding * 4 + superficie_mensaje1.get_height() * 3))
    
    # Actualizar la pantalla
    pygame.display.flip()
    # Esperar 3 segundos para que se pueda leer el mensaje
    pygame.time.wait(3000)

def mostrar_mensaje_mision(ventana, fuente):
    mensaje1 = "¡FELICITACIONES!"
    mensaje2 = "Cumpliste tu primera misión."
    mensaje3 = "Ahora toma estas 15 monedas de recompensa."

    # Renderizar textos
    img1 = fuente.render(mensaje1, True, (0, 255, 0))
    img2 = fuente.render(mensaje2, True, (255, 255, 255))
    img3 = fuente.render(mensaje3, True, (255, 255, 0))

    # Fondo
    ancho = max(img1.get_width(), img2.get_width(), img3.get_width()) + 40
    alto = img1.get_height() + img2.get_height() + img3.get_height() + 60
    fondo = pygame.Surface((ancho, alto))
    fondo.set_alpha(220)
    fondo.fill((0, 0, 0))

    # Posición centrada
    ancho_ventana, alto_ventana = ventana.get_size()
    x = (ancho_ventana - ancho) // 2
    y = (alto_ventana - alto) // 2

    ventana.blit(fondo, (x, y))
    ventana.blit(img1, (x + 20, y + 10))
    ventana.blit(img2, (x + 20, y + 30 + img1.get_height()))
    ventana.blit(img3, (x + 20, y + 50 + img1.get_height() + img2.get_height()))
    pygame.display.flip()
    pygame.time.wait(3500)  # 3.5 segundos

def mostrar_pantalla_game_over(ventana, fuente_grande, fuente_normal, fuente_pequena):
    ventana.fill((0, 0, 0))  # Fondo negro

    # Mensajes
    texto_game_over = "¡Game Over!"
    texto_motivo = "No cuidaste bien de los animales rescatados."
    texto_reiniciar = "Presiona R para reiniciar."

    # Renderizar textos
    img_game_over = fuente_grande.render(texto_game_over, True, (255, 0, 0))
    img_motivo = fuente_normal.render(texto_motivo, True, (255, 255, 255))
    img_reiniciar = fuente_pequena.render(texto_reiniciar, True, (255, 255, 0))

    # Calcular posiciones centradas
    ancho_ventana, alto_ventana = ventana.get_size()
    x_centro = ancho_ventana // 2

    ventana.blit(img_game_over, (x_centro - img_game_over.get_width() // 2, 150))
    ventana.blit(img_motivo, (x_centro - img_motivo.get_width() // 2, 250))
    ventana.blit(img_reiniciar, (x_centro - img_reiniciar.get_width() // 2, 350))

    pygame.display.flip()

def mostrar_pantalla_ganar(ventana, fuente_grande, fuente_normal, fuente_pequena):
    ventana.fill((0, 0, 0))  # Fondo negro

    texto_felicidades = "¡FELICITACIONES!"
    texto_adoptado = "¡Tu gato fue adoptado!"
    texto_ganaste = "¡GANASTE!"

    img_felicidades = fuente_grande.render(texto_felicidades, True, (0, 255, 0))
    img_adoptado = fuente_normal.render(texto_adoptado, True, (255, 255, 255))
    img_ganaste = fuente_pequena.render(texto_ganaste, True, (255, 255, 0))

    ancho_ventana, alto_ventana = ventana.get_size()
    x_centro = ancho_ventana // 2

    ventana.blit(img_felicidades, (x_centro - img_felicidades.get_width() // 2, 150))
    ventana.blit(img_adoptado, (x_centro - img_adoptado.get_width() // 2, 250))
    ventana.blit(img_ganaste, (x_centro - img_ganaste.get_width() // 2, 350))

    pygame.display.flip()
    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.KEYDOWN or evento.type == pygame.QUIT:
                esperando = False

def main():
    # Inicializar Pygame
    pygame.init()
    pygame.mixer.init()
    
    # Crear ventana
    ventana = pygame.display.set_mode((constantes.ANCHO_VENTANA, constantes.ALTO_VENTANA))
    pygame.display.set_caption("S.E.A - Salva, Educa, Adopta")
    
    # Crear fuente
    fuente = pygame.font.Font(None, 36)
    
    # Inicializar sistema de sonido
    sistema_sonido = SistemaSonido()
    
    # Inicializar sistema de pausa
    sistema_pausa = SistemaPausaReinicio(ventana, fuente)
    
    # Inicializar sistema de misiones
    sistema_misiones = SistemaMisiones()
    
    # Mostrar pantalla de inicio
    if not mostrar_pantalla_inicio(ventana, fuente):
        return
    
    # Inicializar juego
    inicializador = InicializadorJuego()
    personaje, gestor_escenas, gestor_npcs = inicializador.inicializar_completo()
    
    # Variables de control
    ejecutando = True
    reloj = pygame.time.Clock()
    mostrar_barra_energia_gato = False
    game_over = False
    gano_juego = False
    tiempo_inicio_gato = None
    comida_disponible = 2
    
    # Variables para mensajes temporales
    mostrar_mensaje_alimentar = False
    tiempo_mensaje_alimentar = 0
    DURACION_MENSAJE_ALIMENTAR = 2000  # milisegundos
    mostrar_mensaje_sin_comida = False
    tiempo_mensaje_sin_comida = 0
    DURACION_MENSAJE_SIN_COMIDA = 2000  # milisegundos
    
    # Variables para el temporizador de energía del gato
    tiempo_ultimo_descuento = pygame.time.get_ticks()
    intervalo_descuento = 30000 # 30 segundos en milisegundos
    
    # Al iniciar, el gato no es visible ni interactivo hasta comprar el refugio
    if hasattr(gestor_npcs, 'gato') and gestor_npcs.gato:
        gestor_npcs.gato.visible = False
        gestor_npcs.gato.fue_rescatado = False
        gestor_npcs.gato.siguiendo = False
        gestor_npcs.gato.energia = 100  # Energía inicial en 100
        gestor_npcs.gato.energia_max = 100  # Asegurar que la energía máxima también sea 100
    
    # Al inicio del main, agrega la variable de control
    barra_energia_gato_permanente = False
    
    # Bucle principal
    while ejecutando:
        # Obtener teclas presionadas
        teclas = pygame.key.get_pressed()
        
        # Manejar eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            
            if sistema_pausa.obtener_salida_solicitada():
                ejecutando = False
                continue
            
            if game_over:
                if evento.type == pygame.KEYDOWN and evento.key == pygame.K_r:
                    # Reiniciar el juego
                    inicializador = InicializadorJuego()
                    personaje, gestor_escenas, gestor_npcs = inicializador.inicializar_completo()
                    sistema_pausa.reiniciar_estado()
                    barra_energia_gato_permanente = False  # Reiniciar la barra de energía
                    game_over = False
                    comida_disponible = 2
                    # Asegurar que el gato esté invisible al reiniciar
                    if hasattr(gestor_npcs, 'gato') and gestor_npcs.gato:
                        gestor_npcs.gato.visible = False
                        gestor_npcs.gato.fue_rescatado = False
                        gestor_npcs.gato.siguiendo = False
                        gestor_npcs.gato.energia = 100
                        gestor_npcs.gato.energia_max = 100
                    continue
            else:
                # Manejar eventos del sistema de pausa
                sistema_pausa.manejar_eventos(evento)
                
                # Solo procesar eventos del juego si no está pausado
                if not sistema_pausa.esta_pausado():
                    # Manejar eventos de NPCs
                    manejar_eventos_npcs(evento, personaje, gestor_escenas, gestor_npcs)
                    
                    # --- INTEGRACIÓN DIÁLOGO VENDEDOR ---
                    if hasattr(gestor_npcs, 'npc_vendedor') and gestor_npcs.npc_vendedor:
                        if gestor_npcs.npc_vendedor.dialogo_activo:
                            comida_disponible, sigue_dialogo = gestor_npcs.npc_vendedor.manejar_evento_dialogo(evento, personaje, comida_disponible)
                            # Solo hacer continue si el vendedor sigue activo
                            if gestor_npcs.npc_vendedor.dialogo_activo:
                                continue
                        elif gestor_npcs.npc_vendedor.mostrar_interaccion and evento.type == pygame.KEYDOWN and evento.key == pygame.K_e:
                            gestor_npcs.npc_vendedor.iniciar_dialogo()
                            continue
                    
                    # Manejar eventos del gato
                    if hasattr(gestor_npcs, 'gato') and gestor_npcs.gato:
                        gato = gestor_npcs.gato
                        if evento.type == pygame.KEYDOWN:
                            if evento.key == pygame.K_q and gato.visible and not gato.fue_rescatado:
                                gato.fue_rescatado = True
                                gato.siguiendo = True
                                mostrar_barra_energia_gato = True
                                print("Gato rescatado y siguiendo al jugador")
                            elif evento.key == pygame.K_r and gato.siguiendo:
                                gato.siguiendo = False
                                mostrar_barra_energia_gato = False
                                print("Gato soltado")
                            elif evento.key == pygame.K_y and gato.siguiendo:
                                if comida_disponible > 0:
                                    energia_extra = int(gato.energia_max * 0.05)  # 5% de energía
                                    gato.energia = min(gato.energia + energia_extra, gato.energia_max)
                                    comida_disponible -= 1
                                    mostrar_mensaje_alimentar = True
                                    tiempo_mensaje_alimentar = pygame.time.get_ticks()
                                    print(f"Gato alimentado. Energía: {gato.energia}/{gato.energia_max}")
                                    print(f"Comida restante: {comida_disponible}")
                                else:
                                    mostrar_mensaje_sin_comida = True
                                    tiempo_mensaje_sin_comida = pygame.time.get_ticks()
                                    print("No hay comida disponible")
        
        # Siempre enviar eventos KEYUP a gestor_npcs
        if evento.type == pygame.KEYUP:
            gestor_npcs.manejar_evento_tecla(evento)
        
        # Verificar reinicio solicitado
        if sistema_pausa.obtener_reinicio_solicitado():
            # Reiniciar el juego
            inicializador = InicializadorJuego()
            personaje, gestor_escenas, gestor_npcs = inicializador.inicializar_completo()
            sistema_pausa.reiniciar_estado()
            barra_energia_gato_permanente = False  # Reiniciar la barra de energía
            # Asegurar que el gato esté invisible al reiniciar
            if hasattr(gestor_npcs, 'gato') and gestor_npcs.gato:
                gestor_npcs.gato.visible = False
                gestor_npcs.gato.fue_rescatado = False
                gestor_npcs.gato.siguiendo = False
                gestor_npcs.gato.energia = 100
                gestor_npcs.gato.energia_max = 100
            continue
        
        # Antes de llamar a dibujar_juego, activa la barra si el gato empieza a seguir
        if hasattr(gestor_npcs, 'gato') and gestor_npcs.gato:
            gato = gestor_npcs.gato
            if not barra_energia_gato_permanente and gato.siguiendo:
                print("¡El gato empezó a seguirte! Mostrando barra de energía.")
                barra_energia_gato_permanente = True
        
        # Solo actualizar el juego si no está pausado y no está en Game Over ni en victoria
        if not sistema_pausa.esta_pausado() and not game_over and not gano_juego:
            actualizar_juego(teclas, personaje, gestor_escenas, gestor_npcs, sistema_sonido, ventana)
            
            # Descontar energía al gato cada 30 segundos
            tiempo_actual = pygame.time.get_ticks()
            if tiempo_actual - tiempo_ultimo_descuento >= intervalo_descuento:
                if hasattr(gestor_npcs, 'gato') and gestor_npcs.gato:
                    gato = gestor_npcs.gato
                    descuento = int(gato.energia_max * 0.05)  # 5% de energía
                    gato.energia = max(0, gato.energia - descuento)
                tiempo_ultimo_descuento = tiempo_actual
            
            # Verificar Game Over por energía del gato
            if hasattr(gestor_npcs, 'gato') and gestor_npcs.gato:
                gato = gestor_npcs.gato
                if gato.siguiendo and gato.energia <= 0:
                    game_over = True
                    print("Game Over - El gato ha perdido toda su energía")
            
            # Lógica de victoria: cuidar al gato 5 minutos sin que su energía llegue a 0
            if hasattr(gestor_npcs, 'gato') and gestor_npcs.gato:
                gato = gestor_npcs.gato
                # Inicia el tiempo solo la primera vez que el gato aparece
                if gato.visible and tiempo_inicio_gato is None:
                    import time
                    tiempo_inicio_gato = time.time()
                # Comprobar victoria solo si el gato está visible y hay tiempo de inicio
                if gato.visible and not gano_juego and gato.energia > 0 and tiempo_inicio_gato is not None:
                    import time
                    tiempo_transcurrido = time.time() - tiempo_inicio_gato
                    if tiempo_transcurrido >= 300:  # 5 minutos
                        gano_juego = True
        
        # Dibujar
        dibujar_juego(ventana, fuente, personaje, gestor_escenas, barra_energia_gato_permanente, comida_disponible)
        
        # Dibujar sistema de pausa
        sistema_pausa.dibujar_overlay_pausa()
        sistema_pausa.dibujar_indicador_pausa()
        
        # Dibujar mensaje temporal de alimentación
        if mostrar_mensaje_alimentar and not game_over:
            fuente_mensaje = pygame.font.Font(None, 32)
            mensaje = "¡Buen trabajo! Alimentaste al gato."
            superficie = fuente_mensaje.render(mensaje, True, (255, 255, 0))
            fondo = pygame.Surface((superficie.get_width() + 40, superficie.get_height() + 20))
            fondo.set_alpha(200)
            fondo.fill((0, 0, 0))
            x = (constantes.ANCHO_VENTANA - fondo.get_width()) // 2
            y = 120
            ventana.blit(fondo, (x, y))
            ventana.blit(superficie, (x + 20, y + 10))
            if pygame.time.get_ticks() - tiempo_mensaje_alimentar > DURACION_MENSAJE_ALIMENTAR:
                mostrar_mensaje_alimentar = False
        
        # Dibujar mensaje temporal de falta de comida
        if mostrar_mensaje_sin_comida and not game_over:
            fuente_mensaje = pygame.font.Font(None, 32)
            mensaje = "No cuentas con la comida para alimentar al gato, busca más."
            superficie = fuente_mensaje.render(mensaje, True, (255, 80, 80))
            fondo = pygame.Surface((superficie.get_width() + 40, superficie.get_height() + 20))
            fondo.set_alpha(200)
            fondo.fill((0, 0, 0))
            x = (constantes.ANCHO_VENTANA - fondo.get_width()) // 2
            y = 170
            ventana.blit(fondo, (x, y))
            ventana.blit(superficie, (x + 20, y + 10))
            if pygame.time.get_ticks() - tiempo_mensaje_sin_comida > DURACION_MENSAJE_SIN_COMIDA:
                mostrar_mensaje_sin_comida = False
        
        # Dibujar Game Over si corresponde
        if game_over:
            mostrar_pantalla_game_over(ventana, fuente, fuente, fuente)
        
        # Actualizar pantalla
        pygame.display.flip()
        
        # Controlar FPS
        reloj.tick(60)
        
        if gano_juego:
            fuente_grande = pygame.font.Font(None, 80)
            fuente_normal = pygame.font.Font(None, 40)
            fuente_pequena = pygame.font.Font(None, 36)
            mostrar_pantalla_ganar(ventana, fuente_grande, fuente_normal, fuente_pequena)
            ejecutando = False
            continue
    
    # Guardar progreso antes de salir
    sistema_misiones.guardar_progreso()
    
    # Finalizar Pygame
    pygame.quit()

if __name__ == "__main__":
    main()