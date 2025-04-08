#gato_humano

import pygame
from humano import NPCHumano
import constantes

# Cargar imágenes del gato
def cargar_imagenes_gato():
    imagenes= {
        "abajo": [pygame.image.load(f"recursos/imagenes/caracteres/gato/gabajo_{i}.png") for i in range(1, 4)],
        "arriba": [pygame.image.load(f"recursos/imagenes/caracteres/gato/garriba_{i}.png") for i in range(1, 4)],
        "izquierda": [pygame.image.load(f"recursos/imagenes/caracteres/gato/gizquierda_{i}.png") for i in range(1, 4)],
        "derecha": [pygame.image.load(f"recursos/imagenes/caracteres/gato/gderecha_{i}.png") for i in range(1, 4)],
        "quieto": pygame.image.load("recursos/imagenes/caracteres/gato/gquieto.png")
}
    for direccion in imagenes:
            if isinstance(imagenes[direccion], list):
                imagenes[direccion] = [pygame.transform.scale(img, (constantes.CUADRICULA_TAMAÑO, constantes.CUADRICULA_TAMAÑO)) for img in imagenes[direccion]]
            else:
                imagenes[direccion] = pygame.transform.scale(imagenes[direccion], (constantes.CUADRICULA_TAMAÑO, constantes.CUADRICULA_TAMAÑO))

    return imagenes

# Cargar imagen y crear NPC humano
def crear_npc_humano():
    imagen = pygame.image.load("recursos/imagenes/caracteres/humano/humanoo.png")
    imagen = pygame.transform.scale(imagen, (constantes.CUADRICULA_TAMAÑO, constantes.CUADRICULA_TAMAÑO))
    return NPCHumano(600, 780, imagen, "¡Hola! Bienvenido a la isla. Ayuda al gato a encontrar a sus amigos perdidos.")