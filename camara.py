#camara

import pygame
import constantes
import refugio 
#self es una referencia al objeto actual que está siendo creado o usado dentro de una clase.
#Cada vez que creas un objeto a partir de una clase, ese objeto necesita recordar sus propias variables y funciones. self permite acceder a las variables y métodos que pertenecen a ese objeto específico.
class Camara:
    def __init__(self, ancho_mapa, alto_mapa): 
        """Inicializa la cámara con los límites del mapa."""
        self.camara_rect = pygame.Rect(0, 0, 800, 600)  # Tamaño de la ventana
        self.ancho_mapa = ancho_mapa 
        self.alto_mapa = alto_mapa
        
        

        
    def aplicar(self, objeto):
        """Aplica el desplazamiento de la cámara a un objeto."""
        
        if isinstance(objeto, pygame.Rect):  # Si ya es un rectángulo
            return objeto.move(-self.camara_rect.x, -self.camara_rect.y) # Aplicar el desplazamiento
        else:  # Si es un objeto con atributo `rect`
            return objeto.rect.move(-self.camara_rect.x, -self.camara_rect.y) # Aplicar el desplazamiento 
          
 
    def update(self, target):
        """Centrar la cámara en el personaje."""
        
        # Verificar la posición actual del personaje
        #print(f"Personaje X: {target.rect.centerx}, Personaje Y: {target.rect.centery}")
        
        
        nueva_x = target.rect.centerx - (800 // 2)
        nueva_y = target.rect.centery - (600 // 2)

         # Verificar si el personaje está en una posición válida para mover la cámara
        #print(f"Antes de limitar -> Cámara X: {nueva_x}, Cámara Y: {nueva_y}")
        
        # Limitar la cámara a los bordes del mapa
        self.camara_rect.x = max(0, min(nueva_x, self.ancho_mapa - 800))
        self.camara_rect.y = max(0, min(nueva_y, self.alto_mapa - 600))

       # Verificar la nueva posición de la cámara
       # print(f"Cámara X: {self.camara_rect.x}, Cámara Y: {self.camara_rect.y}")
      #  print(f"Ancho del mapa: {self.ancho_mapa}")
    
    
    
        