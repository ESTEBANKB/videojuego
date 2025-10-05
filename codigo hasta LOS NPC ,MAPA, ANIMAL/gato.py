# gato.py - Personaje principal del juego
import os
import pygame

class PersonajeGato(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        
        # Cargar imágenes del gato
        self.imagenes = self._cargar_imagenes_gato()
        
        # Estado inicial
        self.direccion = "quieto"
        self.image = self.imagenes["quieto"]
        self.rect = self.image.get_rect(topleft=(x, y))
        
        # Variables de animación
        self.frame_actual = 0
        self.contador_animacion = 0
        self.velocidad_animacion = 8
        
        # Velocidad de movimiento
        self.velocidad = 5
        
        # Estado de movimiento
        self.moviendose = False
        
        # Estado de visibilidad
        self.visible = True
        
        self.energia = 100
        self.energia_max = 100
    
    def _cargar_imagen_con_check(self, ruta):
        """Carga una imagen y verifica que exista; si no, muestra un error rojo"""
        if not os.path.exists(ruta):
            print(f"Error: No se encontró la imagen en la ruta {ruta}")
            superficie_error = pygame.Surface((50, 70))
            superficie_error.fill((255, 0, 0))  # Relleno rojo como aviso de error
            return superficie_error
        
        imagen_original = pygame.image.load(ruta).convert_alpha()
        return pygame.transform.scale(imagen_original, (50, 70))
    
    def _cargar_imagenes_gato(self):
        """Carga las animaciones del personaje gato (3 imágenes por dirección + quieto)"""
        carpeta_gato = "recursos/imagenes/caracteres/gato/"
        imagenes = {
            "abajo": [],
            "arriba": [],
            "derecha": [],
            "izquierda": [],
            "quieto": None
        }

        # Cargar imágenes de movimiento (3 frames por dirección)
        for i in range(1, 4):
            imagenes["abajo"].append(self._cargar_imagen_con_check(carpeta_gato + f"gabajo_{i}.png"))
            imagenes["arriba"].append(self._cargar_imagen_con_check(carpeta_gato + f"garriba_{i}.png"))
            imagenes["derecha"].append(self._cargar_imagen_con_check(carpeta_gato + f"gderecha_{i}.png"))
            imagenes["izquierda"].append(self._cargar_imagen_con_check(carpeta_gato + f"gizquierda_{i}.png"))

        # Cargar imagen quieto
        imagenes["quieto"] = self._cargar_imagen_con_check(carpeta_gato + "gquieto.png")
        return imagenes
    
    def actualizar(self, teclas_presionadas):
        """Actualiza el estado del personaje basado en las teclas presionadas"""
        # Guardar posición anterior
        pos_anterior = self.rect.copy()
        
        # Resetear estado de movimiento
        self.moviendose = False
        
        # Procesar movimiento
        if teclas_presionadas[pygame.K_LEFT] or teclas_presionadas[pygame.K_a]:
            self.rect.x -= self.velocidad
            self.direccion = "izquierda"
            self.moviendose = True
        elif teclas_presionadas[pygame.K_RIGHT] or teclas_presionadas[pygame.K_d]:
            self.rect.x += self.velocidad
            self.direccion = "derecha"
            self.moviendose = True
        elif teclas_presionadas[pygame.K_UP] or teclas_presionadas[pygame.K_w]:
            self.rect.y -= self.velocidad
            self.direccion = "arriba"
            self.moviendose = True
        elif teclas_presionadas[pygame.K_DOWN] or teclas_presionadas[pygame.K_s]:
            self.rect.y += self.velocidad
            self.direccion = "abajo"
            self.moviendose = True
        
        # Actualizar animación
        self._actualizar_animacion()
        
        return pos_anterior
    
    def _actualizar_animacion(self):
        """Actualiza la animación del personaje"""
        if self.moviendose and self.direccion != "quieto":
            # Incrementar contador de animación
            self.contador_animacion += 1
            
            if self.contador_animacion >= self.velocidad_animacion:
                # Cambiar frame
                self.frame_actual = (self.frame_actual + 1) % len(self.imagenes[self.direccion])
                self.image = self.imagenes[self.direccion][self.frame_actual]
                self.contador_animacion = 0
        else:
            # Si no se mueve, mostrar imagen quieto
            self.image = self.imagenes["quieto"]
            self.frame_actual = 0
            self.contador_animacion = 0
    
    def establecer_posicion(self, x, y):
        """Establece la posición del personaje"""
        self.rect.x = x
        self.rect.y = y
    
    def obtener_posicion(self):
        """Obtiene la posición actual del personaje"""
        return self.rect.x, self.rect.y
    
    def dibujar_barra_energia(self, ventana, camara=None):
        print(f"[DEBUG] Dibujando barra de energía: energia={self.energia}, energia_max={self.energia_max}")
        # Dibuja un rectángulo gigante en el centro de la pantalla para depuración
        pygame.draw.rect(ventana, (255, 0, 255), (100, 100, 200, 50))
        barra_ancho = 50
        barra_alto = 10
        x = self.rect.x
        y = self.rect.y - 20
        if camara:
            pos = camara.aplicar(self.rect)
            x = pos.x
            y = pos.y - 20
        pygame.draw.rect(ventana, (255, 0, 0), (x, y, barra_ancho, barra_alto))
        energia_actual = int(barra_ancho * (self.energia / self.energia_max))
        pygame.draw.rect(ventana, (0, 255, 0), (x, y, energia_actual, barra_alto))
        pygame.draw.rect(ventana, (0, 0, 0), (x, y, barra_ancho, barra_alto), 2)
    
    def dibujar(self, ventana, camara=None):
        """Dibuja el personaje en la ventana"""
        if not self.visible:
            return
            
        if camara:
            ventana.blit(self.image, camara.aplicar(self.rect))
        else:
            ventana.blit(self.image, self.rect)
        self.dibujar_barra_energia(ventana, camara)
    
    def colisiona_con(self, otro_rect):
        """Verifica si el personaje colisiona con otro rectángulo"""
        return self.rect.colliderect(otro_rect)
    
    def restaurar_posicion(self, pos_anterior):
        """Restaura la posición anterior del personaje"""
        self.rect = pos_anterior


# Funciones auxiliares para compatibilidad
def cargar_imagen_con_check(ruta):
    """Carga una imagen y verifica que exista; si no, muestra un error rojo"""
    if not os.path.exists(ruta):
        print(f"Error: no se encontró la imagen en la ruta {ruta}")
        superficie_error = pygame.Surface((50, 70))
        superficie_error.fill((255, 0, 0))  # Relleno rojo como aviso de error
        return superficie_error
    return pygame.image.load(ruta).convert_alpha()  # Carga con transparencia

def cargar_imagenes_gato():
    """Función legacy para compatibilidad con código existente"""
    carpeta_gato = "recursos/imagenes/caracteres/gato/"
    imagenes = {
        "abajo": [],
        "arriba": [],
        "derecha": [],
        "izquierda": [],
        "quieto": None
    }

    for i in range(1, 4):
        imagenes["abajo"].append(cargar_imagen_con_check(carpeta_gato + f"gabajo_{i}.png"))
        imagenes["arriba"].append(cargar_imagen_con_check(carpeta_gato + f"garriba_{i}.png"))
        imagenes["derecha"].append(cargar_imagen_con_check(carpeta_gato + f"gderecha_{i}.png"))
        imagenes["izquierda"].append(cargar_imagen_con_check(carpeta_gato + f"gizquierda_{i}.png"))

    imagenes["quieto"] = cargar_imagen_con_check(carpeta_gato + "gquieto.png")
    return imagenes

def crear_personaje_gato(x=100, y=100):
    """Función helper para crear una instancia del personaje gato"""
    return PersonajeGato(x, y)