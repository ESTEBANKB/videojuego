# personaje
import pygame
import constantes


class Personaje(pygame.sprite.Sprite):
    def __init__(self, x, y, imagenes):
        super().__init__()
        """Inicializa el personaje con las imágenes cargadas y su posición."""
        self.imagenes = imagenes  # Diccionario con imágenes organizadas por dirección
        self.direccion_actual = "abajo"  # Dirección inicial
        self.indice_imagen = 0
        self.rect = pygame.Rect(x, y, constantes.ANCHO_PERSONAJE, constantes.ALTO_PERSONAJE)
        self.flip = False
        self.update_time = pygame.time.get_ticks()
        
        self.vel_x = 0
        self.vel_y = 0
        
        #  Agregar el puntaje inicial
        self.score = 0
        
    def mover(self, teclas,colisiones):
        """Mueve al personaje en la pantalla y cambia su dirección."""
        self.vel_x = 0
        self.vel_y = 0
        moviendo = False  # Variable para detectar si se está moviendo
        # movimineto horizontal
        if teclas[pygame.K_a] or teclas[pygame.K_LEFT]:  
            self.vel_x = -constantes.VELOCIDAD_PERSONAJE
            self.direccion_actual = "izquierda"
            moviendo = True
        if teclas[pygame.K_d] or teclas[pygame.K_RIGHT]:  
            self.vel_x = constantes.VELOCIDAD_PERSONAJE
            self.direccion_actual = "derecha"
            moviendo = True
        if teclas[pygame.K_w] or teclas[pygame.K_UP]:  
            self.vel_y = -constantes.VELOCIDAD_PERSONAJE
            self.direccion_actual = "arriba"
            moviendo = True
        if teclas[pygame.K_s] or teclas[pygame.K_DOWN]:  
            self.vel_y = constantes.VELOCIDAD_PERSONAJE
            self.direccion_actual = "abajo"
            moviendo = True



          # Mover en el eje X y verificar colisiones
        self.rect.x += self.vel_x
        if colisiones.verificar_colision(self, "horizontal"):
           self.rect.x -= self.vel_x  # Si hay colisión, revertir el movimiento
        # Mover en el eje Y y verificar colisiones
        self.rect.y += self.vel_y
        if colisiones.verificar_colision(self, "vertical"):
           self.rect.y -= self.vel_y  # Si hay colisión, revertir el movimiento
        # Solo actualizar la animación si el personaje se mueve
        if moviendo:           
           self.update()  # Actualizar la animación
        else:
           self.indice_imagen = 0  # Si no se mueve, mantener la primera imagen
           self.image = self.imagenes[self.direccion_actual][self.indice_imagen]

    def update(self):
        """Actualiza la animación del personaje."""
        cooldown_imagen = 100  # Tiempo en milisegundos para cambiar de imagen
        tiempo_actual = pygame.time.get_ticks()
        
        # Asegurar que la animación cambia en el tiempo correcto
        if tiempo_actual - self.update_time >= cooldown_imagen:
            self.indice_imagen = (self.indice_imagen + 1) % len(self.imagenes[self.direccion_actual])
            self.update_time = tiempo_actual
            
            
        # Asignar la imagen actual del personaje
        self.image = self.imagenes[self.direccion_actual][self.indice_imagen]
        
        
        # 🔍 Verificar valores en cada actualización
       # print("Dirección actual:", self.direccion_actual)
        #print("Índice imagen:", self.indice_imagen)
        #print("Diccionario imágenes:", self.imagenes.keys())

    def dibujar(self, ventana):
        """Dibuja al personaje en la pantalla."""
        imagen_actual = self.imagenes[self.direccion_actual][self.indice_imagen]
        ventana.blit(imagen_actual, self.rect)

