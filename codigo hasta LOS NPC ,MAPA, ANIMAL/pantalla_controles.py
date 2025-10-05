import pygame
import constantes

def mostrar_controles(ventana, fuente, mensaje_inferior=None, color_fondo=(50, 50, 50), alpha_fondo=200):
    """Muestra las instrucciones de control sobre el juego"""
    # Crear superficie semi-transparente para el fondo del texto
    fondo = pygame.Surface((constantes.ANCHO_VENTANA - 100, constantes.ALTO_VENTANA - 100))
    fondo.set_alpha(alpha_fondo)
    fondo.fill(color_fondo)
    ventana.blit(fondo, (50, 50))
    
    # Título
    titulo = fuente.render("CONTROLES", True, (255, 255, 255))
    titulo_rect = titulo.get_rect(center=(constantes.ANCHO_VENTANA // 2, 80))
    ventana.blit(titulo, titulo_rect)
    
    # Definir las acciones y teclas
    controles = [
        ("Moverse", "WASD o"),
        ("Interactuar con NPC", "E"),
        ("Recoger animales", "Q"),
        ("Soltar animales", "R"),
        ("Alimentar animales", "Y"),
        ("Entrar al refugio", "Z"),
        ("Salir del refugio", "ESC"),
        ("Pausar juego / Menú principal", "ENTER")
    ]

    # Calcular el ancho máximo de cada columna y de la ilustración
    max_ancho_accion = max(fuente.size(accion)[0] for accion, _ in controles)
    max_ancho_tecla = max(fuente.size(tecla)[0] for _, tecla in controles)
    ancho_flechas = 60  # Ancho fijo de la ilustración
    espacio_columnas = 120  # Más espacio entre columnas
    espacio_flechas = 15    # Más espacio entre texto y flechas

    # El bloque a centrar es: columna acción + espacio + columna tecla + espacio + flechas
    ancho_total = max_ancho_accion + espacio_columnas + max_ancho_tecla + espacio_flechas + ancho_flechas
    x_inicio = (constantes.ANCHO_VENTANA - ancho_total) // 2
    y_inicial = 140

    # Crear la superficie para las flechas antes del bucle
    flechas_surface = pygame.Surface((60, 60), pygame.SRCALPHA)
    # Dibujar flechas (ajustadas al nuevo tamaño)
    pygame.draw.polygon(flechas_surface, (255, 255, 255), [(30, 6), (24, 18), (36, 18)])  # Flecha arriba
    pygame.draw.polygon(flechas_surface, (255, 255, 255), [(30, 54), (24, 42), (36, 42)])  # Flecha abajo
    pygame.draw.polygon(flechas_surface, (255, 255, 255), [(6, 30), (18, 24), (18, 36)])  # Flecha izquierda
    pygame.draw.polygon(flechas_surface, (255, 255, 255), [(54, 30), (42, 24), (42, 36)])  # Flecha derecha
    pygame.draw.circle(flechas_surface, (255, 255, 255), (30, 30), 3)

    # Dibujar las columnas centradas
    for i, (accion, tecla) in enumerate(controles):
        y = y_inicial + i * 40
        # Acción
        texto_accion = fuente.render(accion, True, (255, 255, 255))
        ventana.blit(texto_accion, (x_inicio, y))
        # Tecla
        x_tecla = x_inicio + max_ancho_accion + espacio_columnas
        texto_tecla = fuente.render(tecla, True, (255, 255, 255))
        ventana.blit(texto_tecla, (x_tecla, y))
        # Flechas solo para la primera fila ("Moverse")
        if i == 0:
            x_flechas = x_tecla + max_ancho_tecla + espacio_flechas
            ventana.blit(flechas_surface, (x_flechas, y - 20))  # Subido 15 píxeles más

    # Mensaje de inicio o personalizado
    y_fondo = 50
    alto_fondo = constantes.ALTO_VENTANA - 100
    y_texto = y_fondo + alto_fondo - 30
    if mensaje_inferior is None:
        mensaje_inferior = "Presiona ESPACIO para comenzar"
    texto_inicio = fuente.render(mensaje_inferior, True, (255, 255, 255))
    texto_rect = texto_inicio.get_rect(center=(constantes.ANCHO_VENTANA // 2, y_texto))
    ventana.blit(texto_inicio, texto_rect) 