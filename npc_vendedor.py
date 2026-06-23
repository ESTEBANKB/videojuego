import pygame
import random

class NPCVendedor(pygame.sprite.Sprite):
   

    def __init__(self):
        super().__init__()
        # Cargar y escalar la imagen del vendedor
        imagen_original = pygame.image.load("recursos/imagenes/caracteres/humano/vendedor.png").convert_alpha()
        # Escalar la imagen a un tamaño más grande (1.5 veces el tamaño original)
        self.imagen = pygame.transform.scale(imagen_original, 
                                          (int(imagen_original.get_width() * 2), 
                                           int(imagen_original.get_height() * 2)))
        self.rect = self.imagen.get_rect()
        # Posición FIJA: esquina superior derecha
        self.rect.topleft = (2800, 220)
        self.mostrar_interaccion = False
        self.dialogo_activo = False
        self.mensaje = ""
        self.mostrar_mensaje = False
        self.tiempo_mensaje = 0
        self.DURACION_MENSAJE = 2000  # ms
        self.estado_dialogo = 0  # 0: saludo, 1: opciones, 2: resultado compra
        self.dialogo_rect = pygame.Rect(70, 300, 500, 220)  # Tamaño y posición del diálogo

    def posicion_aleatoria(self):
        self.rect.topleft = random.choice(self.POSICIONES_FIJAS)

    def iniciar_dialogo(self):
        self.dialogo_activo = True
        self.estado_dialogo = 0
        self.mensaje = ""

    def manejar_evento_dialogo(self, evento, personaje, comida_disponible):
        if not self.dialogo_activo:
            return comida_disponible, False
        if evento.type == pygame.KEYDOWN:
            if self.estado_dialogo == 0:
                # Saludo, pasar a opciones
                if evento.key == pygame.K_c or evento.key == pygame.K_e:
                    self.estado_dialogo = 1
            elif self.estado_dialogo == 1:
                if evento.key == pygame.K_c:
                    if personaje.score >= 3:   # cambio de 3 monedas por 1 comida 
                        personaje.score -= 3
                        comida_disponible += 1
                        self.mensaje = "¡Compraste 1 comida!"
                    else:
                        self.mensaje = "No tienes monedas suficientes."
                    self.estado_dialogo = 2
                    self.tiempo_mensaje = pygame.time.get_ticks()
                elif evento.key == pygame.K_p or evento.key == pygame.K_ESCAPE:
                    self.dialogo_activo = False
            elif self.estado_dialogo == 2:
                # Resultado de compra, volver a opciones o salir
                if evento.key == pygame.K_p or evento.key == pygame.K_ESCAPE:
                    self.dialogo_activo = False
                elif evento.key == pygame.K_c:
                    self.estado_dialogo = 1
        return comida_disponible, self.dialogo_activo

    def dibujar_dialogo(self, ventana):
        # Fondo centrado usando self.dialogo_rect
        fondo = pygame.Surface((self.dialogo_rect.width, self.dialogo_rect.height))
        fondo.set_alpha(220)
        fondo.fill((0, 0, 0))
        ventana.blit(fondo, self.dialogo_rect.topleft)
        pygame.draw.rect(ventana, (255, 255, 255), self.dialogo_rect, 3)
        fuente = pygame.font.Font(None, 25)
        fuente_titulo = pygame.font.Font(None, 36)
        x, y = self.dialogo_rect.topleft
        if self.estado_dialogo == 0:
            texto1 = "Hola, me llamo Andrés."
            texto2 = "Soy un vendedor de comida para tus mascotas."
            texto3 = "Presiona C para continuar."
            ventana.blit(fuente_titulo.render(texto1, True, (255,255,0)), (x+40, y+30))
            ventana.blit(fuente.render(texto2, True, (255,255,255)), (x+40, y+80))
            ventana.blit(fuente.render(texto3, True, (200,200,200)), (x+40, y+140))
        elif self.estado_dialogo == 1:
            texto1 = "¿Qué deseas hacer?"
            texto2 = "C - Comprar comida (1 unidad por 3 moneda)"
            texto3 = "P o ESC - Salir"
            ventana.blit(fuente_titulo.render(texto1, True, (255,255,0)), (x+40, y+30))
            ventana.blit(fuente.render(texto2, True, (255,255,255)), (x+40, y+80))
            ventana.blit(fuente.render(texto3, True, (200,200,200)), (x+40, y+140))
        elif self.estado_dialogo == 2:
            ventana.blit(fuente_titulo.render(self.mensaje, True, (0,255,0) if self.mensaje.startswith('¡') else (255,80,80)), (x+40, y+70))
            ventana.blit(fuente.render("C - Comprar otra | P o ESC - Salir", True, (200,200,200)), (x+40, y+140))

    def dibujar(self, ventana, camara=None):
        if camara:
            pos = camara.aplicar(self)
            ventana.blit(self.imagen, pos)
            x, y = pos.topleft
        else:
            ventana.blit(self.imagen, self.rect)
            x, y = self.rect.topleft

        # Indicador de interacción
        if self.mostrar_interaccion and not self.dialogo_activo:
            fuente = pygame.font.Font(None, 28)
            texto = "Presiona E para hablar"
            superficie = fuente.render(texto, True, (255, 255, 0))
            fondo = pygame.Surface((superficie.get_width() + 10, superficie.get_height() + 5))
            fondo.set_alpha(180)
            fondo.fill((0, 0, 0))
            ventana.blit(fondo, (x - 10, y - 40))
            ventana.blit(superficie, (x - 5, y - 38))

        # Diálogo centrado
        if self.dialogo_activo:
            self.dibujar_dialogo(ventana)

    def actualizar(self, personaje):
        # Mostrar indicador si el personaje está cerca
        distancia = abs(personaje.rect.centerx - self.rect.centerx) + abs(personaje.rect.centery - self.rect.centery)
        self.mostrar_interaccion = distancia < 150 