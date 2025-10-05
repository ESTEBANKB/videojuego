# cargador_recursos.py - Módulo para cargar todos los recursos del juego

import pygame
import os
import csv
import constantes

def cargar_tiles_mundo():
    """
    Carga todos los tiles del mundo desde la carpeta de recursos.
    
    Returns:
        list: Lista de imágenes de tiles cargadas y escaladas
    """
    tile_list = []
    ruta_mundo = os.path.join("recursos", "imagenes", "caracteres", "tiles")
    
    if not os.path.exists(ruta_mundo):
        print(f"Advertencia: No se encontró la carpeta de tiles en {ruta_mundo}")
        return tile_list
    
    try:
        for x in range(constantes.TILE_TYPES):  
            ruta_tile = os.path.join(ruta_mundo, f"tiles_{x+1}.png")
            
            if os.path.exists(ruta_tile):
                tile_image = pygame.image.load(ruta_tile)
                tile_image = pygame.transform.scale(
                    tile_image, 
                    (constantes.CUADRICULA_TAMAÑO, constantes.CUADRICULA_TAMAÑO)
                )
                tile_list.append(tile_image)
            else:
                print(f"Advertencia: No se encontró el tile tiles_{x+1}.png")
                # Crear un tile de placeholder (cuadrado rojo)
                placeholder = pygame.Surface((constantes.CUADRICULA_TAMAÑO, constantes.CUADRICULA_TAMAÑO))
                placeholder.fill((255, 0, 0))
                tile_list.append(placeholder)
                
        print(f"Tiles cargados: {len(tile_list)}")
        return tile_list
        
    except Exception as e:
        print(f"Error al cargar tiles: {e}")
        return []

def cargar_imagenes_monedas():
    """
    Carga todas las imágenes de monedas para la animación.
    
    Returns:
        list: Lista de imágenes de monedas cargadas y procesadas
    """
    coin_images = []
    ruta_img = os.path.join("recursos", "imagenes", "caracteres", "monedas")
    
    if not os.path.exists(ruta_img):
        print(f"Advertencia: No se encontró la carpeta de monedas en {ruta_img}")
        return coin_images
    
    try:
        for i in range(9):  # Asumiendo 9 frames de animación
            ruta_moneda = os.path.join(ruta_img, f"monedas_{i+1}.png")
            
            if os.path.exists(ruta_moneda):
                img = pygame.image.load(ruta_moneda)
                img = pygame.transform.scale(img, (constantes.ANCHO_MONEDA, constantes.ALTO_MONEDA))
                img.set_colorkey(constantes.COLOR_TRANSPARENTE)
                coin_images.append(img)
            else:
                print(f"Advertencia: No se encontró monedas_{i+1}.png")
                
        print(f"Imágenes de monedas cargadas: {len(coin_images)}")
        return coin_images
        
    except Exception as e:
        print(f"Error al cargar imágenes de monedas: {e}")
        return []

def cargar_nivel_csv(nombre_archivo="nivel_test.csv"):
    """
    Carga los datos del nivel desde un archivo CSV.
    
    Args:
        nombre_archivo (str): Nombre del archivo CSV a cargar
        
    Returns:
        list: Matriz bidimensional con los datos del nivel
    """
    ruta_nivel = os.path.join("recursos", "imagenes", "caracteres", "niveles", nombre_archivo)
    
    # Inicializar matriz con valores por defecto
    word_data = []
    for fila in range(constantes.FILAS):
        filas = [5] * constantes.COLUMNAS  # Tile por defecto
        word_data.append(filas)
    
    if not os.path.exists(ruta_nivel):
        print(f"Advertencia: No se encontró el archivo de nivel en {ruta_nivel}")
        print("Usando datos por defecto")
        return word_data
    
    try:
        with open(ruta_nivel, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            
            for x, fila in enumerate(reader):
                if x >= constantes.FILAS:
                    break
                    
                for y, columna in enumerate(fila):
                    if y >= constantes.COLUMNAS:
                        break
                        
                    try:
                        word_data[x][y] = int(columna)
                    except ValueError:
                        print(f"Advertencia: Valor inválido en posición ({x}, {y}): {columna}")
                        word_data[x][y] = 5  # Valor por defecto
                        
        print(f"Nivel cargado exitosamente desde {nombre_archivo}")
        return word_data
        
    except Exception as e:
        print(f"Error al cargar nivel desde CSV: {e}")
        print("Usando datos por defecto")
        return word_data

def cargar_fuentes():
    """
    Carga las fuentes necesarias para el juego.
    
    Returns:
        dict: Diccionario con las fuentes cargadas
    """
    fuentes = {}
    
    try:
        # Fuente principal
        fuentes['principal'] = pygame.font.Font(None, 36)
        
        # Fuente para títulos
        fuentes['titulo'] = pygame.font.Font(None, 48)
        
        # Fuente pequeña para UI
        fuentes['pequena'] = pygame.font.Font(None, 24)
        
        print("Fuentes cargadas exitosamente")
        
    except Exception as e:
        print(f"Error al cargar fuentes: {e}")
        # Usar fuente por defecto en caso de error
        fuente_default = pygame.font.Font(None, 36)
        fuentes = {
            'principal': fuente_default,
            'titulo': fuente_default,
            'pequena': fuente_default
        }
    
    return fuentes

def verificar_recursos():
    """
    Verifica que todos los recursos necesarios estén disponibles.
    
    Returns:
        dict: Diccionario con el estado de cada recurso
    """
    estado_recursos = {
        'tiles': False,
        'monedas': False,
        'niveles': False,
        'personaje': False
    }
    
    # Verificar tiles
    ruta_tiles = os.path.join("recursos", "imagenes", "caracteres", "tiles")
    estado_recursos['tiles'] = os.path.exists(ruta_tiles)
    
    # Verificar monedas
    ruta_monedas = os.path.join("recursos", "imagenes", "caracteres", "monedas")
    estado_recursos['monedas'] = os.path.exists(ruta_monedas)
    
    # Verificar niveles
    ruta_niveles = os.path.join("recursos", "imagenes", "caracteres", "niveles")
    estado_recursos['niveles'] = os.path.exists(ruta_niveles)
    
    # Verificar imágenes de personaje
    ruta_personaje = os.path.join("recursos", "imagenes", "caracteres", "jugador")
    estado_recursos['personaje'] = os.path.exists(ruta_personaje)
    
    # Mostrar reporte
    print("\n=== Estado de recursos ===")
    for recurso, disponible in estado_recursos.items():
        estado = "✓ Disponible" if disponible else "✗ No encontrado"
        print(f"{recurso.capitalize()}: {estado}")
    print("========================\n")
    
    return estado_recursos

def cargar_todos_los_recursos():
    """
    Función principal que carga todos los recursos del juego.
    
    Returns:
        dict: Diccionario con todos los recursos cargados
    """
    print("Iniciando carga de recursos...")
    
    # Verificar disponibilidad de recursos
    verificar_recursos()
    
    recursos = {
        'tiles': cargar_tiles_mundo(),
        'monedas': cargar_imagenes_monedas(),
        'nivel': cargar_nivel_csv(),
        'fuentes': cargar_fuentes()
    }
    
    print("Carga de recursos completada.")
    return recursos

# Función de utilidad para crear surface de placeholder
def crear_surface_placeholder(ancho, alto, color=(255, 0, 255)):
    """
    Crea una surface de placeholder con el color especificado.
    
    Args:
        ancho (int): Ancho de la surface
        alto (int): Alto de la surface
        color (tuple): Color RGB del placeholder
        
    Returns:
        pygame.Surface: Surface creada
    """
    surface = pygame.Surface((ancho, alto))
    surface.fill(color)
    return surface