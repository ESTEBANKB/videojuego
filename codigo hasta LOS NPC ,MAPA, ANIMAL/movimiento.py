#movimiento 
import constantes
import pygame
import os

# Inicializar Pygame (solo si aún no lo has hecho en tu código principal)
pygame.init()

# Obtener la ruta absoluta del directorio de recursos
# Define la ruta absoluta a la carpeta donde están las imágenes del personaje
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
    sprites_personaje = {} # Diccionario para almacenar las listas de sprites por dirección
    
    for direccion, imagenes in direcciones.items(): # Recorre cada dirección y su lista de archivos de imagen
        lista_imagenes = [] # Lista para guardar las imágenes cargadas y escaladas
        for img in imagenes:
            ruta_completa = os.path.join(RUTA_RECURSOS, img)  # Construye la ruta completa al archivo de imagen
            if os.path.exists(ruta_completa): # Verifica si el archivo existe
                imagen = pygame.image.load(ruta_completa).convert_alpha() # Carga la imagen y la convierte a modo de alpha(TRANSPARENICA)
                imagen = pygame.transform.scale(imagen, (constantes.ANCHO_PERSONAJE, constantes.ALTO_PERSONAJE))  # Escalar imagen
                lista_imagenes.append(imagen) # Agrega la imagen a la lista
            else:
                print(f" Imagen no encontrada: {ruta_completa}") #IMPRIME  un mesndaje si la imagen no se encuentra 
        
        sprites_personaje[direccion] = lista_imagenes # Agrega la lista de imágenes a la estructura de datos principal

    return sprites_personaje # Retorna el diccionario con las imágenes cargadas y escaladas


