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
    from .voz import SistemaVoz
    from .exportar import ExportadorPoesia
    
    __all__ = [
        'AnalizadorMetrico',
        'ContadorSilabas', 
        'DetectorRimas',
        'SistemaVoz',
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

def check_dependencies():
    """
    Verifica que todas las dependencias estén instaladas correctamente
    
    Returns:
        dict: Estado de cada dependencia
    """
    dependencies = {
        'streamlit': False,
        'pyttsx3': False,
        'reportlab': False,
        'plotly': False,
        'pandas': False,
        'requests': False
    }
    
    for package in dependencies:
        try:
            __import__(package)
            dependencies[package] = True
        except ImportError:
            dependencies[package] = False
    
    return dependencies

def setup_logging():
    """Configura el sistema de logging para el paquete"""
    import logging
    import sys
    from pathlib import Path
    
    # Crear directorio de logs si no existe
    log_dir = Path(__file__).parent.parent / 'logs'
    log_dir.mkdir(exist_ok=True)
    
    # Configurar formato
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Handler para archivo
    file_handler = logging.FileHandler(log_dir / 'utils.log')
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)
    
    # Handler para consola
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)
    
    # Configurar logger del paquete
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

def validate_installation():
    """
    Valida que la instalación del paquete sea correcta
    
    Returns:
        tuple: (is_valid, errors, warnings)
    """
    errors = []
    warnings = []
    
    # Verificar dependencias críticas
    critical_deps = check_dependencies()
    
    for dep, available in critical_deps.items():
        if not available:
            if dep in ['streamlit', 'pyttsx3']:
                errors.append(f"Dependencia crítica faltante: {dep}")
            else:
                warnings.append(f"Dependencia opcional faltante: {dep}")
    
    # Verificar archivos del paquete
    package_dir = Path(__file__).parent
    required_files = ['metrica.py', 'silabas.py', 'rimas.py', 'voz.py', 'exportar.py']
    
    for file in required_files:
        file_path = package_dir / file
        if not file_path.exists():
            errors.append(f"Archivo del paquete faltante: {file}")
    
    # Verificar imports
    try:
        from .metrica import AnalizadorMetrico
        from .silabas import ContadorSilabas
        from .rimas import DetectorRimas
    except ImportError as e:
        errors.append(f"Error importando módulos principales: {e}")
    
    try:
        from .voz import SistemaVoz
    except ImportError as e:
        warnings.append(f"Módulo de voz no disponible: {e}")
    
    try:
        from .exportar import ExportadorPoesia
    except ImportError as e:
        warnings.append(f"Módulo de exportación limitado: {e}")
    
    is_valid = len(errors) == 0
    
    return is_valid, errors, warnings

def get_system_info():
    """
    Obtiene información del sistema para diagnóstico
    
    Returns:
        dict: Información del sistema
    """
    import platform
    import sys
    
    return {
        'python_version': sys.version,
        'platform': platform.platform(),
        'architecture': platform.architecture(),
        'processor': platform.processor(),
        'package_version': __version__,
        'dependencies': check_dependencies()
    }

# Configurar logging al importar el paquete
logger = setup_logging()
logger.info(f"Paquete utils v{__version__} inicializado")

# Ejecutar validación básica
try:
    is_valid, errors, warnings_list = validate_installation()
    
    if errors:
        logger.error("Errores en la instalación:")
        for error in errors:
            logger.error(f"  - {error}")
    
    if warnings_list:
        logger.warning("Advertencias:")
        for warning in warnings_list:
            logger.warning(f"  - {warning}")
    
    if is_valid:
        logger.info("Paquete utils validado correctamente")
    else:
        logger.error("Paquete utils tiene errores de instalación")
        
except Exception as e:
    logger.error(f"Error durante la validación del paquete: {e}")

# Información sobre el paquete
package_info = {
    'name': 'Analizador Poético Utils',
    'version': __version__,
    'description': 'Utilidades especializadas para análisis métrico de poesía española',
    'modules': __all__,
    'author': __author__,
    'contact': __email__
}

def get_package_info():
    """Retorna información completa del paquete"""
    return package_info.copy()

def quick_test():
    """
    Ejecuta una prueba rápida de funcionalidad básica
    
    Returns:
        bool: True si la prueba pasa
    """
    try:
        # Test contador de sílabas
        contador = ContadorSilabas()
        silabas = contador.contar_silabas("corazón")
        assert silabas == 3, f"Error en conteo de sílabas: esperado 3, obtenido {silabas}"
        
        # Test analizador métrico
        analizador = AnalizadorMetrico()
        metro = analizador.clasificar_metro(8)
        assert "octosílabo" in metro.lower(), f"Error en clasificación métrica: {metro}"
        
        # Test detector de rimas
        detector = DetectorRimas()
        rima = detector.son_rimas_consonantes("amor", "dolor")
        assert rima == True, "Error en detección de rimas consonantes"
        
        logger.info("Prueba rápida completada exitosamente")
        return True
        
    except Exception as e:
        logger.error(f"Error en prueba rápida: {e}")
        return False

# Ejecutar prueba rápida si se ejecuta directamente
if __name__ == '__main__':
    print(f"Analizador Poético Utils v{__version__}")
    print("=" * 40)
    
    print("\n1. Información del sistema:")
    system_info = get_system_info()
    for key, value in system_info.items():
        print(f"   {key}: {value}")
    
    print("\n2. Validación de instalación:")
    is_valid, errors, warnings_list = validate_installation()
    
    if is_valid:
        print("   ✓ Instalación válida")
    else:
        print("   ✗ Errores encontrados:")
        for error in errors:
            print(f"     - {error}")
    
    if warnings_list:
        print("   Advertencias:")
        for warning in warnings_list:
            print(f"     - {warning}")
    
    print("\n3. Prueba de funcionalidad:")
    if quick_test():
        print("   ✓ Prueba rápida exitosa")
    else:
        print("   ✗ Prueba rápida falló")
    
    print("\n4. Módulos disponibles:")
    for module in __all__:
        print(f"   - {module}")
    
    print(f"\nPaquete listo para usar. Versión {__version__}")
