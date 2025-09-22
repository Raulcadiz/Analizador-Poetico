"""
Paquete de utilidades para Analizador Poético Pro

Este paquete contiene todas las herramientas especializadas para el análisis
métrico de poesía en español, síntesis de voz y exportación de documentos.

Módulos:
- metrica: Análisis métrico avanzado (sílabas, metros, ritmo)
- silabas: Contador especializado de sílabas con reglas métricas
- rimas: Detector de rimas consonantes y asonantes
- voz: Sistema de síntesis de voz optimizado para poesía
- exportar: Exportación a múltiples formatos (PDF, HTML, JSON, etc.)
"""

__version__ = '1.0.0'
__author__ = 'Analizador Poético Team'
__email__ = 'soporte@analizadorpoetico.com'

# Importaciones principales para facilitar el uso del paquete
try:
    from .metrica import AnalizadorMetrico
    from .silabas import ContadorSilabas
    from .rimas import DetectorRimas
    from .voz import SistemaVoz, crear_sistema_voz
    from .exportar import ExportadorPoesia
    
    __all__ = [
        'AnalizadorMetrico',
        'ContadorSilabas', 
        'DetectorRimas',
        'SistemaVoz',
        'crear_sistema_voz',
        'ExportadorPoesia'
    ]
    
except ImportError as e:
    # En caso de que falten dependencias, importar solo lo disponible
    import warnings
    warnings.warn(f"Algunas utilidades no están disponibles: {e}")
    __all__ = []

def get_version():
    """Retorna la versión del paquete"""
    return __version__