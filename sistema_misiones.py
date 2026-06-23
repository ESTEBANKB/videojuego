# ===============================
# ARCHIVO: sistema_misiones.py (COMPLETO)
# ===============================
import json
import os

class SistemaMisiones:
    def __init__(self, archivo_guardado="progreso_juego.json"):
        self.archivo_guardado = archivo_guardado
        self.misiones_completadas = set()
        self.flags_juego = {}
        self.cargar_progreso()
    
    def completar_mision(self, id_mision):
        """Marca una misión como completada y guarda el progreso"""
        self.misiones_completadas.add(id_mision)
        self.guardar_progreso()
        print(f"¡Misión '{id_mision}' completada!")
    
    def esta_mision_completada(self, id_mision):
        """Verifica si una misión específica está completada"""
        return id_mision in self.misiones_completadas
    
    def establecer_flag(self, nombre_flag, valor):
        """Establece un flag del juego"""
        self.flags_juego[nombre_flag] = valor
        self.guardar_progreso()
    
    def obtener_flag(self, nombre_flag, valor_por_defecto=False):
        """Obtiene el valor de un flag del juego"""
        return self.flags_juego.get(nombre_flag, valor_por_defecto)
    
    def guardar_progreso(self):
        """Guarda el progreso del juego en un archivo JSON"""
        datos = {
            "misiones_completadas": list(self.misiones_completadas),
            "flags_juego": self.flags_juego
        }
        try:
            with open(self.archivo_guardado, 'w') as archivo:
                json.dump(datos, archivo, indent=2)
        except Exception as e:
            print(f"Error al guardar progreso: {e}")
    
    def cargar_progreso(self):
        """Carga el progreso del juego desde un archivo JSON"""
        if os.path.exists(self.archivo_guardado):
            try:
                with open(self.archivo_guardado, 'r') as archivo:
                    datos = json.load(archivo)
                    self.misiones_completadas = set(datos.get("misiones_completadas", []))
                    self.flags_juego = datos.get("flags_juego", {})
                    print("Progreso cargado exitosamente")
            except Exception as e:
                print(f"Error al cargar progreso: {e}")
        else:
            print("No se encontró archivo de progreso, iniciando juego nuevo")
    
    def reiniciar_progreso(self):
        """Reinicia todo el progreso del juego"""
        self.misiones_completadas.clear()
        self.flags_juego.clear()
        self.guardar_progreso()
        print("Progreso del juego reiniciado")
    
    def obtener_progreso_completo(self):
        """Retorna un diccionario con todo el progreso actual"""
        return {
            "misiones_completadas": list(self.misiones_completadas),
            "flags_juego": self.flags_juego.copy()
        }