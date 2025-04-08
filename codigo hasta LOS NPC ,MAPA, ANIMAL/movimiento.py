#movimiento 
import constantes
import pygame
import os

# Inicializar Pygame (solo si aún no lo has hecho en tu código principal)
pygame.init()

# Obtener la ruta absoluta del directorio de recursos
RUTA_RECURSOS = os.path.abspath(os.path.join("recursos", "imagenes", "caracteres", "jugador"))

# Diccionario para almacenar las imágenes del personaje por dirección
direcciones = {
    "abajo": ["camina_1.png", "camina_2.png", "camina_3.png", "camina_4.png"],
    "arriba": ["camina_5.png", "camina_6.png", "camina_7.png", "camina_8.png"],
    "derecha": ["camina_9.png", "camina_10.png", "camina_11.png", "camina_12.png"],
    "izquierda": ["camina_13.png", "camina_14.png", "camina_15.png", "camina_16.png"]
}

# Función para cargar imágenes
def cargar_imagenes_personaje():
    """Carga todas las imágenes del personaje, las escala y las organiza por dirección."""
    sprites_personaje = {}
    
    for direccion, imagenes in direcciones.items():
        lista_imagenes = []
        for img in imagenes:
            ruta_completa = os.path.join(RUTA_RECURSOS, img)
            if os.path.exists(ruta_completa):
                imagen = pygame.image.load(ruta_completa).convert_alpha()
                imagen = pygame.transform.scale(imagen, (constantes.ANCHO_PERSONAJE, constantes.ALTO_PERSONAJE))  # Escalar imagen
                lista_imagenes.append(imagen)
            else:
                print(f"⚠️ Imagen no encontrada: {ruta_completa}")
        
        sprites_personaje[direccion] = lista_imagenes

    return sprites_personaje


