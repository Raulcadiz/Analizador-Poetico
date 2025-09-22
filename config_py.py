"""
Configuraciones centralizadas para Analizador Poético Pro
"""

import os
from pathlib import Path

# Información de la aplicación
APP_INFO = {
    'name': 'Analizador Poético Pro',
    'version': '1.0.0',
    'description': 'Análisis métrico avanzado de poesía española con síntesis de voz',
    'author': 'Analizador Poético Team',
    'contact': 'soporte@analizadorpoetico.com'
}

# Configuración del servidor Streamlit
SERVER_CONFIG = {
    'port': 8501,
    'host': 'localhost',
    'headless': True,
    'max_upload_size': 200,  # MB
    'theme': {
        'primaryColor': '#667eea',
        'backgroundColor': '#ffffff',
        'secondaryBackgroundColor': '#f0f2f6',
        'textColor': '#262730'
    }
}

# Directorios de la aplicación
BASE_DIR = Path(__file__).parent
UTILS_DIR = BASE_DIR / 'utils'
DATA_DIR = BASE_DIR / 'data'
EXPORTS_DIR = BASE_DIR / 'exports'
LOGS_DIR = BASE_DIR / 'logs'

# Crear directorios si no existen
for directory in [DATA_DIR, EXPORTS_DIR, LOGS_DIR]:
    directory.mkdir(exist_ok=True)

# Configuración de logging
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
        'detailed': {
            'format': '%(asctime)s [%(levelname)s] %(name)s:%(lineno)d: %(message)s'
        }
    },
    'handlers': {
        'default': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
        },
        'file': {
            'level': 'DEBUG',
            'formatter': 'detailed',
            'class': 'logging.FileHandler',
            'filename': str(LOGS_DIR / 'app.log'),
            'mode': 'a',
        }
    },
    'loggers': {
        '': {
            'handlers': ['default', 'file'],
            'level': 'DEBUG',
            'propagate': False
        }
    }
}

# Configuración de síntesis de voz
VOICE_CONFIG = {
    'default_settings': {
        'rate': 150,        # Palabras por minuto
        'volume': 0.9,      # Volumen (0.0 - 1.0)
        'voice_id': None,   # Se seleccionará automáticamente
    },
    'poetry_styles': {
        'lirico_suave': {
            'rate': 120,
            'volume': 0.7,
            'pause_verse': 1.2,
            'pause_stanza': 2.5,
            'description': 'Estilo suave y emotivo para poesía lírica'
        },
        'dramatico_intenso': {
            'rate': 180,
            'volume': 0.95,
            'pause_verse': 0.6,
            'pause_stanza': 1.8,
            'description': 'Estilo intenso para poesía dramática'
        },
        'melancolico': {
            'rate': 100,
            'volume': 0.6,
            'pause_verse': 1.5,
            'pause_stanza': 3.0,
            'description': 'Estilo pausado para poesía melancólica'
        },
        'epico_solemne': {
            'rate': 140,
            'volume': 0.9,
            'pause_verse': 1.0,
            'pause_stanza': 2.0,
            'description': 'Estilo solemne para poesía épica'
        },
        'romantico_intimo': {
            'rate': 110,
            'volume': 0.75,
            'pause_verse': 1.3,
            'pause_stanza': 2.2,
            'description': 'Estilo íntimo para poesía romántica'
        }
    },
    'voice_preferences': {
        'prefer_spanish': True,
        'prefer_female': True,  # Para poesía tradicionalmente más expresiva
        'prefer_quality': ['enhanced', 'premium', 'neural', 'hd'],
        'fallback_rate': 150
    }
}

# Configuración de análisis métrico
METRIC_ANALYSIS_CONFIG = {
    'syllable_counting': {
        'apply_sinalefa': True,
        'apply_final_accent_rule': True,
        'strict_hiatus_detection': False
    },
    'meter_classification': {
        'arte_menor_max': 8,
        'arte_mayor_min': 9,
        'common_meters': {
            4: 'Tetrasílabo',
            5: 'Pentasílabo',
            6: 'Hexasílabo', 
            7: 'Heptasílabo',
            8: 'Octosílabo',
            9: 'Eneasílabo',
            10: 'Decasílabo',
            11: 'Endecasílabo',
            12: 'Dodecasílabo',
            14: 'Alejandrino'
        }
    },
    'rhyme_detection': {
        'minimum_match_length': 2,
        'vowel_normalization': True,
        'accent_normalization': True
    }
}

# Configuración de exportación
EXPORT_CONFIG = {
    'pdf': {
        'font_family': 'Times-Roman',
        'title_font': 'Times-Bold',
        'font_size': 12,
        'title_size': 24,
        'line_spacing': 1.8,
        'margin_inches': 1.0,
        'include_metadata': True
    },
    'html': {
        'css_framework': 'custom',
        'responsive': True,
        'include_print_styles': True,
        'font_family': "'Times New Roman', serif"
    },
    'formats': {
        'pdf': {
            'name': 'PDF Elegante',
            'extension': '.pdf',
            'mime_type': 'application/pdf'
        },
        'html': {
            'name': 'HTML Estilizado', 
            'extension': '.html',
            'mime_type': 'text/html'
        },
        'txt': {
            'name': 'Texto Plano',
            'extension': '.txt',
            'mime_type': 'text/plain'
        },
        'json': {
            'name': 'JSON Estructurado',
            'extension': '.json',
            'mime_type': 'application/json'
        },
        'markdown': {
            'name': 'Markdown',
            'extension': '.md',
            'mime_type': 'text/markdown'
        }
    }
}

# Configuración de la interfaz de usuario
UI_CONFIG = {
    'page_title': 'Analizador Poético Pro',
    'page_icon': '🎭',
    'layout': 'wide',
    'sidebar_state': 'expanded',
    'max_textarea_height': 400,
    'default_examples': [
        {
            'title': 'Romance de Góngora',
            'content': '''Que por mayo era, por mayo,
cuando hace la calor,
cuando los trigos encañan
y están los campos en flor,
cuando canta la calandria
y responde el ruiseñor,
cuando los enamorados
van a servir al amor.'''
        },
        {
            'title': 'Soneto de Quevedo',
            'content': '''Cerrar podrá mis ojos la postrera
sombra que me llevare el blanco día,
y podrá desatar esta alma mía
hora a su afán ansioso lisonjera;
mas no, de esotra parte, en la ribera,
dejará la memoria, en donde ardía:
nadar sabe mi llama la agua fría,
y perder el respeto a ley severa.'''
        },
        {
            'title': 'Verso libre de Lorca',
            'content': '''Verde que te quiero verde.
Verde viento. Verdes ramas.
El barco sobre la mar
y el caballo en la montaña.
Con la sombra en la cintura
ella sueña en su baranda,
verde carne, pelo verde,
con ojos de fría plata.'''
        }
    ]
}

# Configuración de base de datos local
DATABASE_CONFIG = {
    'use_sqlite': True,
    'db_file': str(DATA_DIR / 'poems.db'),
    'backup_interval_hours': 24,
    'max_poems_per_user': 1000,
    'auto_backup': True
}

# Configuración de APIs externas (opcional)
API_CONFIG = {
    'huggingface': {
        'enabled': False,
        'token': os.getenv('HUGGINGFACE_TOKEN'),
        'models': {
            'text_generation': 'gpt2',
            'sentiment_analysis': 'cardiffnlp/twitter-roberta-base-sentiment-latest'
        },
        'timeout': 30,
        'max_retries': 3
    },
    'openai': {
        'enabled': False,
        'api_key': os.getenv('OPENAI_API_KEY'),
        'model': 'gpt-3.5-turbo',
        'max_tokens': 500
    }
}

# Configuración de métricas y analytics
ANALYTICS_CONFIG = {
    'track_usage': False,  # Solo métricas locales
    'save_analysis_history': True,
    'max_history_entries': 500,
    'export_analytics': True
}

# Configuración de seguridad
SECURITY_CONFIG = {
    'max_file_size_mb': 10,
    'allowed_file_types': ['.txt', '.md', '.json'],
    'rate_limiting': {
        'max_requests_per_minute': 60,
        'max_text_length': 50000  # caracteres
    },
    'sanitize_input': True
}

# Configuración de rendimiento
PERFORMANCE_CONFIG = {
    'cache_enabled': True,
    'cache_ttl_seconds': 3600,
    'max_concurrent_voice_synthesis': 1,
    'chunk_large_texts': True,
    'chunk_size_chars': 10000
}

# Mensajes del sistema
SYSTEM_MESSAGES = {
    'welcome': '''¡Bienvenido al Analizador Poético Pro! 
    
Esta herramienta te permite analizar métricamente poesía en español, 
con síntesis de voz especializada y exportación profesional.
    
Comienza escribiendo o pegando un poema en el área de texto.''',
    
    'no_text': 'Por favor, introduce algún texto para analizar.',
    'analysis_complete': 'Análisis completado exitosamente.',
    'voice_not_available': 'Síntesis de voz no disponible en este sistema.',
    'export_success': 'Archivo exportado correctamente.',
    'save_success': 'Poema guardado en tu colección.',
    
    'errors': {
        'analysis_failed': 'Error en el análisis. Verifica que el texto sea válido.',
        'voice_failed': 'Error en síntesis de voz. Revisa la configuración.',
        'export_failed': 'Error al exportar. Inténtalo con otro formato.',
        'save_failed': 'Error al guardar. Verifica que tienes espacio disponible.'
    }
}

# Configuración de desarrollo/debug
DEBUG_CONFIG = {
    'enabled': os.getenv('DEBUG', 'False').lower() == 'true',
    'show_raw_data': False,
    'log_level': 'DEBUG' if os.getenv('DEBUG') else 'INFO',
    'profiling': False,
    'mock_voice_synthesis': False  # Para testing sin audio
}

def get_config(section=None):
    """
    Obtiene configuración específica o completa
    
    Args:
        section (str, optional): Sección específica a obtener
        
    Returns:
        dict: Configuración solicitada
    """
    if section:
        return globals().get(f'{section.upper()}_CONFIG', {})
    
    return {
        'app': APP_INFO,
        'server': SERVER_CONFIG,
        'voice': VOICE_CONFIG,
        'metrics': METRIC_ANALYSIS_CONFIG,
        'export': EXPORT_CONFIG,
        'ui': UI_CONFIG,
        'database': DATABASE_CONFIG,
        'api': API_CONFIG,
        'analytics': ANALYTICS_CONFIG,
        'security': SECURITY_CONFIG,
        'performance': PERFORMANCE_CONFIG,
        'messages': SYSTEM_MESSAGES,
        'debug': DEBUG_CONFIG
    }

def update_config(section, key, value):
    """
    Actualiza un valor específico de configuración
    
    Args:
        section (str): Sección de configuración
        key (str): Clave a actualizar
        value: Nuevo valor
    """
    config_dict = globals().get(f'{section.upper()}_CONFIG')
    if config_dict and key in config_dict:
        config_dict[key] = value
        return True
    return False

def validate_config():
    """
    Valida que la configuración sea correcta
    
    Returns:
        tuple: (es_valida, errores)
    """
    errors = []
    
    # Validar directorios
    for directory in [DATA_DIR, EXPORTS_DIR, LOGS_DIR]:
        if not directory.exists():
            try:
                directory.mkdir(exist_ok=True)
            except Exception as e:
                errors.append(f"No se pudo crear directorio {directory}: {e}")
    
    # Validar configuración de voz
    if VOICE_CONFIG['default_settings']['rate'] < 50 or VOICE_CONFIG['default_settings']['rate'] > 400:
        errors.append("Velocidad de voz fuera de rango válido (50-400)")
    
    if VOICE_CONFIG['default_settings']['volume'] < 0 or VOICE_CONFIG['default_settings']['volume'] > 1:
        errors.append("Volumen de voz fuera de rango válido (0.0-1.0)")
    
    # Validar puertos
    if SERVER_CONFIG['port'] < 1024 or SERVER_CONFIG['port'] > 65535:
        errors.append("Puerto fuera de rango válido (1024-65535)")
    
    return len(errors) == 0, errors

# Ejecutar validación al importar
if __name__ == '__main__':
    is_valid, validation_errors = validate_config()
    if not is_valid:
        print("Errores de configuración encontrados:")
        for error in validation_errors:
            print(f"  - {error}")
    else:
        print("Configuración válida ✓")