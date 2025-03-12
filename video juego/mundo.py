#MUNDO

import pygame
import constantes

class Mundo:
    def __init__(self, archivo_mapa):
        """Carga el mapa desde un archivo de texto."""
        self.mapa = []
        with open(archivo_mapa, "r") as archivo:
            for linea in archivo:
                self.mapa.append(linea.strip())

        self.tile_pasto = pygame.image.load("imagenes/pasto.png")
        self.tile_roca = pygame.image.load("imagenes/roca.png")

        self.tile_pasto = pygame.transform.scale(self.tile_pasto, (constantes.TAMANO_CELDA, constantes.TAMANO_CELDA))
        self.tile_roca = pygame.transform.scale(self.tile_roca, (constantes.TAMANO_CELDA, constantes.TAMANO_CELDA))

    def es_transitable(self, x, y):
        """Verifica si una posición es transitable en el mapa."""
        if 0 <= y < len(self.mapa) and 0 <= x < len(self.mapa[y]):
            return self.mapa[y][x] == "0"  # "0" es suelo transitable
        return False

    def dibujar(self, ventana, personaje):
        """Dibuja el mapa en la pantalla con desplazamiento de cámara."""
        desplazamiento_x = personaje.mapa_x * constantes.TAMANO_CELDA - constantes.ANCHO_VENTANA // 2
        desplazamiento_y = personaje.mapa_y * constantes.TAMANO_CELDA - constantes.ALTO_VENTANA // 2

        for y, fila in enumerate(self.mapa):
            for x, tile in enumerate(fila):
                pos_x = x * constantes.TAMANO_CELDA - desplazamiento_x
                pos_y = y * constantes.TAMANO_CELDA - desplazamiento_y

                if 0 <= pos_x < constantes.ANCHO_VENTANA and 0 <= pos_y < constantes.ALTO_VENTANA:
                    if tile == "0":
                        ventana.blit(self.tile_pasto, (pos_x, pos_y))
                    elif tile == "1":
                        ventana.blit(self.tile_roca, (pos_x, pos_y))
