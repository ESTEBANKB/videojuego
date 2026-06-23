#pantalla_inicio
import pygame

def mostrar_pantalla_inicio(ventana, fuente):
    mostrando_inicio = True
    while mostrando_inicio:
        ventana.fill((0, 1, 1))  # Fondo negro
        img_titulo = fuente.render("S.E.A - Saving species on an adventure", True, (255, 255, 255)) # Texto blanco
        img_mensaje = fuente.render("Presiona ENTER para jugar", True, (255, 255, 255)) # Texto blanco

        ventana.blit(img_titulo, (200, 250)) # Posiciona el texto
        ventana.blit(img_mensaje, (250, 300)) # Posiciona el mensaje
        pygame.display.flip() # Actualiza la pantalla

        for evento in pygame.event.get(): # Eventos
            if evento.type == pygame.QUIT: # Si se cierra la ventana
                return False  # Salir del juego
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN: # Si se presiona ENTER
                return True  # Continuar al juego
'''def mostrar_historia(ventana, fuente):
    historia = [
        "En un mundo donde los animales están en peligro...",
        "Un héroe inesperado se levanta para protegerlos.",
        "Tu misión: salvar especies en peligro, una aventura a la vez.",
    ]

    texto_actual = ""
    indice_historia = 0
    velocidad_texto = 50  # milisegundos entre letras
    letra_idx = 0
    tiempo_ultima_letra = pygame.time.get_ticks()
    esperando_tecla = False

    while indice_historia < len(historia):
        ventana.fill((0, 0, 0))

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()

        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_a]:  # Si presiona A, adelanta
            if letra_idx < len(historia[indice_historia]):
                letra_idx = len(historia[indice_historia])
                texto_actual = historia[indice_historia]
            else:
                if not esperando_tecla:
                    # Verificar si hay más texto en la lista antes de incrementar el índice
                    if indice_historia + 1 < len(historia):
                            indice_historia += 1
                    texto_actual = ""
                    letra_idx = 0
                    esperando_tecla = True
                    pygame.time.delay(200)  # evitar doble entrada

        # Mostrar texto letra por letra
        if letra_idx < len(historia[indice_historia]):
            if pygame.time.get_ticks() - tiempo_ultima_letra > velocidad_texto:
                texto_actual += historia[indice_historia][letra_idx]
                letra_idx += 1
                tiempo_ultima_letra = pygame.time.get_ticks()
                esperando_tecla = False

        texto_render = fuente.render(texto_actual, True, (255, 255, 255))
        ventana.blit(texto_render, (50, 300))
        pygame.display.flip()
        pygame.time.delay(10)
        
         # Al terminar el diálogo, muestra nuevamente el mensaje de "Presiona ENTER"
    esperando_enter = True
    while esperando_enter:
        ventana.fill((0, 0, 0))
        mensaje = fuente.render("Presiona ENTER para comenzar el juego", True, (255, 255, 255))
        ventana.blit(mensaje, (100, 300))
        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
                esperando_enter = False'''
        

