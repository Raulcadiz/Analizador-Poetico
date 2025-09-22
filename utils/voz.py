import threading
import time
import platform
import logging
import subprocess
import os
from threading import Lock

class SistemaVoz:
    def __init__(self):
        self.engine = None
        self.is_speaking = False
        self.stop_speaking = False
        self.engine_lock = Lock()
        self.engine_available = False
        
        # Configuración optimizada para poesía
        self.config_default = {
            'velocidad': 150,
            'volumen': 0.9,
            'pausa_verso': 0.8,
            'pausa_estrofa': 1.5,
            'voz_seleccionada': None
        }
        
        self.voces_disponibles = []
        self.voces_espanol = []
        
        self.inicializar_engine()
    
    def inicializar_engine(self):
        """Inicialización robusta del motor de voz"""
        try:
            import pyttsx3
            
            # Intentar diferentes drivers según la plataforma
            drivers = []
            if platform.system() == "Windows":
                drivers = ['sapi5']
            elif platform.system() == "Darwin":  # macOS
                drivers = ['nsss']
            else:  # Linux
                drivers = ['espeak']
            
            for driver in drivers:
                try:
                    self.engine = pyttsx3.init(driverName=driver)
                    
                    # Verificar que funciona
                    voices = self.engine.getProperty('voices')
                    if voices:
                        self.engine_available = True
                        logging.info(f"Motor de voz inicializado con {driver}")
                        break
                    else:
                        if self.engine:
                            self.engine.stop()
                        self.engine = None
                        
                except Exception as e:
                    logging.warning(f"Fallo con driver {driver}: {e}")
                    continue
            
            if self.engine_available:
                self.configurar_engine()
                self.cargar_voces()
            else:
                logging.error("No se pudo inicializar motor de voz")
                
        except ImportError:
            logging.error("pyttsx3 no está instalado")
            self.engine_available = False
        except Exception as e:
            logging.error(f"Error general: {e}")
            self.engine_available = False
    
    def configurar_engine(self):
        """Configuración inicial del engine"""
        try:
            if not self.engine:
                return
            
            # Configurar propiedades básicas
            self.engine.setProperty('rate', self.config_default['velocidad'])
            self.engine.setProperty('volume', self.config_default['volumen'])
            
            # Para Windows, forzar inicialización
            if platform.system() == "Windows":
                try:
                    self.engine.say("")
                    self.engine.runAndWait()
                except:
                    pass
            
        except Exception as e:
            logging.warning(f"Error en configuración: {e}")
    
    def cargar_voces(self):
        """Carga voces disponibles"""
        if not self.engine:
            return
        
        try:
            voices = self.engine.getProperty('voices')
            
            if not voices:
                logging.warning("No se encontraron voces")
                return
            
            self.voces_disponibles = []
            self.voces_espanol = []
            
            for voice in voices:
                try:
                    voice_info = {
                        'id': voice.id,
                        'name': getattr(voice, 'name', 'Voz sin nombre'),
                        'lang': self._extraer_idioma(voice),
                        'gender': getattr(voice, 'gender', 'unknown')
                    }
                    
                    self.voces_disponibles.append(voice_info)
                    
                    # Filtrar voces en español
                    if self._es_voz_espanol(voice_info):
                        self.voces_espanol.append(voice_info)
                        
                except Exception as e:
                    logging.warning(f"Error procesando voz: {e}")
                    continue
            
            # Seleccionar mejor voz española
            self._seleccionar_voz_espanol()
            
            logging.info(f"Cargadas {len(self.voces_disponibles)} voces ({len(self.voces_espanol)} en español)")
            
        except Exception as e:
            logging.error(f"Error cargando voces: {e}")
    
    def _extraer_idioma(self, voice):
        """Extrae idioma de la voz"""
        try:
            for attr in ['lang', 'language', 'languages']:
                value = getattr(voice, attr, None)
                if value:
                    if isinstance(value, (list, tuple)):
                        return str(value[0]) if value else 'unknown'
                    return str(value)
            
            # Inferir del nombre
            name = str(getattr(voice, 'name', '')).lower()
            if any(esp in name for esp in ['spanish', 'español', 'helena', 'sabina', 'miguel', 'lucia']):
                return 'es-ES'
            
            return 'unknown'
            
        except Exception:
            return 'unknown'
    
    def _es_voz_espanol(self, voice_info):
        """Determina si una voz es española"""
        lang_str = str(voice_info['lang']).lower()
        name_str = str(voice_info['name']).lower()
        
        return (any(esp in lang_str for esp in ['es', 'spa', 'spanish', 'español']) or
                any(esp in name_str for esp in ['spanish', 'español', 'helena', 'sabina', 'miguel', 'lucia', 'pablo']))
    
    def _seleccionar_voz_espanol(self):
        """Selecciona la mejor voz española"""
        try:
            if not self.voces_espanol:
                return
            
            # Preferir voces femeninas
            voces_femeninas = [v for v in self.voces_espanol 
                             if any(fem in v['name'].lower() for fem in ['helena', 'sabina', 'lucia', 'female', 'zira'])]
            
            voice_id = None
            if voces_femeninas:
                voice_id = voces_femeninas[0]['id']
            else:
                voice_id = self.voces_espanol[0]['id']
            
            # Aplicar la voz
            self.engine.setProperty('voice', voice_id)
            self.config_default['voz_seleccionada'] = voice_id
            
            logging.info(f"Voz seleccionada: {voice_id}")
            
        except Exception as e:
            logging.warning(f"Error seleccionando voz: {e}")
    
    def hablar_con_config(self, texto, configuracion=None):
        """Método principal para síntesis de voz"""
        if not self.engine_available or not texto.strip():
            return self._hablar_fallback(texto)
        
        # Detener síntesis anterior
        self.detener()
        
        # Configurar
        config = configuracion or self.config_default
        self._aplicar_configuracion(config)
        
        # Ejecutar en hilo separado
        def _ejecutar():
            try:
                self.is_speaking = True
                self.stop_speaking = False
                self._procesar_texto_poetico(texto, config)
            except Exception as e:
                logging.error(f"Error en síntesis: {e}")
            finally:
                self.is_speaking = False
        
        thread = threading.Thread(target=_ejecutar, daemon=True)
        thread.start()
        
        return True
    
    def _aplicar_configuracion(self, config):
        """Aplica configuración al engine"""
        try:
            if not self.engine:
                return
            
            with self.engine_lock:
                self.engine.setProperty('rate', max(50, min(400, config.get('velocidad', 150))))
                self.engine.setProperty('volume', max(0.0, min(1.0, config.get('volumen', 0.9))))
                
                if config.get('voz_seleccionada'):
                    self.engine.setProperty('voice', config['voz_seleccionada'])
                    
        except Exception as e:
            logging.warning(f"Error aplicando configuración: {e}")
    
    def _procesar_texto_poetico(self, texto, config):
        """Procesa texto poético con pausas"""
        try:
            # Dividir en estrofas
            estrofas = [e.strip() for e in texto.split('\n\n') if e.strip()]
            if not estrofas:
                estrofas = [texto.strip()]
            
            for i, estrofa in enumerate(estrofas):
                if self.stop_speaking:
                    break
                
                versos = [v.strip() for v in estrofa.split('\n') if v.strip()]
                
                for j, verso in enumerate(versos):
                    if self.stop_speaking:
                        break
                    
                    # Síntesis del verso
                    self._hablar_verso(verso)
                    
                    # Pausa entre versos
                    if j < len(versos) - 1 and not self.stop_speaking:
                        time.sleep(config.get('pausa_verso', 0.8))
                
                # Pausa entre estrofas
                if i < len(estrofas) - 1 and not self.stop_speaking:
                    time.sleep(config.get('pausa_estrofa', 1.5))
                    
        except Exception as e:
            logging.error(f"Error procesando texto: {e}")
    
    def _hablar_verso(self, verso):
        """Habla un verso individual"""
        if not verso.strip() or self.stop_speaking:
            return
        
        try:
            with self.engine_lock:
                if self.engine and not self.stop_speaking:
                    verso_procesado = self._preparar_verso(verso)
                    self.engine.say(verso_procesado)
                    self.engine.runAndWait()
                    
        except Exception as e:
            logging.warning(f"Error hablando verso: {e}")
    
    def _preparar_verso(self, verso):
        """Prepara verso para síntesis"""
        # Expandir abreviaciones
        verso = verso.replace('q.', 'que')
        verso = verso.replace('etc.', 'etcétera')
        verso = verso.replace('Sr.', 'Señor')
        verso = verso.replace('Sra.', 'Señora')
        
        return verso
    
    def _hablar_fallback(self, texto):
        """Sistema de respaldo"""
        try:
            if platform.system() == "Windows":
                # PowerShell para Windows
                texto_limpio = texto.replace('"', '').replace("'", "")[:200]
                
                command = f'''powershell -Command "Add-Type -AssemblyName System.Speech; $speak = New-Object System.Speech.Synthesis.SpeechSynthesizer; $speak.Rate = 2; $speak.Speak('{texto_limpio}')"'''
                
                def _ejecutar_powershell():
                    try:
                        subprocess.run(command, shell=True, capture_output=True, timeout=30)
                    except Exception as e:
                        logging.warning(f"Error en PowerShell: {e}")
                
                thread = threading.Thread(target=_ejecutar_powershell, daemon=True)
                thread.start()
                
                return True
            else:
                # Para Linux/Mac
                try:
                    subprocess.run(['espeak', '-v', 'es', '-s', '150', texto[:200]], 
                                 capture_output=True, timeout=30)
                    return True
                except:
                    print(f"[SÍNTESIS FALLBACK] {texto}")
                    return True
                    
        except Exception as e:
            logging.error(f"Error en fallback: {e}")
            print(f"[VOZ NO DISPONIBLE] {texto}")
            return False
    
    def detener(self):
        """Detiene la síntesis"""
        self.stop_speaking = True
        self.is_speaking = False
        
        try:
            with self.engine_lock:
                if self.engine:
                    self.engine.stop()
        except Exception as e:
            logging.warning(f"Error deteniendo: {e}")
    
    def pausar(self):
        """Pausa la síntesis"""
        self.stop_speaking = True
        return True
    
    def reanudar(self):
        """Reanuda la síntesis"""
        self.stop_speaking = False
        return True
    
    def probar_voz(self, texto_prueba=None):
        """Prueba la configuración actual"""
        if not texto_prueba:
            texto_prueba = "Hola, esta es una prueba de voz para poesía."
        
        return self.hablar_con_config(texto_prueba)
    
    def obtener_estadisticas_voz(self):
        """Obtiene estadísticas del sistema"""
        return {
            'motor_disponible': self.engine_available,
            'total_voces': len(self.voces_disponibles),
            'voces_espanol': len(self.voces_espanol),
            'voz_actual': self.config_default.get('voz_seleccionada'),
            'estado': 'Hablando' if self.is_speaking else 'Listo',
            'plataforma': platform.system(),
            'engine_disponible': self.engine is not None
        }
    
    def recitar_con_estilo(self, texto, estilo):
        """Recita con estilo predefinido"""
        estilos = {
            'lirico_suave': {'velocidad': 120, 'volumen': 0.7, 'pausa_verso': 1.2, 'pausa_estrofa': 2.5},
            'dramatico_intenso': {'velocidad': 180, 'volumen': 0.95, 'pausa_verso': 0.6, 'pausa_estrofa': 1.8},
            'melancolico': {'velocidad': 100, 'volumen': 0.6, 'pausa_verso': 1.5, 'pausa_estrofa': 3.0},
            'epico_solemne': {'velocidad': 140, 'volumen': 0.9, 'pausa_verso': 1.0, 'pausa_estrofa': 2.0},
            'romantico_intimo': {'velocidad': 110, 'volumen': 0.75, 'pausa_verso': 1.3, 'pausa_estrofa': 2.2}
        }
        
        if estilo in estilos:
            config_estilo = {**self.config_default, **estilos[estilo]}
            return self.hablar_con_config(texto, config_estilo)
        else:
            return self.hablar_con_config(texto)


class SistemaVozBasico:
    """Sistema básico cuando pyttsx3 no funciona"""
    
    def __init__(self):
        self.is_speaking = False
        self.config_default = {'velocidad': 150, 'volumen': 0.9}
    
    def hablar_con_config(self, texto, configuracion=None):
        print(f"[AUDIO] {texto[:100]}...")
        return True
    
    def detener(self):
        self.is_speaking = False
    
    def pausar(self):
        return True
    
    def reanudar(self):
        return True
    
    def probar_voz(self, texto_prueba=None):
        return self.hablar_con_config(texto_prueba or "Prueba")
    
    def obtener_estadisticas_voz(self):
        return {
            'motor_disponible': False,
            'total_voces': 0,
            'voces_espanol': 0,
            'estado': 'Sistema básico activo',
            'plataforma': platform.system(),
            'engine_disponible': False
        }
    
    def recitar_con_estilo(self, texto, estilo):
        return self.hablar_con_config(texto)


def crear_sistema_voz():
    """Factory function para crear el sistema de voz apropiado"""
    try:
        sistema = SistemaVoz()
        if sistema.engine_available:
            logging.info("Sistema de voz principal inicializado")
            return sistema
        else:
            raise Exception("Motor principal no disponible")
    except Exception as e:
        logging.warning(f"Usando sistema de voz básico: {e}")
        return SistemaVozBasico()