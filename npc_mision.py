#NPC_mision
import pygame
import os
import constantes
from items import Item
from generar_items import generar_monedas

CANTIDAD_MONEDAS_MISION = 13  # Cambia este valor cuando quieras

class NPCMision(pygame.sprite.Sprite):
    def __init__(self, x, y, imagen, sistema_misiones=None):
        super().__init__()
        self.image = imagen
        self.rect = self.image.get_rect(topleft=(x, y))
        self.sistema_misiones = sistema_misiones
        self.dialogo_activo = False
        self.dialogo_ya_mostrado = False
        self.dialogo_actual = 0
        self.linea_actual = 0
        self.mision_completada = False
        self.grupo_monedas = None  # Nuevo atributo para almacenar el grupo de monedas
        self.coin_images = []  # Nuevo atributo para almacenar las imágenes de las monedas
        
        # Definir los diálogos del NPC de misión
        self.dialogos_originales = [
            [
                "Hola, mi nombre es Rodrigo.\n"
                "Mi compañero Rastafari te envió conmigo, ¿verdad?"
            ],
            [
                "¿Sabías que hay más tipos de maltrato animal?\n"
                "No solo abuso físico, también psicológico,\n"
                "abandono, negligencia y explotación."
            ],
            [
                "Tu misión será recolectar 10 monedas para comprar el refugio.\n"
                "Esto te permitirá interactuar con otros NPCs y comenzar\n"
                "a rescatar animales. ¿Estás preparado?"
            ]
        ]

        # Nuevos diálogos para diferentes estados
        self.dialogo_insuficiente = [
            "Aún no tienes las 10 monedas necesarias.\n"
            "Sigue buscando por el mapa, encontrarás más monedas."
        ]

        self.dialogo_comprar = [
            "¡Excelente! Ya tienes las 10 monedas necesarias.\n"
            "Ahora ve a comprar el refugio para poder comenzar\n"
            "a rescatar animales. ¡Presiona Z en la puerta!"
        ]

        self.dialogo_refugio_comprado = [
            "¡Ehh! Ya veo que completaste la misión.\n"
            "Pero sabías que el maltrato animal en Antioquia\n"
            "es un problema grave? Muchos animales sufren\n"
            "de abandono y maltrato diariamente.",
            "En Colombia, más de 100.000 animales son\n"
            "abandonados cada año, y Antioquia es una de las\n"
            "regiones con mayor índice de maltrato animal.\n"
            "¡Necesitamos tu ayuda para cambiar esto!"
        ]
        
        # Inicializar diálogos con los originales
        self.dialogos = self.dialogos_originales.copy()
        
        # Configuración del cuadro de diálogo
        self.dialogo_rect = pygame.Rect(50, 400, 700, 180)  # Reducido el ancho a 700
        self.fuente_dialogo = pygame.font.Font(None, 28)
        self.fuente_pie = pygame.font.Font(None, 22)

    def set_grupo_monedas(self, grupo):
        """Establece el grupo de monedas"""
        print("DEBUG: NPCMision.set_grupo_monedas - Estableciendo grupo de monedas")
        if grupo is not None:
            self.grupo_monedas = grupo
            print("DEBUG: Grupo de monedas establecido correctamente")
        else:
            print("ERROR: Se intentó establecer un grupo de monedas None")

    def set_coin_images(self, images):
        """Establece las imágenes de las monedas"""
        print(f"DEBUG: NPCMision.set_coin_images - Recibiendo {len(images)} imágenes")
        if images:
            self.coin_images = images
            print("DEBUG: Imágenes de monedas establecidas correctamente")
        else:
            print("ERROR: Se intentó establecer una lista vacía de imágenes de monedas")

    def set_personaje(self, personaje):
        self.personaje = personaje

    def mostrar_dialogo(self):
        """Muestra el diálogo inicial y genera las monedas solo la primera vez"""
        self.dialogo_activo = True
        self.dialogo_actual = 0
        self.linea_actual = 0
        self.dialogos = self.dialogos_originales.copy()
        
        # Solo generar monedas si es la primera vez y no se ha completado la misión
        if not self.mision_completada:
            self.mision_completada = True
            # Completar la misión
            if self.sistema_misiones:
                self.sistema_misiones.completar_mision("primera_mision")
                print("¡Primera misión completada! Las monedas aparecerán ahora.")
                
                # Verificar que tenemos todo lo necesario para generar monedas
                print(f"DEBUG: Verificando recursos para generar monedas:")
                print(f"DEBUG: - grupo_monedas: {'Disponible' if self.grupo_monedas is not None else 'None'}")
                print(f"DEBUG: - coin_images: {'Disponible' if self.coin_images is not None else 'None'}")
                
                if self.grupo_monedas is not None and self.coin_images is not None:
                    try:
                        # Limpiar monedas actuales
                        self.grupo_monedas.empty()
                        print("DEBUG: Grupo de monedas limpiado")
                        
                        # Generar una moneda de prueba junto al NPC
                        moneda = Item(self.rect.x + 100, self.rect.y, self.coin_images)
                        self.grupo_monedas.add(moneda)
                        print(f"DEBUG: Moneda de prueba generada en posición ({self.rect.x + 100}, {self.rect.y})")
                        
                        # Generar el resto de las monedas
                        monedas_restantes = generar_monedas(CANTIDAD_MONEDAS_MISION - 1, self.coin_images, self.sistema_misiones)
                        for moneda in monedas_restantes:
                            self.grupo_monedas.add(moneda)
                        print(f"DEBUG: Se generaron {len(monedas_restantes)} monedas adicionales")
                        
                        print(f"DEBUG: Total de monedas en el grupo: {len(self.grupo_monedas)}")
                    except Exception as e:
                        print(f"ERROR al generar monedas: {str(e)}")
                else:
                    print("ERROR: No se pueden generar monedas - grupo_monedas o coin_images es None")

    def mostrar_dialogo_insuficiente(self):
        """Muestra diálogo cuando el jugador no tiene suficientes monedas"""
        self.dialogo_activo = True
        self.dialogo_actual = 0
        self.linea_actual = 0
        self.dialogos = [
            ["Aún no tienes las 10 monedas necesarias.\n"
             "Sigue buscando por el mapa, encontrarás más monedas."]
        ]

    def mostrar_dialogo_comprar(self):
        """Muestra el diálogo cuando tiene las monedas pero aún no ha comprado el refugio"""
        if not self.dialogo_activo:
            self.dialogo_activo = True
            self.dialogo_actual = 0
            self.linea_actual = 0
            # Establecer el nuevo diálogo
            self.dialogos = [
                ["¡Excelente! Ya tienes las 10 monedas necesarias.\n"
                 "Ahora ve a comprar el refugio para poder comenzar\n"
                 "a rescatar animales. ¡Presiona Z en la puerta!"]
            ]

    def mostrar_dialogo_refugio_comprado(self):
        """Muestra el diálogo cuando ya ha comprado el refugio"""
        if not self.dialogo_activo:
            self.dialogo_activo = True
            self.dialogo_actual = 0
            self.linea_actual = 0
            # Establecer el nuevo diálogo
            self.dialogos = [
                ["¡Ehh! Ya veo que completaste la misión.\n"
                 "Pero sabías que el maltrato animal en Antioquia\n"
                 "es un problema grave? Muchos animales sufren\n"
                 "de abandono y maltrato diariamente."],
                ["En Colombia, más de 100.000 animales son\n"
                 "abandonados cada año, y Antioquia es una de las\n"
                 "regiones con mayor índice de maltrato animal.\n"
                 "¡Necesitamos tu ayuda para cambiar esto!"]
            ]

    def ocultar_dialogo(self):
        """Oculta el diálogo"""
        self.dialogo_activo = False
        self.dialogo_actual = 0
        self.linea_actual = 0

    def avanzar_dialogo(self):
        """Avanza el diálogo"""
        if not self.dialogo_activo:
            return

        self.linea_actual += 1

        # Si termina el cuadro actual, pasa al siguiente cuadro
        if self.linea_actual >= len(self.dialogos[self.dialogo_actual]):
            self.dialogo_actual += 1
            self.linea_actual = 0

            # Si ya no hay más cuadros, termina diálogo
            if self.dialogo_actual >= len(self.dialogos):
                self.ocultar_dialogo()

    def dibujar(self, ventana, camara):
        ventana.blit(self.image, camara.aplicar(self.rect))
        
        if self.dialogo_activo:
            self.dibujar_dialogo(ventana)

    def dibujar_dialogo(self, ventana):
        if not self.dialogo_activo:
            return

        # Fondo del cuadro de diálogo (semi-transparente negro)
        s = pygame.Surface((self.dialogo_rect.width, self.dialogo_rect.height))
        s.set_alpha(200)
        s.fill((0, 0, 0))
        ventana.blit(s, (self.dialogo_rect.x, self.dialogo_rect.y))

        # Dibujar borde blanco
        pygame.draw.rect(ventana, (255, 255, 255), self.dialogo_rect, 3)

        # Obtener la línea actual para mostrar
        texto = self.dialogos[self.dialogo_actual][self.linea_actual]

        # Renderizar texto multilínea (separado por '\n')
        lineas = texto.split('\n')
        for i, linea in enumerate(lineas):
            img_texto = self.fuente_dialogo.render(linea, True, (255, 255, 255))
            ventana.blit(img_texto, (self.dialogo_rect.x + 20, self.dialogo_rect.y + 20 + i * 30))

        # Mostrar texto según si es el último diálogo o no
        if self.dialogo_actual < len(self.dialogos) - 1:
            texto_pie = "Presiona P para continuar..."
        else:
            texto_pie = "Presiona P para cerrar"
        img_pie = self.fuente_pie.render(texto_pie, True, (255, 255, 255))
        # Ponerlo en la parte inferior dentro del cuadro, centrado a la izquierda con algo de margen
        ventana.blit(img_pie, (self.dialogo_rect.x + 20, self.dialogo_rect.y + self.dialogo_rect.height - 35))


def cargar_imagen_con_check(ruta):
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


def crear_npc_mision(sistema_misiones=None):
    """Crea y retorna una instancia del NPC de misión"""
    ruta_imagen = "recursos/imagenes/caracteres/humano/humano_mision.png"
    imagen = cargar_imagen_con_check(ruta_imagen)
    
    return NPCMision(1000, 1700, imagen, sistema_misiones)