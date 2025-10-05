# ===============================
# ARCHIVO: generar_items.py (CORREGIDO Y COMPATIBLE)
# ===============================
import pygame
import random
from items import Item
import constantes

# Convertimos los índices de tiles sólidos en coordenadas (columna, fila)
try:
    TILES_SOLIDOS_COORDS = {(i % constantes.COLUMNAS, i // constantes.COLUMNAS) for i in constantes.TILES_SOLIDOS}
except AttributeError:
    # Si no existe TILES_SOLIDOS en constantes, usar valores por defecto
    print("Advertencia: TILES_SOLIDOS no encontrado en constantes, usando valores por defecto")
    TILES_SOLIDOS_COORDS = set()

DISTANCIA_MINIMA = 5  # en celdas/cuadriculas

def muy_cerca_de_otra(col, fil, posiciones_usadas):
    for (c, f) in posiciones_usadas:
        if abs(col - c) < DISTANCIA_MINIMA and abs(fil - f) < DISTANCIA_MINIMA:
            return True
    return False

def generar_monedas(cantidad, animacion_list, sistema_misiones=None):
    """
    Genera monedas en posiciones aleatorias evitando los tiles sólidos y posiciones repetidas y manteniendo una distancia mínima entre monedas.
    Las monedas siempre se generan, pero pueden estar inactivas hasta completar la misión.
    """
    grupo_monedas = pygame.sprite.Group()
    monedas_activas = True
    if sistema_misiones and not sistema_misiones.esta_mision_completada("primera_mision"):
        monedas_activas = False
        print("Las monedas se generarán inactivas hasta completar la primera misión")
    print(f"Generando {cantidad} monedas...")
    posiciones_usadas = set()
    for i in range(cantidad):
        intentos = 0
        max_intentos = 200
        while intentos < max_intentos:
            columna = random.randint(0, constantes.COLUMNAS - 1)
            fila = random.randint(0, constantes.FILAS - 1)
            if ((columna, fila) not in TILES_SOLIDOS_COORDS and
                (columna, fila) not in posiciones_usadas and
                not muy_cerca_de_otra(columna, fila, posiciones_usadas)):
                posiciones_usadas.add((columna, fila))
                x = columna * constantes.CUADRICULA_TAMAÑO
                y = fila * constantes.CUADRICULA_TAMAÑO
                print(f"Moneda {i+1} generada en: ({x}, {y})")
                moneda = Item(x, y, animacion_list)
                moneda.activo = monedas_activas
                grupo_monedas.add(moneda)
                break
            intentos += 1
        if intentos >= max_intentos:
            print(f"No se pudo generar la moneda {i+1} después de {max_intentos} intentos")
    print(f"Total de monedas generadas: {len(grupo_monedas)}")
    print(f"Monedas activas: {'Sí' if monedas_activas else 'No'}")
    return grupo_monedas

def activar_monedas(grupo_monedas):
    """
    Activa todas las monedas del grupo para que sean visibles y coleccionables.
    """
    for moneda in grupo_monedas:
        moneda.activo = True
    print(f"Se han activado {len(grupo_monedas)} monedas")

def generar_monedas_mision(cantidad, animacion_list, posiciones_especificas=None):
    """
    Genera monedas en posiciones específicas después de completar una misión.
    Útil para recompensar al jugador con monedas en lugares específicos.
    """
    grupo_monedas = pygame.sprite.Group()
    
    if posiciones_especificas:
        # Usar posiciones predefinidas
        for i, (x, y) in enumerate(posiciones_especificas):
            if i >= cantidad:
                break
            moneda = Item(x, y, animacion_list)
            moneda.activo = True  # Las monedas de misión siempre están activas
            grupo_monedas.add(moneda)
            print(f"Moneda de misión generada en: ({x}, {y})")
    else:
        # Generar en posiciones aleatorias como método de respaldo
        return generar_monedas(cantidad, animacion_list)
    
    return grupo_monedas

def verificar_monedas_visibles(grupo_monedas):
    """
    Verifica cuántas monedas están activas/visibles en el grupo.
    """
    activas = sum(1 for moneda in grupo_monedas if getattr(moneda, 'activo', True))
    total = len(grupo_monedas)
    print(f"Monedas activas: {activas}/{total}")
    return activas, total