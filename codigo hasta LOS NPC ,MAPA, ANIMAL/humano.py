#humano

import pygame

class NPCHumano(pygame.sprite.Sprite):
    def __init__(self, x, y, imagen_surface, texto_bienvenida):
        super().__init__()
        self.image = imagen_surface
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.texto_bienvenida = texto_bienvenida
        self.dialogo_activo = False
        self.dialogo_ya_mostrado = False

        self.respuestas = ["¿Dónde está el gato?", "¿Qué tengo que hacer?", "Adiós"]
        self.respuesta_seleccionada = 0
        self.respuesta_actual = ""
        self.mostrar_respuesta = False

        self.lineas_dialogo = [texto_bienvenida]
        self.fuente = pygame.font.Font(None, 24)  # Fuente de Pygame
        self.color_fondo = (0, 0, 0)
        self.color_borde = (255, 255, 255)

    def mostrar_dialogo(self):
        self.dialogo_activo = True
        self.mostrar_respuesta = False
        self.respuesta_actual = ""

    def ocultar_dialogo(self):
        self.dialogo_activo = False

    def cambiar_respuesta(self):
        if self.dialogo_activo:
            self.respuesta_seleccionada = (self.respuesta_seleccionada + 1) % len(self.respuestas)

    def actualizar_dialogo(self):
        if self.dialogo_activo:
            seleccion = self.respuestas[self.respuesta_seleccionada]
            if seleccion == "¿Dónde está el gato?":
                self.respuesta_actual = "Está al este del mapa, ¡búscalo!"
            elif seleccion == "¿Qué tengo que hacer?":
                self.respuesta_actual = "Ayuda al gato a encontrar a sus amigos."
            elif seleccion == "Adiós":
                self.respuesta_actual = "¡Buena suerte!"
            self.mostrar_respuesta = True

    def dibujar(self, ventana, camara):
        ventana.blit(self.image, camara.aplicar(self))

    def dibujar_dialogo(self, ventana):
        if not self.dialogo_activo:
            return

        ancho = 600
        alto = 140
        x = 100
        y = 400

        cuadro = pygame.Rect(x, y, ancho, alto)
        pygame.draw.rect(ventana, self.color_fondo, cuadro)
        pygame.draw.rect(ventana, self.color_borde, cuadro, 3)

        # Dibujar el texto del diálogo
        lineas = self.lineas_dialogo.copy()

        if self.mostrar_respuesta:
            lineas.append("")  # Espacio antes de respuesta
            lineas.append(self.respuesta_actual)
        else:
            lineas.append("")  # Espacio antes de opciones
            for i, r in enumerate(self.respuestas):
                marcador = ">> " if i == self.respuesta_seleccionada else "   "
                lineas.append(marcador + r)

        lineas.append("E para seleccionar / P para enviar")

        for i, linea in enumerate(lineas):
            texto = self.fuente.render(linea, True, (255, 255, 255))
            ventana.blit(texto, (x + 10, y + 10 + i * 20))
