# NPC_informacion.py - Versión con menú numerado
import pygame
import os
import textwrap
import constantes

class NPCInformacion(pygame.sprite.Sprite):
    def __init__(self, x, y, sistema_misiones=None):
        super().__init__()
        self.imagen = self.cargar_imagen("recursos/imagenes/caracteres/humano/venta.png")
        self.rect = self.imagen.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.sistema_misiones = sistema_misiones
        
        # Formato igual que NPC bienvenida
        self.fuente_dialogo = pygame.font.Font(None, 20)
        self.fuente_pie = pygame.font.Font(None, 16)
        self.fuente_menu = pygame.font.Font(None, 18)  # Fuente para el menú
        self.fuente_titulo = pygame.font.Font(None, 18)  # Fuente para títulos
        self.dialogo_rect = pygame.Rect(70, 260, 700, 280)
        
        # Variables de control
        self.mostrar_interaccion = False
        self.dialogo_actual = 0
        self.pagina_actual = 0
        self.dialogo_activo = False
        self.mostrar_menu = True
        self.tema_seleccionado = None
        self.dialogo_ya_mostrado = False
        
        # Diálogos introductorios
        self.dialogos = [
            """¡Hola! Soy el Doctor Ronroneo.\n\n¡Wow! Qué gente preocupa por el bienestar animal!""",
            """TIPOS DE MALTRATO ANIMAL:\n\n
            1. Abuso Físico\n
            2. Negligencia\n
            3. Abandono\n
            4. Explotación\n
            5. Maltrato Psicológico\n
            6. Envenenamiento\n\n
            Presiona el número correspondiente para más información."""
        ]
        
        self.paginas_intro = [self._obtener_paginas_dialogo(d) for d in self.dialogos]
        
        # Datos de maltrato animal
        self.datos_maltrato = {
            1: """ABUSO FÍSICO\n\nEl abuso físico incluye golpes, heridas, fracturas, mutilaciones, quemaduras, cortes, o cualquier daño corporal causado intencionalmente a un animal. También se considera abuso físico el uso de collares de castigo, privación de movimiento, o forzar a los animales a realizar actividades peligrosas o dolorosas.\n\n
            CÓMO COMBATIRLO:\n- 
            Denuncia cualquier caso de maltrato físico ante las\n
              autoridades o entidades de protección animal.""",
            2: """NEGLIGENCIA\n\nLa negligencia es la falta de atención básica: comida, agua, refugio o atención veterinaria. Un animal negligido puede sufrir desnutrición, enfermedades, parásitos, o vivir en condiciones insalubres. La negligencia puede ser intencional o por desconocimiento, pero siempre afecta el bienestar del animal.\n\n
            CÓMO COMBATIRLA:\n
            - Informa a las autoridades si ves animales desatendidos, desnutridos o enfermos.""",
            3: """ABANDONO\n\nEl abandono ocurre cuando un animal es dejado a su suerte, sin protección ni recursos, en la calle, en terrenos baldíos o incluso en refugios saturados. El abandono expone a los animales a peligros como accidentes, enfermedades, hambre y maltrato por parte de personas o de otros animales.\n\n
            CÓMO COMBATIRLO:\n
            - Fomenta la adopción responsable y no el abandono.""",
            4: """EXPLOTACIÓN\n\nLa explotación es el uso de animales para trabajo forzado, espectáculos, experimentos, o actividades que les causan sufrimiento. Incluye la utilización de animales en circos, peleas, carreras, laboratorios, o como instrumentos de mendicidad.\n\n
            CÓMO COMBATIRLA:\n
            - No apoyes espectáculos, eventos o actividades que utilicen\n
              animales para entretenimiento o lucro.""",
            5: """MALTRATO PSICOLÓGICO\n\nIncluye encierro prolongado, aislamiento, amenazas, gritos, privación de estímulos, o cualquier acción que cause miedo, estrés o ansiedad al animal. El maltrato psicológico puede afectar gravemente la salud mental y física de los animales.\n\n
            CÓMO COMBATIRLO:\n
            - Brinda compañía, cariño y estimulación a los animales bajo tu cuidado.""",
            6: """ENVENENAMIENTO\n\nEl envenenamiento puede ser intencional (por odio, venganza o control de plagas) o accidental (por dejar sustancias tóxicas al alcance). Puede causar sufrimiento, enfermedades graves y la muerte de los animales.\n\n
            CÓMO COMBATIRLO:\n
            - Mantén sustancias tóxicas (venenos, medicamentos, productos de limpieza)\n
              fuera del alcance de los animales."""
        }

    def cargar_imagen(self, ruta):
        try:
            print(f"Intentando cargar imagen desde: {ruta}")
            imagen_original = pygame.image.load(ruta).convert_alpha()
            # Escalar la imagen a un tamaño más grande (2 veces el tamaño original)
            imagen_escalada = pygame.transform.scale(imagen_original, 
                                                  (int(imagen_original.get_width() * 2), 
                                                   int(imagen_original.get_height() * 2)))
            return imagen_escalada
        except pygame.error as e:
            print(f"Error al cargar la imagen {ruta}: {e}")
            # Crear una imagen de fallback
            imagen = pygame.Surface((50, 50))
            imagen.fill((255, 0, 0))  # Rojo para indicar error
            return imagen

    def _obtener_paginas_dialogo(self, texto):
        import textwrap
        paginas = []
        lineas_actuales = []
        
        # Calcular el número máximo de caracteres que caben en el ancho del recuadro
        caracteres_por_linea = 55  # Valor fijo seguro para evitar desbordes
        
        # Calcular el número máximo de líneas por página
        espacio_vertical = self.dialogo_rect.height - 60  # 20px arriba + 40px abajo para el pie
        altura_linea = 16  # Altura de la fuente pequeña
        max_lineas_por_pagina = int(espacio_vertical / altura_linea)
        
        # Dividir el texto en secciones (título, información, cómo combatirlo)
        secciones = texto.split('\n\n')
        
        for seccion in secciones:
            if seccion.strip():
                # Si es un título, mantenerlo en una línea
                if seccion.startswith('ABUSO FÍSICO') or seccion.startswith('NEGLIGENCIA') or \
                   seccion.startswith('ABANDONO') or seccion.startswith('EXPLOTACIÓN') or \
                   seccion.startswith('MALTRATO PSICOLÓGICO') or seccion.startswith('ENVENENAMIENTO'):
                    lineas_actuales.append(seccion)
                    lineas_actuales.append("")  # Línea en blanco después del título
                elif seccion.startswith('CÓMO COMBATIR'):
                    lineas_actuales.append("")  # Línea en blanco antes de la sección
                    lineas_actuales.append(seccion)
                    lineas_actuales.append("")  # Línea en blanco después de la sección
                else:
                    # Para el resto del texto, dividirlo en líneas
                    lineas = textwrap.wrap(seccion, width=caracteres_por_linea)
                    lineas_actuales.extend(lineas)
                
                # Si hemos alcanzado el máximo de líneas, crear una nueva página
                if len(lineas_actuales) >= max_lineas_por_pagina:
                    paginas.append(lineas_actuales[:max_lineas_por_pagina])
                    lineas_actuales = lineas_actuales[max_lineas_por_pagina:]
        
        # Agregar las líneas restantes como última página
        if lineas_actuales:
            paginas.append(lineas_actuales)
        
        return paginas

    def mostrar_dialogo(self):
        self.dialogo_activo = True
        self.dialogo_actual = 0
        self.pagina_actual = 0
        self.mostrar_menu = True
        self.tema_seleccionado = None
        self.dialogo_ya_mostrado = True

    def avanzar_dialogo(self):
        if not self.dialogo_activo:
            return
        
        # Si está en el menú de tipos de maltrato y presiona P, cerrar el diálogo
        if self.mostrar_menu and self.tema_seleccionado is None and self.dialogo_actual == 1:
            self.dialogo_activo = False
            self.dialogo_actual = 0
            self.pagina_actual = 0
            self.mostrar_menu = True
            self.tema_seleccionado = None
            return
        
        # Si está en un tema específico y presiona P, avanzar página o volver al menú
        if self.tema_seleccionado is not None:
            if hasattr(self, 'paginas_tema') and self.pagina_actual < len(self.paginas_tema) - 1:
                self.pagina_actual += 1
            # Si ya está en la última página, no hace nada con P (solo con 8 se vuelve al menú)
            return
        
        # Avanzar en los diálogos introductorios
        if self.mostrar_menu and self.tema_seleccionado is None:
            if self.dialogo_actual < len(self.dialogos) - 1:
                self.dialogo_actual += 1
                self.pagina_actual = 0
            else:
                # Si estamos en el último diálogo, mantener el menú visible
                self.dialogo_actual = 1
                self.pagina_actual = 0

    def seleccionar_tema(self, numero):
        """Selecciona un tema específico para mostrar su información"""
        if numero < 1 or numero > 6:
            return
        print(f"Seleccionando tema {numero}")  # Debug
        self.tema_seleccionado = numero
        self.mostrar_menu = False
        self.pagina_actual = 0
        self.dialogo_activo = True  # Asegurar que el diálogo permanezca activo
        # Separar definición y cómo combatirlo
        info = self.datos_maltrato[numero]
        partes = info.split('CÓMO COMBATIR')
        self.paginas_tema = []
        if len(partes) == 2:
            definicion = partes[0].strip() + '\n\nCÓMO COMBATIR...'
            combatir = 'CÓMO COMBATIR' + partes[1]
            # Paginar cada parte
            self.paginas_tema.extend(self._obtener_paginas_dialogo(definicion))
            self.paginas_tema.extend(self._obtener_paginas_dialogo(combatir))
        else:
            self.paginas_tema = self._obtener_paginas_dialogo(info)

    def dibujar_dialogo(self, ventana):
        if not self.dialogo_activo:
            return
        s = pygame.Surface((self.dialogo_rect.width, self.dialogo_rect.height))
        s.set_alpha(200)
        s.fill((0, 0, 0))
        ventana.blit(s, (self.dialogo_rect.x, self.dialogo_rect.y))
        pygame.draw.rect(ventana, (255, 255, 255), self.dialogo_rect, 3)

        if self.dialogo_actual == 1 and self.mostrar_menu:
            tipos = [
                "TIPOS DE MALTRATO:",
                "1. Abuso Físico    2. Negligencia    3. Abandono",
                "4. Explotación     5. Maltrato Psicológico     6. Envenenamiento",
                "",
                "Selecciona el número del tipo de maltrato para tener más información",
            ]
            for i, linea in enumerate(tipos):
                superficie = self.fuente_dialogo.render(linea, True, (255, 255, 255))
                ventana.blit(superficie, (self.dialogo_rect.x + 20, self.dialogo_rect.y + 20 + i * 30))
            pie = self.fuente_pie.render("P para cerrar", True, (200, 200, 200))
            ventana.blit(pie, (self.dialogo_rect.x + 20, self.dialogo_rect.y + self.dialogo_rect.height - 35))
        elif self.tema_seleccionado is not None:
            # Mostrar la página actual del tema (definición o cómo combatirlo, paginado)
            if hasattr(self, 'paginas_tema') and self.pagina_actual < len(self.paginas_tema):
                lineas_envueltas = self.paginas_tema[self.pagina_actual]
            else:
                lineas_envueltas = [""]
            for i, linea in enumerate(lineas_envueltas):
                superficie = self.fuente_dialogo.render(linea, True, (255, 255, 255))
                ventana.blit(superficie, (self.dialogo_rect.x + 20, self.dialogo_rect.y + 20 + i * 22))
            pie_y = self.dialogo_rect.y + 20 + len(lineas_envueltas) * 22 + 8
            if pie_y > self.dialogo_rect.y + self.dialogo_rect.height - 30:
                pie_y = self.dialogo_rect.y + self.dialogo_rect.height - 30
            # Pie de página
            if self.pagina_actual < len(self.paginas_tema) - 1:
                pie_texto = "P para continuar | 8 para volver al menú"
            else:
                pie_texto = "8 para volver al menú"
            pie = self.fuente_pie.render(pie_texto, True, (200, 200, 200))
            ventana.blit(pie, (self.dialogo_rect.x + 20, pie_y))
        else:
            if self.dialogo_actual < len(self.dialogos):
                texto = self.dialogos[self.dialogo_actual]
                lineas = texto.split('\n')
                for i, linea in enumerate(lineas):
                    superficie = self.fuente_dialogo.render(linea, True, (255, 255, 255))
                    ventana.blit(superficie, (self.dialogo_rect.x + 20, self.dialogo_rect.y + 20 + i * 30))
            pie = self.fuente_pie.render("Presiona P para continuar...", True, (200, 200, 200))
            ventana.blit(pie, (self.dialogo_rect.x + 20, self.dialogo_rect.y + self.dialogo_rect.height - 35))

    def dibujar(self, ventana, camara=None):
        """Dibuja el NPC en la ventana ajustado a la cámara."""
        print(f"Dibujando NPC en posición: {self.rect.x}, {self.rect.y}")
        # Dibujar NPC
        if camara:
            pos = camara.aplicar(self)
            print(f"Posición ajustada por cámara: {pos}")
            ventana.blit(self.imagen, pos)
        else:
            ventana.blit(self.imagen, self.rect)
        
        # Dibujar diálogo si está activo
        if self.dialogo_activo:
            self.dibujar_dialogo(ventana)
        
        # Dibujar indicador de interacción si corresponde
        elif self.mostrar_interaccion:
            texto = "Presiona E para interactuar"
            texto_surface = self.fuente_dialogo.render(texto, True, (255, 255, 255))
            ventana.blit(texto_surface, (self.rect.x, self.rect.y - 30))

    def actualizar(self, personaje, teclas):
        """Actualiza el estado del NPC"""
        # Verificar si el personaje está cerca
        distancia = abs(personaje.rect.centerx - self.rect.centerx) + abs(personaje.rect.centery - self.rect.centery)
        print(f"Distancia al personaje: {distancia}")
        self.mostrar_interaccion = distancia < 100  # Mostrar indicador si está a menos de 100 píxeles
        print(f"Mostrar interacción: {self.mostrar_interaccion}")
        
        # Manejar selección de temas con teclas numéricas
        if self.dialogo_activo and self.mostrar_menu and self.tema_seleccionado is None:
            if teclas[pygame.K_1]:
                self.seleccionar_tema(1)
            elif teclas[pygame.K_2]:
                self.seleccionar_tema(2)
            elif teclas[pygame.K_3]:
                self.seleccionar_tema(3)
            elif teclas[pygame.K_4]:
                self.seleccionar_tema(4)
            elif teclas[pygame.K_5]:
                self.seleccionar_tema(5)
            elif teclas[pygame.K_6]:
                self.seleccionar_tema(6)
        # Permitir volver al menú con la tecla 8
        if self.dialogo_activo and self.tema_seleccionado is not None and teclas[pygame.K_8]:
            self.tema_seleccionado = None
            self.pagina_actual = 0
            self.mostrar_menu = True
            self.dialogo_actual = 1  # Volver al menú

def crear_npc_informacion(x, y, sistema_misiones=None):
    """Función helper para crear una instancia del NPC de información."""
    return NPCInformacion(x, y, sistema_misiones)