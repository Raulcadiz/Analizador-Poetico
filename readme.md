# 🎭 Analizador Poético Pro

Una aplicación completa para el análisis métrico de poesía española con síntesis de voz especializada y exportación profesional.

## ✨ Características Principales

- **📊 Análisis Métrico Avanzado**: Cuenta sílabas, detecta metros, analiza ritmo
- **🎼 Detección de Rimas**: Identifica esquemas consonantes y asonantes
- **🔊 Síntesis de Voz Poética**: Lectura expresiva con pausas optimizadas
- **📈 Visualizaciones**: Gráficos interactivos de métricas poéticas
- **💾 Gestión de Poemas**: Guarda y organiza tu colección personal
- **📄 Exportación Múltiple**: PDF, HTML, TXT, JSON, Markdown
- **🎨 Estilos de Recitado**: Presets para diferentes tipos de poesía
- **📚 Ejemplos Incluidos**: Romances, sonetos, verso libre

## 🔧 Instalación

### Requisitos del Sistema
- Windows 10 o superior
- Python 3.8+ (se instalará automáticamente si no está presente)
- 4GB RAM mínimo
- 1GB espacio en disco

### Instalación Automática (Recomendada)

1. **Descargar archivos**:
   - Descarga todos los archivos en una carpeta llamada `analizador-poetico`
   - Mantén la estructura de carpetas tal como se proporciona

2. **Ejecutar instalación**:
   ```batch
   # Doble clic en run.bat
   # O desde línea de comandos:
   run.bat
   ```

3. **Primera ejecución**:
   - El script instalará automáticamente Python si no está presente
   - Instalará todas las dependencias necesarias
   - Abrirá la aplicación en tu navegador

### Instalación Manual

1. **Instalar Python**:
   ```bash
   # Descargar desde https://python.org
   # Asegurarse de marcar "Add to PATH"
   ```

2. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Ejecutar aplicación**:
   ```bash
   streamlit run app.py --server.port 8501
   ```

## 🚀 Uso Rápido

### Inicio Básico
1. Ejecuta `run.bat`
2. Se abrirá automáticamente en `http://localhost:8501`
3. Escribe o pega tu poema en el área de texto
4. Haz clic en "📈 Analizar" para obtener métricas completas

### Análisis de Poesía
```
Ejemplo de uso:
1. Pega este verso en la aplicación:

Verde que te quiero verde,
verde viento, verdes ramas.
El barco sobre la mar
y el caballo en la montaña.

2. Obtendrás:
   - Análisis silábico: 8-8-8-8 (octosílabos)
   - Esquema de rimas: ABCB (asonante)
   - Estilo detectado: Verso libre
   - Sugerencias de recitado
```

### Síntesis de Voz
1. Ve a la pestaña "🔊 Control de Voz"
2. Ajusta velocidad, pausas y estilo
3. Haz clic en "🔊 Recitar Poema"
4. Usa presets como "Lírico Suave" o "Dramático Intenso"

## 📁 Estructura del Proyecto

```
analizador-poetico/
├── app.py                    # Aplicación principal
├── requirements.txt          # Dependencias Python
├── run.bat                  # Ejecutor para Windows
├── config.py                # Configuraciones
├── README.md               # Esta guía
└── utils/
    ├── __init__.py
    ├── metrica.py          # Análisis métrico
    ├── silabas.py          # Contador de sílabas
    ├── rimas.py            # Detector de rimas
    ├── voz.py              # Sistema de síntesis de voz
    └── exportar.py         # Exportación de documentos
```

## 🎛️ Configuración Avanzada

### Configuración de Voz
```python
# Estilos predefinidos disponibles:
estilos = {
    'lirico_suave': {
        'velocidad': 120,
        'volumen': 0.7,
        'pausa_verso': 1.2,
        'pausa_estrofa': 2.5
    },
    'dramatico_intenso': {
        'velocidad': 180,
        'volumen': 0.95,
        'pausa_verso': 0.6,
        'pausa_estrofa': 1.8
    }
    # ... más estilos
}
```

### Puertos de Red
- **Puerto por defecto**: 8501
- **Cambiar puerto**: Edita `config.py` o usa `--server.port XXXX`
- **Acceso remoto**: Usa `--server.address 0.0.0.0` (¡Cuidado con la seguridad!)

### Configuración de Firewall Windows
```batch
# Abrir puerto 8501 (ejecutar como administrador):
netsh advfirewall firewall add rule name="Analizador Poetico" dir=in action=allow protocol=TCP localport=8501
```

## 📊 Funcionalidades Detalladas

### Análisis Métrico
- **Conteo silábico**: Aplica reglas de sinalefa y acentuación final
- **Clasificación métrica**: Identifica metros clásicos (octosílabo, endecasílabo, etc.)
- **Análisis rítmico**: Detecta patrones acentuales y regularidad
- **Estilo poético**: Clasifica automáticamente (romance, soneto, verso libre)

### Detección de Rimas
- **Rimas consonantes**: Coincidencia completa desde la vocal tónica
- **Rimas asonantes**: Coincidencia solo de vocales
- **Esquemas clásicos**: ABAB, ABBA, AABB, etc.
- **Calidad de rima**: Evalúa riqueza y corrección

### Síntesis de Voz
- **Voces del sistema**: Utiliza voces instaladas en Windows
- **Optimización poética**: Pausas especiales entre versos y estrofas
- **Control granular**: Velocidad, volumen, tono, pausas
- **Estilos preconfigurados**: Para diferentes tipos de poesía

### Exportación
- **PDF elegante**: Formato profesional con tipografía poética
- **HTML responsive**: Página web con estilos CSS
- **JSON estructurado**: Datos completos para intercambio
- **Análisis CSV**: Para estudios estadísticos
- **Antologías**: Compilaciones multipoemasn PDF

## 🔧 Solución de Problemas

### Problemas Comunes

**❌ Error: "streamlit not found"**
```bash
# Solución:
pip install streamlit
# O reinstalar dependencias:
pip install -r requirements.txt --force-reinstall
```

**❌ Error de síntesis de voz**
```bash
# Verificar voces disponibles:
# La aplicación mostrará voces detectadas en la pestaña de configuración
# Si no hay voces españolas, instalar paquete de idioma en Windows
```

**❌ Puerto 8501 ocupado**
```bash
# Usar puerto alternativo:
streamlit run app.py --server.port 8502
# O editar config.py
```

**❌ Error de permisos en Windows**
```bash
# Ejecutar como administrador o cambiar ubicación de instalación
# Evitar carpetas del sistema como Program Files
```

### Logs y Diagnóstico
```bash
# Ver logs detallados:
streamlit run app.py --logger.level debug

# Verificar instalación:
python -c "import streamlit, pyttsx3, reportlab; print('Todo OK')"
```

## 🎯 Casos de Uso

### Para Estudiantes
- Análisis de métrica para clases de literatura
- Práctica de escansión y rimas
- Comprensión de formas poéticas clásicas

### Para Poetas
- Verificación de metros y rimas
- Experimentación con diferentes estilos
- Archivo organizado de obra personal

### Para Profesores
- Herramienta didáctica para enseñar métrica
- Ejemplos visuales de análisis poético
- Exportación de materiales de clase

### Para Investigadores
- Análisis estadístico de corpus poéticos
- Exportación de datos para estudios métricos
- Comparación entre diferentes estilos

## 🤝 Contribuir

### Reportar Errores
1. Ir a la sección de Issues
2. Describir el problema con detalles
3. Incluir mensaje de error completo
4. Especificar sistema operativo y versión Python

### Sugerir Mejoras
- Nuevas funcionalidades de análisis
- Mejoras en la síntesis de voz
- Formatos de exportación adicionales
- Optimizaciones de rendimiento

## 📋 Limitaciones Conocidas

- **Solo español**: Optimizado específicamente para métrica española
- **Síntesis básica**: Depende de voces del sistema operativo
- **Análisis automático**: Puede requerir revisión manual en casos complejos
- **Recursos**: Uso intensivo de CPU durante síntesis de voz larga

## 🔄 Actualizaciones

### Versión 1.0.0 (Actual)
- ✅ Análisis métrico completo
- ✅ Síntesis de voz especializada
- ✅ Exportación múltiple
- ✅ Gestión de colecciones
- ✅ Interface web moderna

### Próximas Versiones
- 🔮 Integración con APIs de IA
- 🔮 Análisis de estilo poético avanzado
- 🔮 Reconocimiento de voz para dictado
- 🔮 Base de datos de poesía clásica
- 🔮 Análisis comparativo entre autores

## 📞 Soporte

### Documentación
- **Wiki completa**: Consulta la documentación expandida
- **Ejemplos**: Casos de uso paso a paso
- **FAQ**: Preguntas frecuentes

### Comunidad
- **Foro**: Discusiones sobre poesía y métrica
- **Discord**: Chat en tiempo real
- **YouTube**: Tutoriales en video

### Contacto Directo
- **Email**: soporte@analizadorpoetico.com
- **Issues**: GitHub Issues para reportes técnicos
- **Feedback**: Formulario de sugerencias integrado

## 📄 Licencia

MIT License - Libre para uso personal, educativo y comercial.

Ver `LICENSE` para detalles completos.

## 🙏 Agradecimientos

- **Comunidad Streamlit**: Por la excelente framework
- **Desarrolladores pyttsx3**: Por la síntesis de voz
- **ReportLab**: Por generación de PDFs
- **Métrica española clásica**: Basado en tratados de Tomás Navarro Tomás
- **Beta testers**: Profesores y estudiantes de literatura

---

**🎭 Analizador Poético Pro** - *Donde la tecnología encuentra la poesía*

*Hecho con ❤️ para la comunidad hispanohablante*