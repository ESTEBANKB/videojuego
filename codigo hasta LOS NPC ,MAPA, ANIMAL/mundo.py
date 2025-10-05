#mundo 
import pygame
import constantes  # Importamos las constantes definidas en otro archivo, como el tamaño de cada tile
from refugio import Refugio

class Mundo:
    def __init__(self): 
        """Inicializa la estructura del mundo con una lista de tiles."""
        self.map_tiles = []  # Lista donde se almacenarán todos los tiles visibles del mapa
        self.refugio = None  # Inicializamos como None hasta que se detecte la transición
        self.mapa_actual = "principal"  # Mapa actual, por defecto el principal


    def process_data(self, data, tile_list): 
        """Procesa la matriz del mundo y genera los tiles a partir de una lista de imágenes."""
        self.level_length = len(data)  # Guarda la cantidad de filas del nivel (alto del mapa)

        for y, row in enumerate(data):  # Recorremos cada fila (y) del mapa
            for x, tile in enumerate(row):  # Recorremos cada celda (x) de la fila
                if tile >= 0:  # Solo procesamos los valores válidos (descartamos -1 que suele ser vacío)
                    image = tile_list[tile]  # Obtenemos la imagen correspondiente al índice del tile
                    image_rect = image.get_rect()  # Creamos un rectángulo con las dimensiones de la imagen

                    # Calculamos la posición en píxeles del tile multiplicando su posición en la matriz
                    # por el tamaño de cada casilla (definido en las constantes)
                    image_x = x * constantes.CUADRICULA_TAMAÑO
                    image_y = y * constantes.CUADRICULA_TAMAÑO
                    image_rect.topleft = (image_x, image_y)  # Posicionamos el rectángulo en el lugar correcto

                    tile_data = [image, image_rect]  # Creamos una lista que agrupa la imagen con su posición
                    self.map_tiles.append(tile_data)  # Añadimos este tile a la lista general del mundo

    def draw(self, surface):
        """Dibuja todos los tiles del mundo en la superficie del juego."""
        for tile in self.map_tiles:
            surface.blit(tile[0], tile[1])  # Dibuja la imagen del tile en su rectángulo sobre la pantalla 

    def cambiar_a_refugio(self, personaje):
        """Cambia al refugio cuando el personaje entra a la puerta."""
        self.mapa_actual = "refugio"  # Cambiar el mapa actual a refugio
        self.refugio = Refugio(personaje)  # Crear la instancia de Refugio y pasarle el personaje

    def detectar_entrada_refugio(self, personaje):
        """Detecta si el personaje entra en la puerta para cambiar de mapa."""
        # Si el personaje está sobre el tile 312 (X=12, Y=12 por ejemplo) o 313 (X=13, Y=12)
        if personaje.rect.colliderect(pygame.Rect(312 * constantes.CUADRICULA_TAMAÑO, 313 * constantes.CUADRICULA_TAMAÑO, constantes.CUADRICULA_TAMAÑO, constantes.CUADRICULA_TAMAÑO)):
            self.cambiar_a_refugio(personaje)  # Llamamos a la función que cambia al refugio

    def actualizar(self, personaje):
        """Actualiza la lógica del mundo según el mapa actual."""
        if self.mapa_actual == "refugio":
            self.refugio.actualizar()  # Si estamos en el refugio, actualiza las mecánicas del refugio
        else:
            self.detectar_entrada_refugio(personaje)  # En el mapa principal, detecta la entrada al refugio