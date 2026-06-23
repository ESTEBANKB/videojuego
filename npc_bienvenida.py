# npc_bienvenida.py - Convertido a NPC de Misión Dos
import pygame
import os
import textwrap

class NPCHumano(pygame.sprite.Sprite):
    def __init__(self, x=1900, y=600, sistema_misiones=None):
        super().__init__()
        
        # Cargar imagen del NPC (nueva ruta)
        self.ruta_imagen = "recursos/imagenes/caracteres/humano/personaje.png"
        self.image = self._cargar_imagen_con_check(self.ruta_imagen)
        self.rect = self.image.get_rect(topleft=(x, y))
        
        self.sistema_misiones = sistema_misiones
        
        # Variables para controlar el diálogo
        self.dialogo_activo = False
        self.dialogo_ya_mostrado = False
        self.dialogo_actual = 0 # Índice del "tema" o "fase" del diálogo
        self.mision_activada = False  # Nueva variable para controlar si ya se activó la misión
        
        # Fuentes para el diálogo
        self.fuente_dialogo = pygame.font.Font(None, 28)
        self.fuente_pie = pygame.font.Font(None, 22)
        
        # Rectángulo del cuadro de diálogo
        self.dialogo_rect = pygame.Rect(50, 400, 700, 150)
        
        # Diálogos específicos del NPC para la Misión Dos
        self.dialogos_por_tema = [ 
            """¡Hola aventurero! Soy Samuel patrullo este bosque. 
            He estado esperando a alguien con tu determinación para una misión muy importante.""",
            
            """hay un gato abandonado  está en grave peligro y necesita nuestra ayuda 
            urgente. ¿Estás dispuesto a aceptar esta misión?""",
            
            """buscalo debe estar muy mal....?"""

        ]
        
        # Diálogo inicial cuando el refugio no está comprado
        self.dialogo_inicial = [
            """Hola, soy Azael y veo que estás interesado en el refugio.""",
            """Debes comprar primero el refugio para poderte dar tu 2da misión.""",
            """Busca a Rodrigo en el mapa y completa la misión de las monedas.\n
            ¡Buena suerte!"""
        ]
        
        # Almacenar las páginas pre-calculadas para cada tema de diálogo
        self.paginas_por_tema = []
        for dialogo_completo in self.dialogos_por_tema:
            self.paginas_por_tema.append(self._obtener_paginas_dialogo(dialogo_completo))
            
        # Almacenar las páginas del diálogo inicial
        self.paginas_inicial = []
        for dialogo_completo in self.dialogo_inicial:
            self.paginas_inicial.append(self._obtener_paginas_dialogo(dialogo_completo))

        self.pagina_actual = 0 # Índice de la página actual dentro del diálogo activo
        self.mostrar_dialogo_inicial = True  # Controla si mostrar el diálogo inicial
        self.refugio_comprado = False  # Nueva variable para controlar si el refugio está comprado

    def _cargar_imagen_con_check(self, ruta):
        """Carga una imagen y verifica que exista; si no, muestra un error rojo"""
        if not os.path.exists(ruta):
            print(f"Error: no se encontró la imagen en la ruta {ruta}")
            superficie_error = pygame.Surface((50, 70))
            superficie_error.fill((255, 0, 0))  # Relleno rojo como aviso de error
            return superficie_error
        return pygame.image.load(ruta).convert_alpha()  # Carga con transparencia

    def _obtener_paginas_dialogo(self, texto_completo):
        """
        Divide un texto completo en páginas que caben en el cuadro de diálogo.
        Cada página termina cuando no caben más líneas.
        """
        max_ancho_linea = 70  # Caracteres por línea (ajusta según tu fuente y tamaño de recuadro)
        altura_linea = self.fuente_dialogo.get_height() + 2 # Altura de cada línea de texto + un pequeño margen
        
        # Calcular el número máximo de líneas que caben en el cuadro de diálogo
        margen_vertical_dialogo = 40 # Margen superior e inferior dentro del diálogo (20 + 20)
        altura_disponible = self.dialogo_rect.height - margen_vertical_dialogo
        max_lineas_por_pagina = int(altura_disponible / altura_linea)
        
        paginas = []
        lineas_actuales_pagina = []
        
        # Primero, envolver todo el texto para tener las líneas que realmente se renderizarán
        todas_las_lineas_envueltas = []
        # Dividir por '\n' para manejar párrafos explícitos
        parrafos = texto_completo.replace('\\n', '\n').split('\n')
        
        for parrafo in parrafos:
            if parrafo.strip(): # Si no es una línea vacía
                todas_las_lineas_envueltas.extend(textwrap.wrap(parrafo, width=max_ancho_linea))
            else: # Mantener las líneas vacías para representar saltos de párrafo
                todas_las_lineas_envueltas.append("") # Añadir una línea vacía para el salto de párrafo

        for linea in todas_las_lineas_envueltas:
            # Si añadir la línea actual excede el límite de líneas por página,
            # cerramos la página actual y empezamos una nueva.
            if len(lineas_actuales_pagina) >= max_lineas_por_pagina:
                paginas.append(lineas_actuales_pagina)
                lineas_actuales_pagina = [linea] # Empezar una nueva página con la línea actual
            else:
                lineas_actuales_pagina.append(linea)
        
        # Añadir la última página si hay líneas restantes
        if lineas_actuales_pagina:
            paginas.append(lineas_actuales_pagina)
            
        return paginas

    def actualizar(self, personaje, teclas):
        """Actualiza el estado del NPC (p.ej., si el diálogo debe estar activo)."""
        # Lógica para activar el diálogo si el personaje está cerca
        distancia_x = abs(personaje.rect.centerx - self.rect.centerx)
        distancia_y = abs(personaje.rect.centery - self.rect.centery)
        
        # Definir una distancia de interacción razonable
        distancia_interaccion = 80 # Ajusta según lo consideres necesario

        # El diálogo puede activarse múltiples veces (a diferencia del NPC de bienvenida)
        if distancia_x < distancia_interaccion and distancia_y < distancia_interaccion:
            # No activar automáticamente, esperar a que el jugador presione E
            pass
        elif (distancia_x >= distancia_interaccion or distancia_y >= distancia_interaccion) and self.dialogo_activo:
            self.dialogo_activo = False
            # Reiniciar diálogo si el jugador se aleja
            self.dialogo_actual = 0
            self.pagina_actual = 0

    def actualizar_estado_refugio(self, refugio_comprado):
        """Actualiza el estado del refugio"""
        self.refugio_comprado = refugio_comprado
        if refugio_comprado:
            self.mostrar_dialogo_inicial = False  # Cambiar al diálogo de la misión cuando se compre el refugio

    def mostrar_dialogo(self):
        """Activa el diálogo cuando el jugador presiona E"""
        self.dialogo_activo = True
        self.dialogo_actual = 0
        self.pagina_actual = 0
        # Si el refugio está comprado, mostrar el diálogo de la misión
        if self.refugio_comprado:
            self.mostrar_dialogo_inicial = False

    def avanzar_dialogo(self):
        """Avanza el diálogo cuando se presiona P"""
        if not self.dialogo_activo:
            return
            
        # Comprobar si hay más páginas en el diálogo actual
        if self.mostrar_dialogo_inicial:
            if self.pagina_actual < len(self.paginas_inicial[self.dialogo_actual]) - 1:
                self.pagina_actual += 1 # Avanzar a la siguiente página
            else:
                # Si no hay más páginas, intentar avanzar al siguiente tema de diálogo
                if self.dialogo_actual < len(self.paginas_inicial) - 1:
                    self.dialogo_actual += 1 # Avanzar al siguiente tema
                    self.pagina_actual = 0  # Reiniciar a la primera página del nuevo tema
                else:
                    # Si no hay más páginas ni más temas, cerrar el diálogo
                    self.dialogo_activo = False
                    self.dialogo_actual = 0 # Reiniciar para la próxima vez
                    self.pagina_actual = 0 # Reiniciar página también
        else:
            if self.pagina_actual < len(self.paginas_por_tema[self.dialogo_actual]) - 1:
                self.pagina_actual += 1 # Avanzar a la siguiente página
            else:
                # Si no hay más páginas, intentar avanzar al siguiente tema de diálogo
                if self.dialogo_actual < len(self.paginas_por_tema) - 1:
                    self.dialogo_actual += 1 # Avanzar al siguiente tema
                    self.pagina_actual = 0  # Reiniciar a la primera página del nuevo tema
                else:
                    # Si no hay más páginas ni más temas, cerrar el diálogo y activar misión
                    self.dialogo_activo = False
                    self.dialogo_actual = 0 # Reiniciar para la próxima vez
                    self.pagina_actual = 0 # Reiniciar página también
                    
                    # Activar la Misión Dos si no se ha activado antes y el refugio está comprado
                    if self.sistema_misiones and not self.mision_activada and self.refugio_comprado:
                        try:
                            self.sistema_misiones.activar_mision(2)  # Activar misión 2
                            self.mision_activada = True
                            print("¡Misión 2 activada: Salvar las tortugas marinas!")
                            # Hacer aparecer al gato en la posición inicial
                            if hasattr(self, 'gestor_npcs') and self.gestor_npcs and hasattr(self.gestor_npcs, 'gato') and self.gestor_npcs.gato:
                                self.gestor_npcs.gato.rect.x = 2430
                                self.gestor_npcs.gato.rect.y = 600
                                self.gestor_npcs.gato.visible = True
                        except Exception as e:
                            print(f"Error activando misión 2: {e}")

    def dibujar(self, ventana, camara=None):
        """Dibuja el NPC"""
        if camara:
            ventana.blit(self.image, camara.aplicar(self.rect))
        else:
            ventana.blit(self.image, self.rect)

    def dibujar_dialogo(self, ventana):
        """Dibuja el cuadro de diálogo y el texto si está activo."""
        if not self.dialogo_activo:
            return

        # Fondo del cuadro de diálogo (semi-transparente negro)
        s = pygame.Surface((self.dialogo_rect.width, self.dialogo_rect.height))
        s.set_alpha(200)
        s.fill((0, 0, 0))
        ventana.blit(s, (self.dialogo_rect.x, self.dialogo_rect.y))

        # Dibujar borde blanco
        pygame.draw.rect(ventana, (255, 255, 255), self.dialogo_rect, 3)
        
        # Obtener las líneas de la página actual
        try:
            if self.mostrar_dialogo_inicial:
                lineas_a_mostrar = self.paginas_inicial[self.dialogo_actual][self.pagina_actual]
            else:
                lineas_a_mostrar = self.paginas_por_tema[self.dialogo_actual][self.pagina_actual]
        except IndexError:
            print(f"Error: Índice de diálogo/página fuera de rango para {self.__class__.__name__}. "
                  f"Dialogo actual: {self.dialogo_actual}, Página actual: {self.pagina_actual}")
            lineas_a_mostrar = ["Error en diálogo", "Presiona P para cerrar"]

        y_offset = self.dialogo_rect.y + 20
        for linea in lineas_a_mostrar:
            img_texto = self.fuente_dialogo.render(linea, True, (255, 255, 255))
            ventana.blit(img_texto, (self.dialogo_rect.x + 20, y_offset))
            y_offset += self.fuente_dialogo.get_height() + 2

        # Mostrar instrucciones en el pie
        if self.mostrar_dialogo_inicial:
            hay_mas_paginas = self.pagina_actual < len(self.paginas_inicial[self.dialogo_actual]) - 1
            hay_mas_dialogos = self.dialogo_actual < len(self.paginas_inicial) - 1
        else:
            hay_mas_paginas = self.pagina_actual < len(self.paginas_por_tema[self.dialogo_actual]) - 1
            hay_mas_dialogos = self.dialogo_actual < len(self.paginas_por_tema) - 1

        if hay_mas_paginas:
            texto_pie = "Presiona P para continuar..."
        elif hay_mas_dialogos:
            texto_pie = "Presiona P para continuar..."
        else:
            if not self.mision_activada and self.refugio_comprado:
                texto_pie = "Presiona P para aceptar la misión"
            else:
                texto_pie = "Presiona P para cerrar"
        
        img_pie = self.fuente_pie.render(texto_pie, True, (200, 200, 200))
        ventana.blit(img_pie, (self.dialogo_rect.x + 20, self.dialogo_rect.bottom - 35))

# Función auxiliar para crear instancias del NPC de Misión Dos
def crear_npc_humano(sistema_misiones=None):
    return NPCHumano(1900, 600, sistema_misiones)