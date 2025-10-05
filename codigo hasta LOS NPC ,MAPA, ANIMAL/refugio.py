import pygame
import constantes
import csv
import os
from colisiones_refugio import ColisionesRefugio
from camara import Camara  # Importamos la clase Camara


class Refugio:
    def __init__(self, personaje):
        """Inicializa el refugio, cargando mapa, colisiones, tiles y cámara."""
        self.personaje = personaje
        self.colisiones_refugio = ColisionesRefugio()  # Colisiones específicas del refugio
        self.colisiones = self.colisiones_refugio  # Esto soluciona tu error
        # Cargar el mapa del refugio desde el CSV
        self.mapa_refugio = self.cargar_mapa_refugio()
        self.map_tiles = self.mapa_refugio

        # Cargar las colisiones del mapa
        self.colisiones_refugio.cargar_colisiones(self.mapa_refugio)

        # Cargar las imágenes de los tiles del refugio
        self.tile_list_refugio = self.cargar_tiles_refugio()

        # Instanciar la cámara para el refugio
        ancho_refugio = constantes.COLUMNAS_REFUGIO * constantes.CUADRICULA_TAMAÑO
        alto_refugio = constantes.FILAS_REFUGIO * constantes.CUADRICULA_TAMAÑO
        self.camara_refugio = Camara(ancho_refugio, alto_refugio)

    def cargar_tiles_refugio(self):
        """Carga las imágenes de los tiles del refugio desde la carpeta correspondiente."""
        tile_list = []
        ruta_tiles = os.path.join("recursos", "imagenes", "caracteres", "tiles_refugio")

        print("Ruta completa donde se buscan los tiles del refugio:")
        print(os.path.abspath(ruta_tiles))

        for i in range(1, constantes.TILE_REFUGIO + 1):  # Ej. 1 a 200
            ruta_imagen = os.path.join(ruta_tiles, f"refugio_{i}.png")
            if os.path.exists(ruta_imagen):
                imagen = pygame.image.load(ruta_imagen).convert_alpha()
                imagen = pygame.transform.scale(imagen, (constantes.CUADRICULA_TAMAÑO, constantes.CUADRICULA_TAMAÑO))
                tile_list.append(imagen)
            else:
                tile_list.append(None)  # Previene errores si falta una imagen
                print(f"No se encontró la imagen: {ruta_imagen}")
        return tile_list

    def cargar_mapa_refugio(self):
        """Carga el mapa del refugio desde un archivo CSV y lo convierte a una matriz de enteros."""
        word_data = []
        ruta_nivel = os.path.join("recursos", "imagenes", "caracteres", "niveles", "niveles_refugio.csv")

        # Inicializa la matriz vacía con valores por defecto
        for _ in range(constantes.FILAS_REFUGIO):
            filas = [0] * constantes.COLUMNAS_REFUGIO
            word_data.append(filas)

        # Lee y reemplaza con los valores del archivo CSV
        try:
            with open(ruta_nivel, newline='') as archivo:
                reader = csv.reader(archivo, delimiter=';')  # Usa el delimitador correcto
                for x, fila in enumerate(reader):
                    for y, columna in enumerate(fila):
                        word_data[x][y] = int(columna)
        except Exception as e:
            print(f"Error al leer el archivo de nivel del refugio: {e}")
        return word_data

    def dibujar(self, ventana):
        """Dibuja el mapa del refugio tile por tile en la ventana."""
        # Obtener el desplazamiento de la cámara para el refugio
        scroll = self.camara_refugio.camara_rect
        
        for y, fila in enumerate(self.mapa_refugio):
            for x, tile in enumerate(fila):
                if 0 <= tile < len(self.tile_list_refugio):
                    imagen_tile = self.tile_list_refugio[tile]
                    if imagen_tile:
                        ventana.blit(imagen_tile, (x * constantes.CUADRICULA_TAMAÑO - scroll.x,
                            y * constantes.CUADRICULA_TAMAÑO - scroll.y))
                else:
                    print(f"Tile fuera de rango: {tile} en posición ({x},{y})")

    def actualizar(self):
        """Actualizar eventos internos del refugio, como NPCs o lógica adicional."""
        # Aquí podrías añadir más lógica, como la interacción con NPCs.
        pass

    def actualizar_cam(self):
        """Actualizar la cámara del refugio."""
        self.camara_refugio.update(self.personaje)  # Usamos el personaje para actualizar la cámara
