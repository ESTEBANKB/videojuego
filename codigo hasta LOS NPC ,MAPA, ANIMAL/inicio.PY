# inicio.py

import pygame  # Importamos la librería Pygame
import constantes  # Importamos las constantes del juego
from pantalla_inicio import mostrar_pantalla_inicio  # Importamos la función
from personaje import Personaje  # Importamos la clase del personaje
from items import Item  # Importamos la clase de los items
from mundo import Mundo  # Importamos la clase del mundo
from camara import Camara  # Importar la clase de la cámara
from movimiento import cargar_imagenes_personaje  # Importar la función para cargar imágenes del personaje
from generar_items import generar_monedas  # Importamos la nueva función para generar monedas
from colisiones import Colisiones  # Importamos la función para detectar colisiones
from npc import GatoNPC
from humano import NPCHumano
from gato_humano import cargar_imagenes_gato, crear_npc_humano

import os
import csv

# Inicializar Pygame
pygame.init()

# Configuración de la ventana

ventana = pygame.display.set_mode((constantes.ANCHO_VENTANA, constantes.ALTO_VENTANA))
pygame.display.set_caption("S.E.A - Saving species on an adventure")

# Configuración del reloj para controlar los FPS
clock = pygame.time.Clock()

# Definir la fuente de texto
fuente = pygame.font.Font(None, 36)  # Fuente predeterminada de Pygame, tamaño 36
# 🔹 Mostrar la pantalla de inicio antes de comenzar
if not mostrar_pantalla_inicio(ventana, fuente):
    pygame.quit()
    exit()


# Función para dibujar texto en pantalla
def dibujar_texto(texto, fuente, x, y, color):
    img = fuente.render(texto, True, color)
    ventana.blit(img, (x, y))

# Cargar las imágenes del personaje
diccionario_imagenes = cargar_imagenes_personaje()

# Crear el personaje en una posición inicial
personaje = Personaje(550, 550, diccionario_imagenes)


# Cargar imágenes del mundo
tile_list = []
ruta_mundo = os.path.join("recursos", "imagenes", "caracteres", "tiles")

if os.path.exists(ruta_mundo):
    for x in range(constantes.TILE_TYPES):  
        tile_image = pygame.image.load(os.path.join(ruta_mundo, f"tiles_{x+1}.png"))
        tile_image = pygame.transform.scale(tile_image, (constantes.CUADRICULA_TAMAÑO, constantes.CUADRICULA_TAMAÑO))
        tile_list.append(tile_image)






# Cargar imágenes de las monedas
coin_images = []
ruta_img = os.path.join("recursos", "imagenes", "caracteres", "monedas")

if os.path.exists(ruta_img):
    for i in range(9):
        img = pygame.image.load(os.path.join(ruta_img, f"monedas_{i+1}.png"))
        img = pygame.transform.scale(img, (constantes.ANCHO_MONEDA, constantes.ALTO_MONEDA))
        coin_images.append(img)
        img.set_colorkey(constantes.COLOR_TRANSPARENTE)  # Elimina el color de fondo si es necesario
        coin_images.append(img)


  # Cambia 10 por la cantidad deseada de monedas


# Cargar el nivel desde un archivo CSV
word_data = []
ruta_nivel = os.path.join("recursos", "imagenes", "caracteres", "niveles", "nivel_test.csv")

for fila in range(constantes.FILAS):
    filas = [5] * constantes.COLUMNAS
    word_data.append(filas)

# Leer el archivo de niveles
with open(ruta_nivel, newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=';')
    for x, fila in enumerate(reader):
        for y, columna in enumerate(fila):
            word_data[x][y] = int(columna)  # Convertir a entero

# Crear el mundo con la información del nivel
world = Mundo()
world.process_data(word_data, tile_list)

# Cargar colisiones
colisiones = Colisiones()
# Justo antes de colisiones.cargar_colisiones(word_data)
#print("Datos del mundo:", word_data)

colisiones.cargar_colisiones(word_data)

# Crear la cámara con el tamaño del mapa (suponiendo 20x15 tiles)
ancho_mapa = constantes.COLUMNAS * constantes.CUADRICULA_TAMAÑO
alto_mapa = len(world.map_tiles) * constantes.CUADRICULA_TAMAÑO
camara = Camara(ancho_mapa, alto_mapa)

#print(f"Ancho del mapa: {ancho_mapa} px ({constantes.COLUMNAS} tiles)") # para verificar la cantidad de tiles en el mapa

#  Generar monedas en todo el mapa
grupo_item = generar_monedas(10, coin_images)

# Crear NPC humano
npc_humano = crear_npc_humano()  # Llamas a la función y te da una instancia de NPCHumano

tecla_e_presionada = False
tecla_p_presionada = False

# Crear gato y humano-gato
imagenes_gato = cargar_imagenes_gato()  # Carga las imágenes del gato
gato = GatoNPC(2430, 600,imagenes_gato)



# Agregar todos los sprites si usas grupos (opcional)
grupo_npcs = pygame.sprite.Group()
grupo_npcs.add(gato)
grupo_npcs.add(npc_humano)



# Bucle principal del juego
jugando = True
while jugando:  
    clock.tick(constantes.FPS)  # Controla la velocidad del juego

    # Manejo de eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            jugando = False
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_RETURN:
                npc_humano.ocultar_dialogo()  # Cierra el diálogo si se presiona Enter
            
    # Captura de teclas presionadas
    teclas = pygame.key.get_pressed()
    personaje.mover(teclas, colisiones)  # Movimiento del personaje
    
    # Controlar si el personaje está tocando al NPC humano
    tocando_npc = pygame.sprite.collide_rect(personaje, npc_humano)

    if tocando_npc and not npc_humano.dialogo_ya_mostrado:
        npc_humano.mostrar_dialogo()
        npc_humano.dialogo_ya_mostrado = True
    elif not tocando_npc:
        npc_humano.ocultar_dialogo()
        npc_humano.dialogo_ya_mostrado = False

    # Control de diálogo
    if npc_humano.dialogo_activo:
        # Detectar pulsación única de E
        if teclas[pygame.K_e]:
            if not tecla_e_presionada:
                npc_humano.cambiar_respuesta()
                tecla_e_presionada = True
        else:
            tecla_e_presionada = False

        # Detectar pulsación única de P
        if teclas[pygame.K_p]:
            if not tecla_p_presionada:
                npc_humano.actualizar_dialogo()
                tecla_p_presionada = True
        else:
            tecla_p_presionada = False
    # Actualizar la cámara para seguir al personaje
    camara.update(personaje)
    
    # Gato sigue al personaje
    if pygame.sprite.collide_rect(personaje, gato) and not gato.siguiendo:
        gato.siguiendo = True

    gato.actualizar(personaje)
    
    # Dibujar en pantalla
    ventana.fill(constantes.VERDE)  # Fondo de color verde
    #  Dibujar el mundo ajustado a la cámara
    for tile in world.map_tiles:
        ventana.blit(tile[0], camara.aplicar(tile[1]))  # tile[1] ya es un rect

      #  Dibujar el personaje ajustado a la cámara
    ventana.blit(personaje.imagenes[personaje.direccion_actual][personaje.indice_imagen], camara.aplicar(personaje))

    
    for item in grupo_item:
        ventana.blit(item.image, camara.aplicar(item))


    npc_humano.dibujar(ventana, camara)  # Dibujar NPC humano ajustado a la cámara
    gato.dibujar(ventana, camara)  # Dibujar el gato ajustado a la cámara
  

    grupo_item.update(personaje)  # Actualizar los items
    grupo_item.draw(ventana)  # Dibujar items
    
    npc_humano.dibujar_dialogo(ventana)  # Dibujar el cuadro de diálogo del NPC humano si está activo
    
    # Mostrar el puntaje en pantalla
    dibujar_texto(f"Score: {personaje.score}", fuente, 650, 5, (255, 255, 0))
    
    pygame.display.flip()  # Actualiza la pantalla

pygame.quit()
