#coliciones

# Importa pygame y un módulo personalizado llamado 'constantes'
import pygame
import constantes

# Estas líneas imprimen información útil para depurar:
#print("Ruta de constantes:", constantes.__file__)  # Muestra desde qué archivo se está importando el módulo 'constantes'
#print("TILES_SOLIDOS en constantes:", constantes.TILES_SOLIDOS)  # Muestra el contenido de la lista de tiles sólidos (para verificar que esté cargando bien)

# Clase para representar un tile (cuadro) sólido en el mapa
class TileSolidoRefugio(pygame.sprite.Sprite):
    """Clase para representar tiles sólidos con colisión."""
    def __init__(self, x, y):
        super().__init__()  # Llama al constructor de Sprite
        # Crea una superficie cuadrada del tamaño definido en constantes
        self.image = pygame.Surface((constantes.CUADRICULA_TAMAÑO, constantes.CUADRICULA_TAMAÑO))
        self.image.set_alpha(0)  # La hace completamente invisible (útil para colisiones invisibles)
        # Define el rectángulo de colisión y lo posiciona en (x, y)
        self.rect = self.image.get_rect(topleft=(x, y))

# Clase para gestionar todas las colisiones del juego
class ColisionesRefugio:
    def __init__(self):
        # Crea un grupo de sprites que contendrá todos los tiles sólidos del nivel
        self.solid_tiles = pygame.sprite.Group()

    def cargar_colisiones(self, data):
        """Carga los tiles sólidos según la matriz del nivel."""
        # Recorre cada fila y cada tile en la matriz del mapa
        for y, fila in enumerate(data):
            for x, tile in enumerate(fila):
                # Si el tile actual está en la lista de tiles sólidos
                if tile in constantes.TILES_SOLIDOS_REFUGIO:
                    # Crea un tile sólido en esa posición y lo añade al grupo
                    self.solid_tiles.add(TileSolidoRefugio(x * constantes.CUADRICULA_TAMAÑO, y * constantes.CUADRICULA_TAMAÑO))

    def verificar_colision(self, personaje, eje):
        """Evita que el personaje atraviese los tiles sólidos."""
        # Verifica colisiones entre el personaje y cada tile sólido
        for tile in self.solid_tiles:
            if personaje.rect.colliderect(tile.rect):  # Si hay colisión
                if eje == "horizontal":
                    if personaje.vel_x > 0:  # El personaje se mueve hacia la derecha
                        personaje.rect.right = tile.rect.left  # Detiene su lado derecho justo antes del tile
                    elif personaje.vel_x < 0:  # Se mueve hacia la izquierda
                        personaje.rect.left = tile.rect.right  # Detiene su lado izquierdo justo después del tile
                elif eje == "vertical":
                    if personaje.vel_y > 0:  # Se mueve hacia abajo
                        personaje.rect.bottom = tile.rect.top  # Detiene su parte inferior justo encima del tile
                    elif personaje.vel_y < 0:  # Se mueve hacia arriba
                        personaje.rect.top = tile.rect.bottom  # Detiene su parte superior justo debajo del tile

