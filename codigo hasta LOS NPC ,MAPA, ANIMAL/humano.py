import pygame
import textwrap # Necesario para envolver texto

class NPCHumano(pygame.sprite.Sprite):
    def __init__(self, x, y, imagen, dialogos): # Añadir 'dialogos' al init
        super().__init__()
        # Imagen y rectángulo para el NPC
        self.image = imagen
        self.rect = self.image.get_rect(topleft=(x, y))
        
        # Variables para controlar el diálogo
        self.dialogo_activo = False         # ¿Se muestra diálogo?
        self.dialogo_ya_mostrado = False    # Para mostrar diálogo solo una vez si quieres
        self.dialogo_actual = 0             # Índice de la pestaña de diálogo actual
        self.linea_actual = 0               # Línea de texto dentro de la pestaña (no se usa directamente si se envuelve texto)
        self.respuesta_actual = 0           # Índice para seleccionar opciones, si las hay

        # Fuente para el texto del diálogo (puedes ajustar según tu fuente en inicio.py)
        self.fuente_dialogo = pygame.font.Font(None, 22)
        self.fuente_pie = pygame.font.Font(None, 22) # Para el texto "Pulsa P para continuar..."

        # Tamaño y posición del cuadro de diálogo
        self.dialogo_rect = pygame.Rect(50, 400, 700, 150)
        
        # Asignar los diálogos
        self.dialogos = dialogos # Ahora se pasan los diálogos al constructor

    def mostrar_dialogo(self):
        """Activa el diálogo para mostrarlo"""
        self.dialogo_activo = True
        self.dialogo_actual = 0  # Empezar con la primera pestaña
        # self.linea_actual = 0    # No es tan relevante con textwrap, pero lo puedes mantener

    def ocultar_dialogo(self):
        """Desactiva el diálogo para ocultarlo"""
        self.dialogo_activo = False
        self.dialogo_ya_mostrado = True # Marca que ya se mostró para no repetir si es un diálogo único

    def avanzar_dialogo(self):
        """Avanza al siguiente cuadro de diálogo o lo oculta si es el último."""
        if self.dialogo_actual < len(self.dialogos) - 1:
            self.dialogo_actual += 1
            # self.linea_actual = 0 # Reiniciar la línea al avanzar de cuadro, no es tan crítico con textwrap
        else:
            self.ocultar_dialogo()

    def cambiar_respuesta(self):
        """
        Cambiar opción seleccionada (si tuvieses opciones para seleccionar).
        Aquí como ejemplo simplemente alterna la respuesta (no usado en este diálogo).
        """
        self.respuesta_actual = (self.respuesta_actual + 1) % 2  # Ejemplo simple

    def dibujar(self, ventana, camara):
        """Dibuja el NPC en la ventana ajustado a la cámara"""
        ventana.blit(self.image, camara.aplicar(self.rect))

    def dibujar_dialogo(self, ventana):
        """Dibuja el cuadro de diálogo y el texto si está activo"""
        if not self.dialogo_activo:
            return

        # Fondo del cuadro de diálogo (semi-transparente negro)
        s = pygame.Surface((self.dialogo_rect.width, self.dialogo_rect.height))
        s.set_alpha(200)
        s.fill((0, 0, 0))
        ventana.blit(s, (self.dialogo_rect.x, self.dialogo_rect.y))

        # Dibujar borde blanco
        pygame.draw.rect(ventana, (255, 255, 255), self.dialogo_rect, 3)

        # Obtener el texto del diálogo actual para mostrar
        # Envolviendo el texto para que quepa en el cuadro
        texto_a_mostrar = self.dialogos[self.dialogo_actual]
        lineas_envueltas = textwrap.wrap(texto_a_mostrar, width=70) # Ajusta el 'width' según necesidad

        y_offset = self.dialogo_rect.y + 15
        for linea in lineas_envueltas:
            img_texto = self.fuente_dialogo.render(linea, True, (255, 255, 255))
            ventana.blit(img_texto, (self.dialogo_rect.x + 15, y_offset))
            y_offset += self.fuente_dialogo.get_height() + 2
            
        # Mostrar texto "Pulsa P para continuar..." abajo del cuadro, sólo si NO es el último cuadro
        if self.dialogo_actual < len(self.dialogos) - 1:
            texto_pie = "Pulsa P para continuar..."
            img_pie = self.fuente_pie.render(texto_pie, True, (255, 255, 255))
            ventana.blit(img_pie, (self.dialogo_rect.x + 20, self.dialogo_rect.y + self.dialogo_rect.height - 35))