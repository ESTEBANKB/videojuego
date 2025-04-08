import pygame
import random
from items import Item
import constantes

# Convertimos los índices de tiles sólidos en coordenadas (columna, fila)
TILES_SOLIDOS_COORDS = {(i % constantes.COLUMNAS, i // constantes.COLUMNAS) for i in constantes.TILES_SOLIDOS}

def generar_monedas(cantidad, animacion_list):
    """Genera monedas en posiciones aleatorias evitando los tiles sólidos."""
    grupo_monedas = pygame.sprite.Group()

    for _ in range(cantidad):
        while True:
            # Generar posición aleatoria en la cuadrícula
            columna = random.randint(0, constantes.COLUMNAS - 1)
            fila = random.randint(0, constantes.FILAS - 1)

            # Verificar que la posición no sea un tile sólido
            if (columna, fila) not in TILES_SOLIDOS_COORDS:
                # Convertir coordenadas de la cuadrícula a píxeles
                x = columna * constantes.CUADRICULA_TAMAÑO
                y = fila * constantes.CUADRICULA_TAMAÑO

                print(f"Moneda en: ({x}, {y})")  # Depuración
                moneda = Item(x, y, animacion_list)
                grupo_monedas.add(moneda)
                break  # Salir del bucle cuando encuentra una posición válida

    return grupo_monedas
