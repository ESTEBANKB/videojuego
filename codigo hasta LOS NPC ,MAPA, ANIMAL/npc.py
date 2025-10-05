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
        self.ha_colisionado = False
        self.velocidad = 4
        self.tiempo_animacion = 0
        self.intervalo_animacion = 5
        self.distancia_seguimiento = 300
        self.distancia_maxima = 500
        self.mostrar_indicador = False
        self.tecla_q_presionada = False
        self.tecla_r_presionada = False  # Nueva tecla para soltar
        self.visible = True
        self.energia = 100
        self.energia_max = 100
        self.fue_rescatado = False

    def actualizar(self, personaje, teclas=None):
        # Obtener teclas si no se pasaron
        if teclas is None:
            teclas = pygame.key.get_pressed()
        
        # Calcular distancia al personaje
        dx = personaje.rect.x - self.rect.x
        dy = personaje.rect.y - self.rect.y
        distancia = (dx**2 + dy**2) ** 0.5

        # Mostrar indicador cuando el jugador está cerca
        self.mostrar_indicador = distancia < 100

        # Verificar si se presionó Q - CORRECCIÓN AQUÍ
        if teclas[pygame.K_q]:  # Forma correcta de verificar teclas
            if not self.tecla_q_presionada and distancia < 100:
                print("Tecla Q presionada - Cambiando estado de seguimiento")
                self.siguiendo = not self.siguiendo
                self.tecla_q_presionada = True
                print(f"Estado de seguimiento: {self.siguiendo}")
        else:
            self.tecla_q_presionada = False

        # Verificar si se presionó R para soltar el gato
        if teclas[pygame.K_r]:
            if not self.tecla_r_presionada and self.siguiendo:
                print("Tecla R presionada - Soltando al gato")
                self.siguiendo = False
                self.tecla_r_presionada = True
                print("El gato ya no te sigue")
        else:
            self.tecla_r_presionada = False

        # Lógica de seguimiento
        if self.siguiendo:
            print(f"Siguiendo al jugador - Distancia: {distancia}")
            # Determinar dirección
            if abs(dx) > abs(dy):
                self.direccion_actual = "derecha" if dx > 0 else "izquierda"
            else:
                self.direccion_actual = "abajo" if dy > 0 else "arriba"

            # Mover hacia el personaje
            if distancia > 40:  # Solo moverse si está lejos
                # Normalizar el movimiento para que sea más suave
                if dx != 0:
                    self.rect.x += self.velocidad if dx > 0 else -self.velocidad
                if dy != 0:
                    self.rect.y += self.velocidad if dy > 0 else -self.velocidad

                # Actualizar animación
                self.tiempo_animacion += 1
                if self.tiempo_animacion >= self.intervalo_animacion:
                    self.indice_imagen = (self.indice_imagen + 1) % len(self.imagenes[self.direccion_actual])
                    self.image = self.imagenes[self.direccion_actual][self.indice_imagen]
                    self.tiempo_animacion = 0
            else:
                # Si está cerca, mostrar imagen quieta
                self.image = self.imagenes["quieto"]
                self.indice_imagen = 0
                self.tiempo_animacion = 0

            # Dejar de seguir si se aleja demasiado
            if distancia > self.distancia_maxima:
                print("Jugador demasiado lejos - Dejando de seguir")
                self.siguiendo = False

    def dibujar(self, ventana, camara):
        if not hasattr(self, 'visible') or not self.visible:
            return
        ventana.blit(self.image, camara.aplicar(self))
        
        # Mostrar indicadores según el estado
        if self.siguiendo:
            fuente = pygame.font.Font(None, 24)
            mensaje_soltar = "Presiona R para soltar"
            texto_soltar = fuente.render(mensaje_soltar, True, (255, 255, 0))
            fondo_soltar = pygame.Surface((texto_soltar.get_width() + 10, texto_soltar.get_height() + 5))
            fondo_soltar.set_alpha(180)
            fondo_soltar.fill((50, 50, 0))
            pos_texto_soltar = camara.aplicar(pygame.Rect(self.rect.x - 20, self.rect.y - 30, 0, 0))
            ventana.blit(fondo_soltar, (pos_texto_soltar.x - 5, pos_texto_soltar.y - 2))
            ventana.blit(texto_soltar, pos_texto_soltar)
            
        elif self.mostrar_indicador:
            fuente = pygame.font.Font(None, 24)
            mensaje = "Presiona Q para que te siga"
            texto = fuente.render(mensaje, True, (255, 255, 255))
            fondo = pygame.Surface((texto.get_width() + 10, texto.get_height() + 5))
            fondo.set_alpha(180)
            fondo.fill((0, 0, 0))
            pos_texto = camara.aplicar(pygame.Rect(self.rect.x - 20, self.rect.y - 30, 0, 0))
            ventana.blit(fondo, (pos_texto.x - 5, pos_texto.y - 2))
            ventana.blit(texto, pos_texto)