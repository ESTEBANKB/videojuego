#npc

import pygame

class GatoNPC(pygame.sprite.Sprite):
    def __init__(self, x, y, imagenes):
        super().__init__()
        self.imagenes = imagenes
        self.direccion_actual = "abajo"  # Dirección inicial válida
        self.indice_imagen = 0
        self.image = self.imagenes["quieto"]  # Imagen inicial en estado quieto
        self.rect = self.image.get_rect(topleft=(x, y))
        self.siguiendo = False
        self.velocidad = 3  # Velocidad del gato
        self.tiempo_animacion = 0  # Contador de tiempo para animación
        self.intervalo_animacion = 5  # Número de frames antes de cambiar imagen

    def actualizar(self, personaje):
        if self.siguiendo:
            dx = personaje.rect.x - self.rect.x
            dy = personaje.rect.y - self.rect.y
            distancia = (dx**2 + dy**2) ** 0.5

            if distancia > 40:  # Si está lejos, se mueve
                if abs(dx) > abs(dy):
                    self.direccion_actual = "derecha" if dx > 0 else "izquierda"
                else:
                    self.direccion_actual = "abajo" if dy > 0 else "arriba"

                self.rect.x += self.velocidad if dx > 0 else -self.velocidad
                self.rect.y += self.velocidad if dy > 0 else -self.velocidad

                # Controlar velocidad de animación
                self.tiempo_animacion += 1
                if self.tiempo_animacion >= self.intervalo_animacion:
                    self.indice_imagen = (self.indice_imagen + 1) % len(self.imagenes[self.direccion_actual])
                    self.image = self.imagenes[self.direccion_actual][self.indice_imagen]
                    self.tiempo_animacion = 0  # Reiniciar contador
            else:
                # Si está cerca, cambia a imagen "quieto"
                self.image = self.imagenes["quieto"]

    def dibujar(self, ventana, camara):
        ventana.blit(self.image, camara.aplicar(self))