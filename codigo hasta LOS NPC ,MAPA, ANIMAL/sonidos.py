import pygame
import os
import sys

def resource_path(relative_path):
    """Obtiene la ruta absoluta del recurso, funciona para desarrollo y para PyInstaller"""
    try:
        # PyInstaller crea un directorio temporal y almacena la ruta en _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class SistemaSonido:
    def __init__(self):
        # Inicializar el sistema de sonido de pygame
        pygame.mixer.init()
        
        # Configurar volumen inicial
        self.volumen_musica = 0.3  # Reducido para no ser tan intrusivo
        self.volumen_efectos = 0.4  # Reducido para los pasos
        
        # Cargar los sonidos
        self.cargar_sonidos()
        
        # Iniciar música de fondo
        self.iniciar_musica_fondo()
    
    def cargar_sonidos(self):
        """Carga todos los sonidos del juego"""
        ruta_sonidos = resource_path(os.path.join("recursos", "sonidos"))
        
        # Cargar música de fondo
        self.musica_fondo = os.path.join(ruta_sonidos, "fondo_1.wav")
        
        # Cargar efectos de sonido
        self.sonido_pasos = pygame.mixer.Sound(os.path.join(ruta_sonidos, "pasos_1.wav"))
        self.sonido_moneda = pygame.mixer.Sound(os.path.join(ruta_sonidos, "moneda_1.wav"))
        
        # Configurar volumen de efectos
        self.sonido_pasos.set_volume(self.volumen_efectos)
        self.sonido_moneda.set_volume(self.volumen_efectos)
        
        # Configurar el sonido de pasos para que sea más suave
        self.sonido_pasos.set_volume(0.3)  # Volumen más bajo para los pasos
    
    def iniciar_musica_fondo(self):
        """Inicia la música de fondo en loop"""
        try:
            pygame.mixer.music.load(self.musica_fondo)
            pygame.mixer.music.set_volume(self.volumen_musica)
            pygame.mixer.music.play(-1)  # -1 para loop infinito
        except Exception as e:
            print(f"Error al cargar la música de fondo: {e}")
    
    def reproducir_pasos(self):
        """Reproduce el sonido de pasos con un pequeño retraso aleatorio para sonar más natural"""
        # Solo reproducir si no está ya sonando
        if not pygame.mixer.get_busy():
            self.sonido_pasos.play()
    
    def reproducir_moneda(self):
        """Reproduce el sonido de recolección de moneda"""
        self.sonido_moneda.play()
    
    def pausar_musica(self):
        """Pausa la música de fondo"""
        pygame.mixer.music.pause()
    
    def reanudar_musica(self):
        """Reanuda la música de fondo"""
        pygame.mixer.music.unpause()
    
    def detener_musica(self):
        """Detiene la música de fondo"""
        pygame.mixer.music.stop()
    
    def ajustar_volumen_musica(self, volumen):
        """Ajusta el volumen de la música de fondo (0.0 a 1.0)"""
        self.volumen_musica = max(0.0, min(1.0, volumen))
        pygame.mixer.music.set_volume(self.volumen_musica)
    
    def ajustar_volumen_efectos(self, volumen):
        """Ajusta el volumen de los efectos de sonido (0.0 a 1.0)"""
        self.volumen_efectos = max(0.0, min(1.0, volumen))
        self.sonido_pasos.set_volume(self.volumen_efectos)
        self.sonido_moneda.set_volume(self.volumen_efectos)
