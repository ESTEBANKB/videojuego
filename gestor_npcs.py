# gestor_npcs.py - Versión unificada y mejorada

import pygame
from npc import GatoNPC
from gato_humano import  crear_npc_humano
from npc_mision import crear_npc_mision
from NPC_informacion import NPCInformacion
from npc_general import crear_npc_general  # Importar el NPC general
from gato import cargar_imagenes_gato
from npc_bienvenida import NPCHumano  # Importar el NPC de bienvenida
from npc_vendedor import NPCVendedor  # Importar el NPC vendedor

class GestorNPCs:
    def __init__(self, sistema_misiones):
        self.sistema_misiones = sistema_misiones
        
        # Variables para evitar repetición de teclas
        self.tecla_e_presionada = False
        self.tecla_p_presionada = False
        
        # Crear NPCs con manejo de errores
        self.npc_bienvenida = self._crear_npc_bienvenida()  # Nuevo NPC de bienvenida
        self.npc_humano = self._crear_npc_humano()
        self.npc_mision = self._crear_npc_mision()
        self.gato = self._crear_gato()
        self.npc_informacion = self._crear_npc_informacion()
        self.npc_general = self._crear_npc_general()  # NUEVO: NPC General
        self.npc_vendedor = None  # Vendedor, inicialmente no existe
        
        # Lista de todos los NPCs para facilitar iteraciones
        self.todos_los_npcs = [
            ('npc_bienvenida', self.npc_bienvenida),  # Añadir a la lista
            ('npc_humano', self.npc_humano),
            ('npc_mision', self.npc_mision),
            ('npc_informacion', self.npc_informacion),
            ('npc_general', self.npc_general),
            ('gato', self.gato),
            ('npc_vendedor', self.npc_vendedor)  # Agregar el vendedor a la lista
        ]

    def _crear_npc_bienvenida(self):
        """Crea el NPC de bienvenida con manejo de errores"""
        try:
            npc = NPCHumano(300, 850, self.sistema_misiones)
            npc.visible = True  # Asegurar que el NPC sea visible por defecto
            return npc
        except Exception as e:
            print(f"Error creando NPC de bienvenida: {e}")
            return None

    def _crear_npc_humano(self):
        """Crea el NPC humano de bienvenida con manejo de errores"""
        try:
            return crear_npc_humano()
        except Exception as e:
            print(f"Error creando NPC humano: {e}")
            return None

    def _crear_npc_mision(self):
        """Crea el NPC de misión con manejo de errores"""
        try:
            return crear_npc_mision(self.sistema_misiones)
        except Exception as e:
            print(f"Error creando NPC de misión: {e}")
            return None

    def _crear_gato(self):
        """Crea el gato NPC con manejo de errores"""
        try:
            imagenes_gato = cargar_imagenes_gato()
            return GatoNPC(2430, 600, imagenes_gato)
        except Exception as e:
            print(f"Error creando gato: {e}")
            return None

    def _crear_npc_informacion(self):
        """Crea el NPC de información con manejo de errores"""
        try:
            return NPCInformacion(1800, 400, self.sistema_misiones)
        except Exception as e:
            print(f"Error creando NPC de Información: {e}")
            return None

    def _crear_npc_general(self):
        """Crea el NPC general con manejo de errores"""
        try:
            return crear_npc_general()
        except Exception as e:
            print(f"Error creando NPC General: {e}")
            return None

    def actualizar(self, personaje, teclas, grupo_item=None):
        """Actualiza la lógica de todos los NPCs"""
        # Asegurarse de que tenemos las teclas
        if teclas is None:
            teclas = pygame.key.get_pressed()
        
        # Actualizar gato
        if self.gato:
            try:
                # Pasar las teclas al gato
                self.gato.actualizar(personaje, teclas)
            except Exception as e:
                print(f"Error actualizando gato: {e}")
        
        # Actualizar NPCs con diálogo
        npcs_con_dialogo = [
            ('npc_bienvenida', self.npc_bienvenida),
            ('npc_humano', self.npc_humano),
            ('npc_mision', self.npc_mision),
            ('npc_informacion', self.npc_informacion),
            ('npc_general', self.npc_general)
        ]
        
        for nombre, npc in npcs_con_dialogo:
            if npc:
                try:
                    # Algunos NPCs tienen método actualizar específico
                    if hasattr(npc, 'actualizar'):
                        if nombre == 'npc_informacion':
                            npc.actualizar(personaje, teclas)
                        else:
                            npc.actualizar(personaje, teclas)
                except Exception as e:
                    print(f"Error actualizando {nombre}: {e}")
        
        # Actualizar vendedor si existe
        if self.npc_vendedor:
            self.npc_vendedor.actualizar(personaje)

    def manejar_evento_tecla(self, evento):
        """Maneja eventos específicos de teclas para los NPCs"""
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_e and not self.tecla_e_presionada:
                self.cerrar_todos_los_dialogos()
                self.tecla_e_presionada = True
                self._manejar_interaccion_e()
                
            elif evento.key == pygame.K_p and not self.tecla_p_presionada:
                self.tecla_p_presionada = True
                self._manejar_interaccion_p()
                
            # NUEVO: Manejar teclas numéricas para el NPC de información
            elif pygame.K_1 <= evento.key <= pygame.K_8:
                if (self.npc_informacion and 
                    hasattr(self.npc_informacion, 'dialogo_activo') and 
                    self.npc_informacion.dialogo_activo):
                    numero = evento.key - pygame.K_0
                    if hasattr(self.npc_informacion, 'seleccionar_tema'):
                        self.npc_informacion.seleccionar_tema(numero)
                
        elif evento.type == pygame.KEYUP:
            if evento.key == pygame.K_e:
                self.tecla_e_presionada = False
            elif evento.key == pygame.K_p:
                print("KEYUP de P recibido, reseteando tecla_p_presionada")
                self.tecla_p_presionada = False

    def _manejar_interaccion_e(self):
        """Maneja las interacciones con la tecla E"""
        # Esta función será llamada desde verificar_interacciones cuando se detecte colisión
        pass

    def _manejar_interaccion_p(self):
        """Maneja las interacciones con la tecla P para avanzar diálogos"""
        # Lista de NPCs que pueden tener diálogos activos
        npcs_con_dialogo = [
            self.npc_bienvenida,  # Añadir NPC de bienvenida
            self.npc_informacion,
            self.npc_mision,
            self.npc_humano,
            self.npc_general
        ]
        
        for npc in npcs_con_dialogo:
            if (npc and 
                hasattr(npc, 'dialogo_activo') and 
                npc.dialogo_activo and 
                hasattr(npc, 'avanzar_dialogo')):
                npc.avanzar_dialogo()
                break  # Solo avanzar un diálogo a la vez

    def verificar_interacciones(self, personaje):
        """Verifica las colisiones y maneja las interacciones con E"""
        if not self.tecla_e_presionada:
            return
        
        # Lista de NPCs interactuables con sus mensajes de activación
        npcs_interactuables = [
            (self.npc_bienvenida, 'NPC Bienvenida'),  # Añadir NPC de bienvenida
            (self.npc_humano, 'NPC Humano'),
            (self.npc_mision, 'NPC Misión'),
            (self.npc_informacion, 'NPC Información'),
            (self.npc_general, 'NPC General')
        ]
        
        for npc, nombre in npcs_interactuables:
            if npc and personaje.rect.colliderect(npc.rect):
                # Verificar si el diálogo no está ya activo
                dialogo_activo = (hasattr(npc, 'dialogo_activo') and npc.dialogo_activo) or \
                               (hasattr(npc, 'dialogo_visible') and npc.dialogo_visible)
                
                if not dialogo_activo:
                    # Activar diálogo según el tipo de NPC
                    if hasattr(npc, 'mostrar_dialogo'):
                        npc.mostrar_dialogo()
                        print(f"Activando diálogo de {nombre}")
                    elif hasattr(npc, 'dialogo_visible'):
                        npc.dialogo_visible = True
                        print(f"Activando diálogo visible de {nombre}")
                
                break  # Solo interactuar con un NPC a la vez

    def dibujar(self, ventana, camara):
        """Dibuja todos los NPCs en pantalla"""
        # Dibujar gato (tiene su propio método de dibujo)
        if self.gato:
            try:
                self.gato.dibujar(ventana, camara)
            except Exception as e:
                print(f"Error dibujando gato: {e}")
        
        # Dibujar NPCs con sprites y diálogos
        npcs_a_dibujar = [
            ('npc_bienvenida', self.npc_bienvenida),  # Añadir a la lista
            ('npc_humano', self.npc_humano),
            ('npc_mision', self.npc_mision),
            ('npc_informacion', self.npc_informacion),
            ('npc_general', self.npc_general)
        ]
        
        for nombre, npc in npcs_a_dibujar:
            if npc:
                try:
                    # Dibujar el sprite del NPC
                    if hasattr(npc, 'dibujar'):
                        npc.dibujar(ventana, camara)
                    else:
                        # Dibujo básico si no tiene método específico
                        ventana.blit(npc.image, camara.aplicar(npc.rect))
                    
                    # Dibujar diálogo si está activo
                    if hasattr(npc, 'dibujar_dialogo'):
                        npc.dibujar_dialogo(ventana)
                    elif (hasattr(npc, 'dialogo_visible') and 
                          npc.dialogo_visible and 
                          hasattr(npc, 'dibujar_dialogo')):
                        npc.dibujar_dialogo(ventana)
                        
                except Exception as e:
                    print(f"Error dibujando {nombre}: {e}")
        
        # Dibujar vendedor si existe
        if self.npc_vendedor:
            self.npc_vendedor.dibujar(ventana, camara)

    def dibujar_indicadores_interaccion(self, ventana, camara, personaje):
        """Dibuja indicadores de interacción cerca de NPCs"""
        fuente_pequena = pygame.font.Font(None, 24)
        
        # Lista de NPCs con sus mensajes
        npcs_con_indicadores = [
            (self.npc_bienvenida, "Presiona E para hablar"),  # Mensaje actualizado
            (self.npc_humano, "Presiona E para hablar con Rastafari"),
            (self.npc_mision, "Presiona E para misiones"),
            (self.npc_informacion, "Presiona E para información"),
            (self.npc_general, "Presiona E para consejos generales")
        ]
        
        for npc, mensaje in npcs_con_indicadores:
            if npc and personaje.rect.colliderect(npc.rect.inflate(50, 50)):
                # Verificar si el diálogo no está activo
                dialogo_activo = (hasattr(npc, 'dialogo_activo') and npc.dialogo_activo) or \
                               (hasattr(npc, 'dialogo_visible') and npc.dialogo_visible)
                
                if not dialogo_activo:
                    # Dibujar indicador sobre el NPC
                    pos_texto = camara.aplicar(pygame.Rect(npc.rect.x - 20, npc.rect.y - 30, 0, 0))
                    superficie_texto = fuente_pequena.render(mensaje, True, (255, 255, 255))
                    
                    # Fondo semi-transparente
                    fondo = pygame.Surface((superficie_texto.get_width() + 10, superficie_texto.get_height() + 5))
                    fondo.set_alpha(180)
                    fondo.fill((0, 0, 0))
                    
                    ventana.blit(fondo, (pos_texto.x - 5, pos_texto.y - 2))
                    ventana.blit(superficie_texto, pos_texto)

    def obtener_sistema_misiones(self):
        """Retorna el sistema de misiones"""
        return self.sistema_misiones

    def hay_dialogo_activo(self):
        """Verifica si algún NPC tiene un diálogo activo"""
        npcs_con_dialogo = [
            self.npc_bienvenida,  # Añadir NPC de bienvenida
            self.npc_humano,
            self.npc_mision,
            self.npc_informacion,
            self.npc_general
        ]
        
        for npc in npcs_con_dialogo:
            if npc:
                # Priorizar dialogo_activo si existe, si no, buscar dialogo_visible
                if (hasattr(npc, 'dialogo_activo') and npc.dialogo_activo) or \
                   (hasattr(npc, 'dialogo_visible') and npc.dialogo_visible):
                    return True
        return False

    def cerrar_todos_los_dialogos(self):
        """Cierra todos los diálogos activos"""
        npcs_con_dialogo = [
            self.npc_bienvenida,  # Añadir NPC de bienvenida
            self.npc_humano,
            self.npc_mision,
            self.npc_informacion,
            self.npc_general
        ]
        
        for npc in npcs_con_dialogo:
            if npc:
                if hasattr(npc, 'dialogo_activo'):
                    npc.dialogo_activo = False
                if hasattr(npc, 'dialogo_visible'):
                    npc.dialogo_visible = False
                # Reiniciar el índice del diálogo para la próxima vez
                if hasattr(npc, 'dialogo_actual'):
                    npc.dialogo_actual = 0
                if hasattr(npc, 'mostrar_menu'): # Para NPCInformacion
                    npc.mostrar_menu = True

    def actualizar_gato(self, personaje, escena_actual_obj, teclas):
        if not escena_actual_obj.puerta_refugio.refugio_comprado:
            if personaje.score >= escena_actual_obj.puerta_refugio.monedas_requeridas:
                if escena_actual_obj.puerta_refugio.verificar_entrada(personaje):
                    if teclas[pygame.K_z]:
                        personaje.score -= escena_actual_obj.puerta_refugio.monedas_requeridas
                        escena_actual_obj.puerta_refugio.refugio_comprado = True
                        print("Refugio comprado. Configurando gato para que sea visible.")
                        if hasattr(escena_actual_obj, 'gestor_npcs') and escena_actual_obj.gestor_npcs.gato:
                            gato = escena_actual_obj.gestor_npcs.gato
                            gato.rect.x = 2430
                            gato.rect.y = 600
                            gato.visible = True
                            gato.fue_rescatado = False
                            gato.siguiendo = False
                            print("Gato configurado para ser visible.")