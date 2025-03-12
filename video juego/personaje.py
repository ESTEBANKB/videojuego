#personaje.py
import pygame
import constantes
import os

class Personaje:
    def __init__(self, x, y):
        """Inicializa al personaje con su imagen y posición."""
        self.imagen = pygame.image.load(os.path.join("imagenes\personaje.png")) # Carga la imagen original
        self.imagen = pygame.transform.scale(self.imagen, (constantes.ANCHO_PERSONAJE, constantes.ALTO_PERSONAJE)) # Escala la imagen 
        # Redimensiona según constantes
       # Posición inicial en el mapa
        # Posición inicial en la cuadrícula
        self.mapa_x, self.mapa_y = x, y  
        self.rect = self.imagen.get_rect()
        self.rect.topleft = (self.mapa_x * constantes.TAMANO_CELDA, self.mapa_y * constantes.TAMANO_CELDA)
        

        

    def mover(self, teclas,mundo):
        """Mueve al personaje según las teclas presionadas."""
        self.velocidad = constantes.VELOCIDAD_PERSONAJE # usamos la constante para la velocidad
        nueva_x, nueva_y = self.rect.x, self.rect.y
        
        if teclas[pygame.K_a] or teclas[pygame.K_LEFT]:
            self.rect.x -= constantes.VELOCIDAD_PERSONAJE
        if teclas[pygame.K_d] or teclas[pygame.K_RIGHT]:
            self.rect.x += constantes.VELOCIDAD_PERSONAJE
        if teclas[pygame.K_w] or teclas[pygame.K_UP]:
            self.rect.y -= constantes.VELOCIDAD_PERSONAJE
        if teclas[pygame.K_s] or teclas[pygame.K_DOWN]:
            self.rect.y += constantes.VELOCIDAD_PERSONAJE
            
            

       # Verificar si la nueva área está permitida
        if mundo.es_transitable(nueva_x, nueva_y):
            self.mapa_x, self.mapa_y = nueva_x, nueva_y
            self.rect.topleft = (self.mapa_x * constantes.TAMANO_CELDA, self.mapa_y * constantes.TAMANO_CELDA)
            
    def dibujar(self, ventana):
        """Dibuja al personaje en la pantalla."""
        ventana.blit(self.imagen, self.rect)

