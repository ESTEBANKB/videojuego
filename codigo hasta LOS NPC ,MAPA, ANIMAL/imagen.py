#imagen 
import pygame
import os


import pygame
import os

def escalar_img(image, scale):
    """Escala una imagen al tamaño deseado."""
    w, h = image.get_size()
    return pygame.transform.scale(image, (int(w * scale), int(h * scale)))

def contar_elementos(directorio):
    """Cuenta el número de archivos en un directorio."""
    return len(os.listdir(directorio)) if os.path.exists(directorio) else 0

def nombres_carpetas(directorio):
    """Lista los nombres de los archivos dentro de un directorio."""
    return os.listdir(directorio) if os.path.exists(directorio) else []


