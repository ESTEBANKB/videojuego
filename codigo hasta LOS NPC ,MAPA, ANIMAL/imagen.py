#imagen
# Importa los módulos necesarios
import pygame  # Librería para desarrollo de videojuegos, útil para trabajar con imágenes, sonido, eventos, etc.
import os      # Módulo para interactuar con el sistema de archivos (carpetas y archivos del sistema)

# Función para escalar una imagen
def escalar_img(image, scale):
    """Escala una imagen al tamaño deseado."""
    w, h = image.get_size()  # Obtiene el ancho (w) y alto (h) de la imagen original
    return pygame.transform.scale(image, (int(w * scale), int(h * scale)))  
    # Escala la imagen multiplicando sus dimensiones por el factor 'scale'

# Función para contar la cantidad de archivos en un directorio
def contar_elementos(directorio):
    """Cuenta el número de archivos en un directorio."""
    return len(os.listdir(directorio)) if os.path.exists(directorio) else 0
    # Si el directorio existe, cuenta los archivos/carpetas dentro usando os.listdir
    # Si no existe, retorna 0

# Función para obtener los nombres de los archivos/carpetas dentro de un directorio
def nombres_carpetas(directorio):
    """Lista los nombres de los archivos dentro de un directorio."""
    return os.listdir(directorio) if os.path.exists(directorio) else []
    # Si el directorio existe, devuelve una lista con los nombres de archivos/carpetas dentro
    # Si no existe, devuelve una lista vacía


