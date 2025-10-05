# gestor_escenas.py - Sistema de gestión de escenas del juego

from enum import Enum
import pygame
import constantes
from refugio import Refugio
from colisiones_refugio import ColisionesRefugio
from camara import Camara


class TipoEscena(Enum):
    """Enumera los tipos de escenas disponibles en el juego."""
    MAPA_PRINCIPAL = "mapa_principal"
    REFUGIO = "refugio"

class GestorEscenas:
    """
    Clase que gestiona las diferentes escenas del juego.
    Controla el cambio entre escenas y su inicialización/limpieza.
    """
    
    def __init__(self):
        """Inicializa el gestor de escenas."""
        self.escena_actual = None
        self.escenas = {}
        self.en_transicion = False
        
    def registrar_escena(self, tipo_escena, escena):
        """
        Registra una nueva escena en el gestor.
        
        Args:
            tipo_escena (TipoEscena): El tipo de escena a registrar
            escena: La instancia de la escena a registrar
        """
        self.escenas[tipo_escena] = escena
        print(f"Escena registrada: {tipo_escena.value}")
        
    def cambiar_escena(self, nuevo_tipo_escena, personaje=None):
        """
        Cambia a una nueva escena.
        
        Args:
            nuevo_tipo_escena (TipoEscena): El tipo de escena a la que cambiar
            personaje: Referencia al personaje (opcional)
            
        Returns:
            bool: True si el cambio fue exitoso, False si falló
        """
        if self.en_transicion:
            return False
            
        self.en_transicion = True
        
        # Limpiar escena anterior
        if self.escena_actual:
            self.limpiar_escena_actual()
            
        # Activar nueva escena
        if nuevo_tipo_escena in self.escenas:
            self.escena_actual = nuevo_tipo_escena
            escena = self.escenas[nuevo_tipo_escena]
            
            # Inicializar la nueva escena si tiene el método
            if hasattr(escena, 'inicializar_escena'):
                escena.inicializar_escena(personaje)
                
            print(f"Cambiado a escena: {nuevo_tipo_escena.value}")
            self.en_transicion = False
            return True
        else:
            print(f"Error: Escena no encontrada: {nuevo_tipo_escena.value}")
            self.en_transicion = False
            return False
    
    def limpiar_escena_actual(self):
        """Limpia los recursos de la escena actual antes del cambio."""
        if self.escena_actual and self.escena_actual in self.escenas:
            escena = self.escenas[self.escena_actual]
            
            # Limpiar colisiones si existen
            if hasattr(escena, 'colisiones') and hasattr(escena.colisiones, 'solid_tiles'):
                escena.colisiones.solid_tiles.empty()
                print(f"Colisiones limpiadas para escena: {self.escena_actual.value}")
                
            # Limpiar NPCs si existen
            if hasattr(escena, 'npcs_activos'):
                escena.npcs_activos = False
                
            # Llamar al método de limpieza personalizado si existe
            if hasattr(escena, 'limpiar_escena'):
                escena.limpiar_escena()
    
    def obtener_escena_actual(self):
        """
        Obtiene la instancia de la escena actual.
        
        Returns:
            La instancia de la escena actual o None si no hay escena activa
        """
        if self.escena_actual:
            return self.escenas.get(self.escena_actual)
        return None
    
    def obtener_tipo_escena_actual(self):
        """
        Obtiene el tipo de la escena actual.
        
        Returns:
            TipoEscena: El tipo de la escena actual o None
        """
        return self.escena_actual
    
    def esta_en_transicion(self):
        """
        Verifica si el gestor está en proceso de transición.
        
        Returns:
            bool: True si está en transición, False si no
        """
        return self.en_transicion
    
    def listar_escenas_registradas(self):
        """
        Lista todas las escenas registradas.
        
        Returns:
            list: Lista con los tipos de escenas registradas
        """
        return list(self.escenas.keys())
    
    def escena_existe(self, tipo_escena):
        """
        Verifica si una escena está registrada.
        
        Args:
            tipo_escena (TipoEscena): El tipo de escena a verificar
            
        Returns:
            bool: True si la escena existe, False si no
        """
        return tipo_escena in self.escenas


# Clase para el mapa principal - VERSIÓN MEJORADA CON INTEGRACIÓN DE NPCs
class MapaPrincipal:
    def __init__(self, personaje, world, colisiones, camara, grupo_item, puerta_refugio, gestor_npcs):
        self.personaje = personaje
        self.world = world
        self.colisiones = colisiones
        self.camara = camara
        self.grupo_item = grupo_item
        self.puerta_refugio = puerta_refugio
        self.gestor_npcs = gestor_npcs  # Usar el gestor de NPCs
        self.npcs_activos = True
        self.activa = False
        
    def inicializar_escena(self, personaje=None):
        self.activa = True
        self.npcs_activos = True
        
        # Recargar colisiones del mapa principal si es necesario
        if hasattr(self, 'word_data'):
            self.colisiones.solid_tiles.empty()
            self.colisiones.cargar_colisiones(self.word_data)
            
        print("Mapa principal inicializado - Colisiones:", len(self.colisiones.solid_tiles))
        
    def limpiar_escena(self):
        self.activa = False
        self.npcs_activos = False
        if self.colisiones and hasattr(self.colisiones, 'solid_tiles'):
            self.colisiones.solid_tiles.empty()
            
    def actualizar(self, teclas):
        if not self.activa:
            return
            
        # Mover personaje con colisiones del mapa principal
        self.personaje.mover(teclas, self.colisiones)
        
        # Actualizar cámara
        self.camara.update(self.personaje)
        
        # Actualizar sistema de puerta
        self.puerta_refugio.actualizar_mensaje()
        
        # Actualizar NPCs usando el gestor
        if self.npcs_activos:
            self.gestor_npcs.actualizar(self.personaje, teclas, self.grupo_item)
                    
        # Actualizar items
        self.grupo_item.update(self.personaje)

    def _dibujar_indicadores_interaccion(self, ventana):
        """Dibuja indicadores de interacción cerca de NPCs"""
        fuente_pequena = pygame.font.Font(None, 24)
        
        # Verificar proximidad con NPCs y mostrar indicadores
        if self.gestor_npcs.npc_humano:
            distancia = abs(self.personaje.rect.centerx - self.gestor_npcs.npc_humano.rect.centerx) + \
                       abs(self.personaje.rect.centery - self.gestor_npcs.npc_humano.rect.centery)
            if distancia < 80:  # Si está cerca
                pos_texto = self.camara.aplicar(pygame.Rect(
                    self.gestor_npcs.npc_humano.rect.x - 20, 
                    self.gestor_npcs.npc_humano.rect.y - 30, 0, 0))
                superficie_texto = fuente_pequena.render("Presiona E para hablar", True, (255, 255, 255))
                
                # Fondo semi-transparente
                fondo = pygame.Surface((superficie_texto.get_width() + 10, superficie_texto.get_height() + 5))
                fondo.set_alpha(180)
                fondo.fill((0, 0, 0))
                
                ventana.blit(fondo, (pos_texto.x - 5, pos_texto.y - 2))
                ventana.blit(superficie_texto, pos_texto)
        
        # Similar para otros NPCs
        if self.gestor_npcs.npc_mision:
            distancia = abs(self.personaje.rect.centerx - self.gestor_npcs.npc_mision.rect.centerx) + \
                       abs(self.personaje.rect.centery - self.gestor_npcs.npc_mision.rect.centery)
            if distancia < 80:
                pos_texto = self.camara.aplicar(pygame.Rect(
                    self.gestor_npcs.npc_mision.rect.x - 20, 
                    self.gestor_npcs.npc_mision.rect.y - 30, 0, 0))
                superficie_texto = fuente_pequena.render("Presiona E para misiones", True, (255, 255, 255))
                
                fondo = pygame.Surface((superficie_texto.get_width() + 10, superficie_texto.get_height() + 5))
                fondo.set_alpha(180)
                fondo.fill((0, 0, 0))
                
                ventana.blit(fondo, (pos_texto.x - 5, pos_texto.y - 2))
                ventana.blit(superficie_texto, pos_texto)
        
        if self.gestor_npcs.npc_informacion:
            distancia = abs(self.personaje.rect.centerx - self.gestor_npcs.npc_informacion.rect.centerx) + \
                       abs(self.personaje.rect.centery - self.gestor_npcs.npc_informacion.rect.centery)
            if distancia < 80:
                pos_texto = self.camara.aplicar(pygame.Rect(
                    self.gestor_npcs.npc_informacion.rect.x - 20, 
                    self.gestor_npcs.npc_informacion.rect.y - 30, 0, 0))
                superficie_texto = fuente_pequena.render("Presiona E para información", True, (255, 255, 255))
                
                fondo = pygame.Surface((superficie_texto.get_width() + 10, superficie_texto.get_height() + 5))
                fondo.set_alpha(180)
                fondo.fill((0, 0, 0))
                
                ventana.blit(fondo, (pos_texto.x - 5, pos_texto.y - 2))
                ventana.blit(superficie_texto, pos_texto)
        
    def dibujar(self, ventana):
        if not self.activa:
            return
            
        # Dibujar el mundo ajustado a la cámara
        for tile in self.world.map_tiles:
            ventana.blit(tile[0], self.camara.aplicar(tile[1]))
            
        # Dibujar items
        for item in self.grupo_item:
            ventana.blit(item.image, self.camara.aplicar(item))
            
        # Dibujar NPCs usando el gestor
        if self.npcs_activos:
            self.gestor_npcs.dibujar(ventana, self.camara)
            
            # Dibujar indicadores de interacción
            self._dibujar_indicadores_interaccion(ventana)
        
        # Dibujar indicador de la puerta
        self.puerta_refugio.dibujar_indicador_puerta(ventana, self.camara)
        
        # Dibujar mensaje de la puerta
        self.puerta_refugio.dibujar_mensaje(ventana)


# Clase mejorada del refugio con cámara corregida
class RefugioMejorado:
    def __init__(self, personaje):
        self.personaje = personaje
        self.refugio_original = Refugio(personaje)
        self.colisiones = ColisionesRefugio()
        self.camara = None
        self.activa = False
        self.posicion_entrada = (300, 300)  # Posición donde aparece el personaje
        self.gestor_npcs = None  # Referencia al gestor de NPCs
        self.gato_posicion_refugio = None  # Nueva variable para guardar la posición del gato en el refugio
        
        # Configurar cámara del refugio
        ancho_refugio = constantes.COLUMNAS_REFUGIO * constantes.CUADRICULA_TAMAÑO
        alto_refugio = constantes.FILAS_REFUGIO * constantes.CUADRICULA_TAMAÑO
        self.camara = Camara(ancho_refugio, alto_refugio)
        
    def inicializar_escena(self, personaje=None):
        self.activa = True
        
        if personaje:
            self.personaje = personaje
            
        # Limpiar colisiones anteriores
        self.colisiones.solid_tiles.empty()
        
        # Recargar colisiones del refugio
        self.colisiones.cargar_colisiones(self.refugio_original.mapa_refugio)
        
        # Posicionar personaje en la entrada
        self.personaje.rect.x = self.posicion_entrada[0]
        self.personaje.rect.y = self.posicion_entrada[1]
        
        # Posicionar gato si existe
        if self.gestor_npcs and self.gestor_npcs.gato:
            if self.gato_posicion_refugio:
                # Si hay una posición guardada del gato en el refugio, usarla
                self.gestor_npcs.gato.rect.x = self.gato_posicion_refugio[0]
                self.gestor_npcs.gato.rect.y = self.gato_posicion_refugio[1]
            else:
                # Si no hay posición guardada, ponerlo cerca del personaje
                self.gestor_npcs.gato.rect.x = self.posicion_entrada[0] + 50
                self.gestor_npcs.gato.rect.y = self.posicion_entrada[1]
        
        print("Refugio inicializado - Colisiones:", len(self.colisiones.solid_tiles))
        
    def limpiar_escena(self):
        self.activa = False
        if self.colisiones and hasattr(self.colisiones, 'solid_tiles'):
            self.colisiones.solid_tiles.empty()
            
    def actualizar(self, teclas):
        if not self.activa:
            return
            
        # Mover personaje con colisiones del refugio
        self.personaje.mover(teclas, self.colisiones)
        
        # Actualizar gato si existe
        if self.gestor_npcs and self.gestor_npcs.gato:
            # Actualizar el gato con las teclas para mantener sus animaciones
            self.gestor_npcs.gato.actualizar(self.personaje, teclas)
            
            # Si el gato no está siguiendo, guardar su posición en el refugio
            if not self.gestor_npcs.gato.siguiendo:
                self.gato_posicion_refugio = (self.gestor_npcs.gato.rect.x, self.gestor_npcs.gato.rect.y)
        
        # Actualizar cámara del refugio
        self.camara.update(self.personaje)
        
        # Actualizar lógica específica del refugio
        self.refugio_original.actualizar()
        
    def dibujar(self, ventana):
        """Dibuja todos los elementos del refugio"""
        # Dibujar el mapa del refugio tile por tile usando la cámara de RefugioMejorado
        scroll = self.camara.camara_rect
        for y, fila in enumerate(self.refugio_original.mapa_refugio):
            for x, tile in enumerate(fila):
                if 0 <= tile < len(self.refugio_original.tile_list_refugio):
                    imagen_tile = self.refugio_original.tile_list_refugio[tile]
                    if imagen_tile:
                        ventana.blit(imagen_tile, (x * constantes.CUADRICULA_TAMAÑO - scroll.x,
                            y * constantes.CUADRICULA_TAMAÑO - scroll.y))
                else:
                    print(f"Tile fuera de rango: {tile} en posición ({x},{y})")
        # Dibujar gato si existe
        if self.gestor_npcs and self.gestor_npcs.gato:
            self.gestor_npcs.gato.dibujar(ventana, self.camara)