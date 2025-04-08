#coliciones
import pygame
import constantes
print("Ruta de constantes:", constantes.__file__)  # Muestra de dónde se está importando
print("TILES_SOLIDOS en constantes:", constantes.TILES_SOLIDOS)  # Verifica su contenido


class TileSolido(pygame.sprite.Sprite):
    """Clase para representar tiles sólidos con colisión."""
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((constantes.CUADRICULA_TAMAÑO, constantes.CUADRICULA_TAMAÑO))
        self.image.set_alpha(0)  # Hacer invisible el tile sólido
        self.rect = self.image.get_rect(topleft=(x, y))

class Colisiones:
    def __init__(self):
        self.solid_tiles = pygame.sprite.Group()

    def cargar_colisiones(self, data):
        """Carga los tiles sólidos según la matriz del nivel."""
        for y, fila in enumerate(data):
            for x, tile in enumerate(fila):
                if tile in constantes.TILES_SOLIDOS:  # TILES_SOLIDOS es una lista de tiles con colisión
                    self.solid_tiles.add(TileSolido(x * constantes.CUADRICULA_TAMAÑO, y * constantes.CUADRICULA_TAMAÑO))

    def verificar_colision(self, personaje, eje):
        """Evita que el personaje atraviese los tiles sólidos."""
        for tile in self.solid_tiles:
            if personaje.rect.colliderect(tile.rect):
                if eje == "horizontal":
                    if personaje.vel_x > 0:  # Se mueve a la derecha
                        personaje.rect.right = tile.rect.left
                    elif personaje.vel_x < 0:  # Se mueve a la izquierda
                        personaje.rect.left = tile.rect.right
                elif eje == "vertical":
                    if personaje.vel_y > 0:  # Se mueve hacia abajo
                        personaje.rect.bottom = tile.rect.top
                    elif personaje.vel_y < 0:  # Se mueve hacia arriba
                        personaje.rect.top = tile.rect.bottom
