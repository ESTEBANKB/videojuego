import pygame

def mostrar_pantalla_inicio(ventana, fuente):
    mostrando_inicio = True
    while mostrando_inicio:
        ventana.fill((0, 0, 0))  # Fondo negro
        img_titulo = fuente.render("S.E.A - Saving species on an adventure", True, (255, 255, 255))
        img_mensaje = fuente.render("Presiona ENTER para jugar", True, (255, 255, 255))

        ventana.blit(img_titulo, (200, 250))
        ventana.blit(img_mensaje, (250, 300))
        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False  # Salir del juego
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
                return True  # Continuar al juego
