# puerta_refugio.py
import pygame
import constantes

class PuertaRefugio:
    def __init__(self, world, tile_indices=[312, 313]):
        """
        Inicializa la puerta del refugio.
        
        Args:
            world: Instancia del mundo que contiene los tiles
            tile_indices: Lista de índices de los tiles que forman la puerta
        """
        self.world = world
        self.tile_indices = tile_indices
        self.monedas_requeridas = 10
        self.puerta_abierta = False
        self.mensaje_mostrado = False
        self.tiempo_mensaje = 0
        self.duracion_mensaje = 3000  # 3 segundos en milisegundos
        self.refugio_comprado = False  # Nuevo atributo para rastrear si el refugio ya fue comprado
        
        # Fuente para los mensajes
        self.fuente = pygame.font.Font(None, 36)
        
        # Colores para los mensajes
        self.color_bloqueado = (255, 0, 0)  # Rojo
        self.color_abierto = (0, 255, 0)    # Verde
        
    def verificar_entrada(self, personaje):
        """
        Verifica si el personaje puede entrar al refugio.
        
        Args:
            personaje: Instancia del personaje
            
        Returns:
            bool: True si puede entrar, False si no
        """
        # Verificar si el personaje está tocando algún tile de la puerta
        tocando_puerta = False
        
        if hasattr(self.world, 'map_tiles') and len(self.world.map_tiles) > max(self.tile_indices):
            for tile_index in self.tile_indices:
                if personaje.rect.colliderect(self.world.map_tiles[tile_index][1]):
                    tocando_puerta = True
                    break
        
        if tocando_puerta:
            # Si el refugio ya fue comprado, permitir entrada sin verificar monedas
            if self.refugio_comprado:
                if not self.puerta_abierta:
                    self.puerta_abierta = True
                    self.mostrar_mensaje_abierto()
                return True
            
            # Verificar si tiene suficientes monedas solo si no ha sido comprado
            if personaje.score >= self.monedas_requeridas:
                if not self.puerta_abierta:
                    self.puerta_abierta = True
                    self.mostrar_mensaje_abierto()
                return True
            else:
                # No tiene suficientes monedas
                self.mostrar_mensaje_bloqueado(personaje.score)
                return False
        
        return False
    
    def mostrar_mensaje_bloqueado(self, monedas_actuales):
        """Muestra mensaje cuando la puerta está bloqueada."""
        self.mensaje_mostrado = True
        self.tiempo_mensaje = pygame.time.get_ticks()
        
        monedas_faltantes = self.monedas_requeridas - monedas_actuales
        self.mensaje_actual = f"Puerta bloqueada! Ve y busca a Rodrigo"
        self.color_mensaje = self.color_bloqueado
        
    def mostrar_mensaje_abierto(self):
        """Muestra mensaje cuando la puerta se abre."""
        self.mensaje_mostrado = True
        self.tiempo_mensaje = pygame.time.get_ticks()
        self.mensaje_actual = "¡Puerta desbloqueada! Presiona Z para entrar"
        self.color_mensaje = self.color_abierto
        
    def actualizar_mensaje(self):
        """Actualiza el estado del mensaje."""
        if self.mensaje_mostrado:
            tiempo_actual = pygame.time.get_ticks()
            if tiempo_actual - self.tiempo_mensaje >= self.duracion_mensaje:
                self.mensaje_mostrado = False
                
    def dibujar_mensaje(self, ventana):
        """Dibuja el mensaje en pantalla si está activo."""
        if self.mensaje_mostrado:
            # Crear superficie del texto
            texto_surface = self.fuente.render(self.mensaje_actual, True, self.color_mensaje)
            texto_rect = texto_surface.get_rect()
            
            # Centrar el mensaje en la parte superior de la pantalla
            texto_rect.centerx = constantes.ANCHO_VENTANA // 2
            texto_rect.y = 100
            
            # Dibujar fondo semitransparente para el mensaje
            fondo_rect = texto_rect.inflate(20, 10)
            fondo_surface = pygame.Surface((fondo_rect.width, fondo_rect.height))
            fondo_surface.set_alpha(180)
            fondo_surface.fill((0, 0, 0))
            
            ventana.blit(fondo_surface, fondo_rect)
            ventana.blit(texto_surface, texto_rect)
    
    def dibujar_indicador_puerta(self, ventana, camara):
        """Dibuja un indicador visual sobre la puerta."""
        if hasattr(self.world, 'map_tiles') and len(self.world.map_tiles) > max(self.tile_indices):
            # Obtener la posición del primer tile de la puerta
            tile_rect = self.world.map_tiles[self.tile_indices[0]][1]
            
            # Calcular posición del indicador aplicando la cámara
            indicador_x = tile_rect.centerx - camara.camara_rect.x
            indicador_y = tile_rect.y - 30 - camara.camara_rect.y
            
            # Elegir color y símbolo según el estado
            if self.puerta_abierta:
                color = self.color_abierto
                simbolo = "✓"
            else:
                color = self.color_bloqueado
                simbolo = "✗"
            
            # Dibujar círculo de fondo
            pygame.draw.circle(ventana, (0, 0, 0), (indicador_x, indicador_y), 15)
            pygame.draw.circle(ventana, color, (indicador_x, indicador_y), 12)
            
            # Dibujar símbolo
            fuente_simbolo = pygame.font.Font(None, 24)
            simbolo_surface = fuente_simbolo.render(simbolo, True, (255, 255, 255))
            simbolo_rect = simbolo_surface.get_rect(center=(indicador_x, indicador_y))
            ventana.blit(simbolo_surface, simbolo_rect)
    
    def reiniciar(self):
        """Reinicia el estado de la puerta (útil al cambiar de escena)."""
        self.puerta_abierta = False
        self.mensaje_mostrado = False
        self.tiempo_mensaje = 0
        
    def obtener_progreso(self, monedas_actuales):
        """
        Obtiene información sobre el progreso hacia abrir la puerta.
        
        Args:
            monedas_actuales: Número actual de monedas del personaje
            
        Returns:
            dict: Información del progreso
        """
        return {
            'monedas_actuales': monedas_actuales,
            'monedas_requeridas': self.monedas_requeridas,
            'monedas_faltantes': max(0, self.monedas_requeridas - monedas_actuales),
            'puede_entrar': monedas_actuales >= self.monedas_requeridas,
            'porcentaje': min(100, (monedas_actuales / self.monedas_requeridas) * 100)
        }