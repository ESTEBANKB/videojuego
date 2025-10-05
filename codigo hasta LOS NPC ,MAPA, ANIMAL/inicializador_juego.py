# inicializador_juego.py - Carga de recursos y configuración inicial

import pygame
import constantes
import os
import csv
from personaje import Personaje
from gato import PersonajeGato
from mundo import Mundo
from colisiones import Colisiones
from camara import Camara
from movimiento import cargar_imagenes_personaje
from generar_items import generar_monedas
from puerta_refugio import PuertaRefugio
from gestor_npcs import GestorNPCs
from sistema_misiones import SistemaMisiones
from gestor_escenas import GestorEscenas, MapaPrincipal, RefugioMejorado, TipoEscena

class InicializadorJuego:
    """Clase responsable de cargar y configurar todos los recursos del juego"""
    
    def __init__(self):
        self.tile_list = []
        self.coin_images = []
        self.word_data = []
        
    def cargar_tiles_mundo(self):
        """Carga los tiles del mundo"""
        ruta_mundo = os.path.join("recursos", "imagenes", "caracteres", "tiles")
        if os.path.exists(ruta_mundo):
            for x in range(constantes.TILE_TYPES):  
                tile_image = pygame.image.load(os.path.join(ruta_mundo, f"tiles_{x+1}.png"))
                tile_image = pygame.transform.scale(tile_image, (constantes.CUADRICULA_TAMAÑO, constantes.CUADRICULA_TAMAÑO))
                self.tile_list.append(tile_image)
        return self.tile_list
    
    def cargar_imagenes_monedas(self):
        """Carga las imágenes de las monedas"""
        self.coin_images = []  # Asegurarnos de que la lista esté vacía al inicio
        ruta_img = os.path.join("recursos", "imagenes", "caracteres", "monedas")
        print(f"DEBUG: Intentando cargar imágenes de monedas desde: {ruta_img}")
        
        if os.path.exists(ruta_img):
            print("DEBUG: Carpeta de monedas encontrada")
            for i in range(9):
                ruta_moneda = os.path.join(ruta_img, f"monedas_{i+1}.png")
                print(f"DEBUG: Intentando cargar: {ruta_moneda}")
                if os.path.exists(ruta_moneda):
                    try:
                        img = pygame.image.load(ruta_moneda)
                        img = pygame.transform.scale(img, (constantes.ANCHO_MONEDA, constantes.ALTO_MONEDA))
                        img.set_colorkey(constantes.COLOR_TRANSPARENTE)
                        self.coin_images.append(img)
                        print(f"DEBUG: Imagen monedas_{i+1}.png cargada correctamente")
                    except Exception as e:
                        print(f"ERROR al cargar monedas_{i+1}.png: {str(e)}")
                else:
                    print(f"ERROR: No se encontró el archivo: {ruta_moneda}")
        else:
            print(f"ERROR: No se encontró la carpeta de monedas en: {ruta_img}")
        
        print(f"DEBUG: Total de imágenes de monedas cargadas: {len(self.coin_images)}")
        if len(self.coin_images) == 0:
            print("ERROR: No se pudo cargar ninguna imagen de monedas")
        return self.coin_images
    
    def cargar_nivel_csv(self):
        """Carga el nivel desde un archivo CSV"""
        # Inicializar con tiles por defecto
        for fila in range(constantes.FILAS):
            filas = [5] * constantes.COLUMNAS
            self.word_data.append(filas)
        
        # Cargar desde CSV
        ruta_nivel = os.path.join("recursos", "imagenes", "caracteres", "niveles", "nivel_test.csv")
        
        try:
            with open(ruta_nivel, newline='') as csvfile:
                reader = csv.reader(csvfile, delimiter=';')
                for x, fila in enumerate(reader):
                    for y, columna in enumerate(fila):
                        if x < len(self.word_data) and y < len(self.word_data[x]):
                            self.word_data[x][y] = int(columna)
        except FileNotFoundError:
            print(f"Archivo de nivel no encontrado: {ruta_nivel}")
        except Exception as e:
            print(f"Error cargando nivel: {e}")
            
        return self.word_data
    
    def crear_personaje(self):
        """Crea el personaje principal"""
        diccionario_imagenes = cargar_imagenes_personaje()
        return Personaje(550, 550, diccionario_imagenes)
    
    def crear_mundo_y_colisiones(self):
        """Crea el mundo y sistema de colisiones"""
        # Crear mundo
        world = Mundo()
        world.process_data(self.word_data, self.tile_list)
        
        # Crear colisiones
        colisiones = Colisiones()
        colisiones.cargar_colisiones(self.word_data)
        
        return world, colisiones
    
    def crear_camara(self, world):
        """Crea el sistema de cámara"""
        ancho_mapa = constantes.COLUMNAS * constantes.CUADRICULA_TAMAÑO
        alto_mapa = constantes.FILAS * constantes.CUADRICULA_TAMAÑO
        return Camara(ancho_mapa, alto_mapa)
    
    def crear_sistemas_juego(self):
        """Crea los sistemas principales del juego"""
        # Crear sistema de misiones
        sistema_misiones = SistemaMisiones()
        
        # Crear gestor de NPCs
        gestor_npcs = GestorNPCs(sistema_misiones)
        
        return sistema_misiones, gestor_npcs
    
    def crear_items(self, sistema_misiones):
        """Crea los items del juego"""
        # Crear un grupo vacío de monedas que se generará más tarde
        return pygame.sprite.Group()
    
    def crear_puerta_refugio(self, world):
        """Crea el sistema de puerta del refugio"""
        return PuertaRefugio(world, [312, 313])
    
    def inicializar_completo(self):
        """Inicializa todos los componentes del juego"""
        # Cargar imágenes primero
        self.cargar_imagenes()
        print("DEBUG: Imágenes cargadas")
        
        # Crear personaje
        personaje = self.crear_personaje()
        print("DEBUG: Personaje creado")
        
        # Crear sistema de misiones y gestor de NPCs
        sistema_misiones, gestor_npcs = self.crear_sistemas_juego()
        print("DEBUG: Sistema de misiones y gestor de NPCs creados")
        
        # Crear mundo y colisiones
        world, colisiones = self.crear_mundo_y_colisiones()
        print("DEBUG: Mundo y colisiones creados")
        
        # Crear cámara
        camara = self.crear_camara(world)
        print("DEBUG: Cámara creada")
        
        # Crear grupo de monedas
        self.grupo_item = self.crear_items(sistema_misiones)
        print("DEBUG: Grupo de monedas creado")
        
        # Crear puerta del refugio
        puerta_refugio = self.crear_puerta_refugio(world)
        print("DEBUG: Puerta del refugio creada")
        
        # Crear mapa principal
        mapa_principal = MapaPrincipal(personaje, world, colisiones, camara, self.grupo_item, puerta_refugio, gestor_npcs)
        mapa_principal.word_data = self.word_data  # Para poder recargar colisiones
        print("DEBUG: Mapa principal creado")
        
        # Crear refugio
        refugio = RefugioMejorado(personaje)
        refugio.gestor_npcs = gestor_npcs  # Pasar el gestor de NPCs al refugio
        print("DEBUG: Refugio creado")
        
        # Crear gestor de escenas
        gestor_escenas = GestorEscenas()
        gestor_escenas.registrar_escena(TipoEscena.MAPA_PRINCIPAL, mapa_principal)
        gestor_escenas.registrar_escena(TipoEscena.REFUGIO, refugio)
        print("DEBUG: Gestor de escenas creado")
        
        # Pasar el grupo de monedas y las imágenes al NPC de misión
        if gestor_npcs.npc_mision:
            print("DEBUG: Configurando NPC de misión")
            print(f"DEBUG: Número de imágenes de monedas disponibles: {len(self.coin_images)}")
            gestor_npcs.npc_mision.set_grupo_monedas(self.grupo_item)
            gestor_npcs.npc_mision.set_coin_images(self.coin_images)
            gestor_npcs.npc_mision.set_personaje(personaje)
        else:
            print("ERROR: No se encontró el NPC de misión")
        
        # Empezar en el mapa principal
        gestor_escenas.cambiar_escena(TipoEscena.MAPA_PRINCIPAL, personaje)
        
        return personaje, gestor_escenas, gestor_npcs

    def cargar_imagenes(self):
        """Carga todas las imágenes necesarias para el juego"""
        print("DEBUG: Iniciando carga de imágenes")
        self.cargar_tiles_mundo()
        self.cargar_imagenes_monedas()
        self.cargar_nivel_csv()
        print("DEBUG: Carga de imágenes completada")

# FUNCIÓN PARA REINICIAR EL JUEGO (mantiene compatibilidad)
def reiniciar_juego():
    """Reinicia todos los componentes del juego usando el inicializador"""
    print("Reiniciando juego...")
    
    inicializador = InicializadorJuego()
    return inicializador.inicializar_completo()