#INICIO.PY
import pygame  # Importamos la librería Pygame.
import constantes  # Importamos las constantes desde el archivo separado.
from personaje import Personaje
from mundo import Mundo # Importamos el mundo desde el archivo separado.

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
ventana = pygame.display.set_mode((constantes.ANCHO_VENTANA, constantes.ALTO_VENTANA))
pygame.display.set_caption("S.E.A - Story Entertainment Adventure")

# Configuración del reloj para controlar los FPS
clock = pygame.time.Clock()

# Crear el personaje
personaje = Personaje(1, 1)

#cargar el mundo
mundo = Mundo("mapa.txt")


# Cargar fuente para el texto
pygame.font.init()
fuente = pygame.font.Font(None, 50)

def mostrar_pantalla_inicio():
    """Función para mostrar la pantalla de inicio del juego."""
    ventana.fill(constantes.BLANCO)
    titulo_texto = fuente.render("S.E.A - Presiona ENTER para jugar", True, constantes.NEGRO)
    ventana.blit(titulo_texto, (constantes.ANCHO_VENTANA // 2 - titulo_texto.get_width() // 2, constantes.ALTO_VENTANA // 3))
    pygame.display.flip()



    

# Bucle principal del juego
jugando = True
while jugando:
    clock.tick(constantes.FPS) # 🔹 Controla la velocidad del bucle

    # Manejo de eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            jugando = False

    # Movimiento del personaje
    teclas = pygame.key.get_pressed()
    personaje.mover(teclas,mundo)

    # Dibujar en pantalla
    ventana.fill(constantes.VERDE)  # Fondo verde
    mundo.dibujar(ventana,personaje) # Dibujar el mapa con desplazamiento
    personaje.dibujar(ventana)  # Dibujar personaje


    pygame.display.flip()   # 🔹 Actualiza la pantalla

pygame.quit()
