# mapa_principal.py
import pygame
import constantes
from refugio import Refugio

class MapaPrincipal:
    def __init__(self, personaje, world, colisiones, camara, grupo_item, puerta_refugio, gestor_npcs):
        self.personaje = personaje
        self.world = world
        self.colisiones = colisiones
        self.camara = camara
        self.grupo_item = grupo_item
        self.puerta_refugio = puerta_refugio
        self.gestor_npcs = gestor_npcs
        self.npcs_activos = True
        self.activa = False
        self.gato = None  # Referencia al gato
        
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
        
        # Actualizar gato si existe
        if self.gato:
            # Aquí puedes agregar la lógica de movimiento del gato
            # Por ejemplo, que siga al personaje
            self.gato.rect.x = self.personaje.rect.x + 50
            self.gato.rect.y = self.personaje.rect.y
                    
        # Actualizar items
        self.grupo_item.update(self.personaje)
        
    def _dibujar_indicadores_interaccion(self, ventana):
        fuente_pequena = pygame.font.Font(None, 24)
        
        # Indicador para el NPC de misión
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
        
        # Indicador para el NPC de información
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
        
        # Dibujar gato si existe
        if self.gato:
            self.gato.dibujar(ventana, self.camara)
