#mundo
import pygame
import constantes

class Mundo:
    def __init__(self):
        """Inicializa la estructura del mundo con una lista de tiles."""
        self.map_tiles = []

    def process_data(self, data, tile_list):
        """Procesa la matriz del mundo y genera los tiles."""
        self.level_length = len(data)
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile >= 0:  # Verificar que sea un índice válido
                    image = tile_list[tile]
                    image_rect = image.get_rect()
                    image_x = x * constantes.CUADRICULA_TAMAÑO
                    image_y = y * constantes.CUADRICULA_TAMAÑO
                    image_rect.topleft = (image_x, image_y)
                    tile_data = [image, image_rect]
                    self.map_tiles.append(tile_data)

    def draw(self, surface):
        """Dibuja los tiles del mundo en la superficie del juego."""
        for tile in self.map_tiles:
            surface.blit(tile[0], tile[1])
