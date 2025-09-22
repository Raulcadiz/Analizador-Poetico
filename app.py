import streamlit as st
import threading
import time
import json
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
from utils.metrica import AnalizadorMetrico
from utils.silabas import ContadorSilabas
from utils.rimas import DetectorRimas
from utils.voz import crear_sistema_voz  # Usar el sistema original por ahora
from utils.exportar import ExportadorPoesia
import requests

# Configuración de la página
st.set_page_config(
    page_title="Analizador Poético Pro",
    page_icon="🎭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado mejorado - CORREGIDO
def cargar_css_mejorado():
    return """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Crimson+Text:ital,wght@0,400;0,600;1,400&display=swap');
    
    .main-header {
        background: linear-gradient(135deg, rgb(102, 126, 234) 0%, rgb(118, 75, 162) 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
    }
    
    .main-header h1 {
        font-family: 'Crimson Text', serif;
        font-size: 3rem;
        margin-bottom: 0.5rem;
    }
    
    /* Estilos mejorados para textarea con colores dinámicos */
    .stTextArea textarea {
        font-family: 'Crimson Text', serif !important;
        font-size: 16px !important;
        line-height: 1.8 !important;
        transition: all 0.3s ease !important;
        border-radius: 8px !important;
    }
    
    /* Colores por número de sílabas */
    .silabas-8 {
        background-color: rgb(232, 245, 232) !important;
        border: 2px solid rgb(76, 175, 80) !important;
        color: rgb(46, 125, 50) !important;
    }
    
    .silabas-11 {
        background-color: rgb(255, 243, 224) !important;
        border: 2px solid rgb(255, 152, 0) !important;
        color: rgb(230, 81, 0) !important;
    }
    
    .silabas-14 {
        background-color: rgb(255, 253, 231) !important;
        border: 2px solid rgb(255, 235, 59) !important;
        color: rgb(245, 127, 23) !important;
    }
    
    .silabas-exceso {
        background-color: rgb(255, 235, 238) !important;
        border: 2px solid rgb(244, 67, 54) !important;
        color: rgb(198, 40, 40) !important;
    }
    
    .silabas-normal {
        background-color: rgb(250, 250, 250) !important;
        border: 2px solid rgb(224, 224, 224) !important;
        color: rgb(51, 51, 51) !important;
    }
    
    .metric-card {
        background: linear-gradient(145deg, rgb(248, 249, 250), rgb(233, 236, 239));
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid rgb(102, 126, 234);
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        transition: transform 0.2s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
    }
    
    .verse-analysis {
        background: rgb(255, 255, 255);
        padding: 1.5rem;
        border-radius: 12px;
        border: 2px solid rgb(224, 224, 224);
        margin: 1rem 0;
        font-family: 'Crimson Text', serif;
        line-height: 1.8;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    
    .rhyme-pattern {
        font-family: 'Courier New', monospace;
        background: rgb(240, 240, 240);
        padding: 1rem;
        border-radius: 8px;
        display: inline-block;
        font-weight: bold;
        border-left: 4px solid rgb(118, 75, 162);
    }
    
    /* Indicador de sílabas en tiempo real */
    .silabas-indicator {
        background: linear-gradient(45deg, rgb(102, 126, 234), rgb(118, 75, 162));
        color: white;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 14px;
        margin: 10px 0;
        display: inline-block;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
        animation: pulse 2s ease-in-out infinite alternate;
    }
    
    @keyframes pulse {
        from { box-shadow: 0 2px 8px rgba(0,0,0,0.2); }
        to { box-shadow: 0 4px 16px rgba(0,0,0,0.4); }
    }
    
    .voice-status-card {
        background: rgb(227, 242, 253);
        border: 2px solid rgb(33, 150, 243);
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .voice-error-card {
        background: rgb(255, 235, 238);
        border: 2px solid rgb(244, 67, 54);
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .voice-success-card {
        background: rgb(232, 245, 232);
        border: 2px solid rgb(76, 175, 80);
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
"""

class AppPoetryAnalyzer:
    def __init__(self):
        self.inicializar_componentes()
        self.cargar_datos_sesion()
    
    def inicializar_componentes(self):
        """Inicializa todos los componentes de análisis"""
        if 'analizador' not in st.session_state:
            st.session_state.analizador = AnalizadorMetrico()
            st.session_state.contador = ContadorSilabas()
            st.session_state.detector_rimas = DetectorRimas()
            st.session_state.sistema_voz = crear_sistema_voz()
            st.session_state.exportador = ExportadorPoesia()
            st.session_state.historial_analisis = []
    
    def cargar_datos_sesion(self):
        """Carga datos persistentes de la sesión"""
        if 'poemas_guardados' not in st.session_state:
            st.session_state.poemas_guardados = {}
        if 'configuracion_voz' not in st.session_state:
            st.session_state.configuracion_voz = {
                'velocidad': 150,
                'volumen': 0.9,
                'pausa_verso': 0.8,
                'pausa_estrofa': 1.5,
                'voz_seleccionada': None
            }
        if 'texto_ejemplo_cargado' not in st.session_state:
            st.session_state.texto_ejemplo_cargado = ""
        if 'cargar_ejemplo' not in st.session_state:
            st.session_state.cargar_ejemplo = False

def mostrar_indicador_silabas(app, texto_actual):
    """Muestra indicador de sílabas en tiempo real"""
    if not texto_actual.strip():
        return
    
    # Obtener la línea actual (última línea no vacía)
    lineas = texto_actual.split('\n')
    linea_actual = ""
    
    for linea in reversed(lineas):
        if linea.strip():
            linea_actual = linea.strip()
            break
    
    if not linea_actual:
        return
    
    # Contar sílabas de la línea actual
    try:
        silabas = st.session_state.contador.contar_silabas_verso(linea_actual)
        
        # Determinar color y mensaje
        color = "#6c757d"
        emoji = "📝"
        mensaje = f"{silabas} sílabas"
        tipo_verso = ""
        
        if silabas == 8:
            color = "#28a745"
            emoji = "✅"
            tipo_verso = "(Octosílabo)"
        elif silabas == 11:
            color = "#fd7e14"
            emoji = "🔥"
            tipo_verso = "(Endecasílabo)"
        elif silabas == 14:
            color = "#ffc107"
            emoji = "⭐"
            tipo_verso = "(Alejandrino)"
        elif silabas > 14:
            color = "#dc3545"
            emoji = "⚠️"
            tipo_verso = "(Exceso)"
        
        # Mostrar indicador
        st.markdown(f"""
        <div style="background: {color}; color: white; padding: 8px 16px; 
                    border-radius: 20px; display: inline-block; margin: 5px 0;
                    font-weight: bold; font-size: 14px; box-shadow: 0 2px 8px rgba(0,0,0,0.2);">
            {emoji} {mensaje} {tipo_verso}
        </div>
        """, unsafe_allow_html=True)
        
        # Mostrar división silábica si es interesante
        if silabas in [8, 11, 14]:
            try:
                palabras = linea_actual.split()
                if len(palabras) <= 3:  # Solo para líneas cortas
                    division_palabras = []
                    for palabra in palabras:
                        div = st.session_state.contador.dividir_en_silabas(palabra)
                        division_palabras.append(' - '.join(div))
                    
                    st.markdown(f"""
                    <small style="color: #6c757d; font-style: italic;">
                        División: {' | '.join(division_palabras)}
                    </small>
                    """, unsafe_allow_html=True)
            except:
                pass
                
    except Exception as e:
        st.error(f"Error analizando sílabas: {e}")

def main():
    app = AppPoetryAnalyzer()
    
    # Cargar CSS mejorado
    st.markdown(cargar_css_mejorado(), unsafe_allow_html=True)
    
    # Header principal mejorado
    st.markdown("""
    <div class="main-header">
        <h1>🎭 Analizador Poético Pro</h1>
        <p style="font-size: 1.2rem; margin-bottom: 0;">
            Análisis métrico avanzado • Síntesis de voz especializada • Exportación profesional
        </p>
        <p style="font-size: 0.9rem; opacity: 0.8;">
            Herramienta completa para el análisis de poesía en español
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Mostrar estado del sistema de voz
    mostrar_estado_voz()
    
    # Configuración de pestañas principales
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📝 Análisis Principal", 
        "🔊 Control de Voz", 
        "📊 Estadísticas", 
        "💾 Mis Poemas", 
        "⚙️ Configuración"
    ])
    
    with tab1:
        mostrar_analisis_principal(app)
    
    with tab2:
        mostrar_control_voz(app)
    
    with tab3:
        mostrar_estadisticas(app)
    
    with tab4:
        mostrar_mis_poemas(app)
    
    with tab5:
        mostrar_configuracion(app)

def mostrar_estado_voz():
    """Muestra el estado actual del sistema de voz"""
    try:
        stats = st.session_state.sistema_voz.obtener_estadisticas_voz()
        
        if stats['motor_disponible']:
            st.markdown(f"""
            <div class="voice-success-card">
                ✅ <strong>Sistema de Voz Activo</strong><br>
                🗣️ {stats['voces_espanol']} voces en español disponibles | 
                🎵 Estado: {stats['estado']} | 
                💻 Plataforma: {stats['plataforma']}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="voice-status-card">
                ℹ️ <strong>Sistema de Voz en Modo Básico</strong><br>
                Sistema fallback activo - Funcionalidad limitada pero operativa
            </div>
            """, unsafe_allow_html=True)
            
    except Exception as e:
        st.markdown(f"""
        <div class="voice-error-card">
            ⚠️ <strong>Error en Sistema de Voz</strong><br>
            {str(e)[:100]}... | Algunas funciones pueden estar limitadas
        </div>
        """, unsafe_allow_html=True)

def mostrar_analisis_principal(app):
    """Pestaña principal de análisis"""
    col1, col2 = st.columns([2, 1])
    
    with col2:
        st.subheader("📚 Ejemplos y Plantillas")
        
        ejemplos_poesia = {
            "Romance de Góngora": """Que por mayo era, por mayo,
cuando hace la calor,
cuando los trigos encañan
y están los campos en flor,
cuando canta la calandria
y responde el ruiseñor,
cuando los enamorados
van a servir al amor.""",
            
            "Soneto de Quevedo": """Cerrar podrá mis ojos la postrera
sombra que me llevare el blanco día,
y podrá desatar esta alma mía
hora a su afán ansioso lisonjera;
mas no, de esotra parte, en la ribera,
dejará la memoria, en donde ardía:
nadar sabe mi llama la agua fría,
y perder el respeto a ley severa.""",
            
            "Verso libre de Lorca": """Verde que te quiero verde.
Verde viento. Verdes ramas.
El barco sobre la mar
y el caballo en la montaña.
Con la sombra en la cintura
ella sueña en su baranda,
verde carne, pelo verde,
con ojos de fría plata.""",
            
            "Redondilla clásica": """En tanto que de rosa y azucena
se muestra la color en vuestro gesto,
y que vuestro mirar ardiente, honesto,
enciende al corazón y lo refrena;
y en tanto que el cabello, que en la vena
del oro se escogió, con vuelo presto,
por el hermoso cuello blanco, enhiesto,
el viento mueve, esparce y desordena."""
        }
        
        ejemplo_seleccionado = st.selectbox(
            "Selecciona un ejemplo:",
            ["Seleccionar..."] + list(ejemplos_poesia.keys())
        )
        
        if ejemplo_seleccionado != "Seleccionar...":
            with st.expander(f"Vista previa: {ejemplo_seleccionado}"):
                st.markdown(f"""
                <div style="background: #fff; border: 2px solid #eee; border-radius: 10px; padding: 1rem; margin: 0.5rem 0;">
                    <pre style="white-space: pre-wrap; font-family: 'Crimson Text', serif; line-height: 1.6;">
{ejemplos_poesia[ejemplo_seleccionado]}
                    </pre>
                </div>
                """, unsafe_allow_html=True)
            
            if st.button(f"📋 Usar {ejemplo_seleccionado}", use_container_width=True):
                st.session_state.texto_ejemplo_cargado = ejemplos_poesia[ejemplo_seleccionado]
                st.session_state.cargar_ejemplo = True
                st.rerun()
        
        # Tips de análisis
        with st.expander("💡 Tips de Análisis"):
            st.markdown("""
            **Para mejores resultados:**
            - Asegúrate de que cada verso esté en una línea separada
            - Separa las estrofas con líneas en blanco
            - Incluye todos los signos de puntuación
            - Para análisis de ritmo, escribe al menos 4 versos
            
            **Colores del editor:**
            - 🟢 Verde: 8 sílabas (Octosílabo)
            - 🟠 Naranja: 11 sílabas (Endecasílabo)
            - 🟡 Amarillo: 14 sílabas (Alejandrino)
            - 🔴 Rojo: Más de 14 sílabas
            """)
    
    with col1:
        st.subheader("✏️ Tu Poesía")
        
        # Manejar carga de ejemplo
        texto_inicial = ""
        if st.session_state.cargar_ejemplo:
            texto_inicial = st.session_state.texto_ejemplo_cargado
            st.session_state.cargar_ejemplo = False
        
        # Área de texto mejorada
        texto_poesia = st.text_area(
            "Introduce tu poema aquí:",
            value=texto_inicial,
            height=350,
            placeholder="""Verde que te quiero verde.
Verde viento. Verdes ramas.
El barco sobre la mar
y el caballo en la montaña.
Con la sombra en la cintura
ella sueña en su baranda,
verde carne, pelo verde,
con ojos de fría plata...""",
            help="Escribe o pega tu poema. El analizador detectará automáticamente el metro.",
            key="textarea_poesia"
        )
        
        # Mostrar indicador de sílabas en tiempo real
        if texto_poesia.strip():
            mostrar_indicador_silabas(app, texto_poesia)
        
        # Botones de acción principales
        col_btn1, col_btn2, col_btn3, col_btn4 = st.columns(4)
        
        with col_btn1:
            if st.button("🔊 Recitar", type="primary", use_container_width=True):
                if texto_poesia.strip():
                    recitar_poema_seguro(app, texto_poesia)
                else:
                    st.warning("Escribe un poema primero")
        
        with col_btn2:
            if st.button("📈 Analizar", use_container_width=True):
                if texto_poesia.strip():
                    realizar_analisis_completo(app, texto_poesia)
        
        with col_btn3:
            if st.button("💾 Guardar", use_container_width=True):
                if texto_poesia.strip():
                    guardar_poema(app, texto_poesia)
        
        with col_btn4:
            if st.button("📄 Exportar", use_container_width=True):
                if texto_poesia.strip():
                    exportar_poema(app, texto_poesia)
    
    # Mostrar análisis si hay texto
    if texto_poesia and texto_poesia.strip():
        mostrar_resultados_analisis(app, texto_poesia)

def mostrar_control_voz(app):
    """Pestaña de control de voz avanzado"""
    st.header("🔊 Control Avanzado de Voz")
    
    # Estado detallado del sistema de voz
    try:
        stats = st.session_state.sistema_voz.obtener_estadisticas_voz()
        
        st.subheader("📊 Estado del Sistema de Voz")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Motor", "✅ Activo" if stats['motor_disponible'] else "⚠️ Básico")
        with col2:
            st.metric("Voces Total", stats['total_voces'])
        with col3:
            st.metric("Voces Español", stats['voces_espanol'])
        with col4:
            st.metric("Estado", stats['estado'])
        
        if not stats.get('engine_disponible', True):
            st.info("🔧 Usando sistema de voz básico. Instala pyttsx3 para funcionalidad completa.")
            
    except Exception as e:
        st.error(f"Error obteniendo estadísticas de voz: {e}")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("🎛️ Configuración de Voz")
        
        # Control de velocidad
        velocidad = st.slider(
            "Velocidad de lectura (palabras por minuto)",
            min_value=80,
            max_value=300,
            value=st.session_state.configuracion_voz['velocidad'],
            help="Velocidades recomendadas: Lírica (80-120), Normal (150), Dramática (200+)"
        )
        
        # Control de volumen
        volumen = st.slider(
            "Volumen",
            min_value=0.1,
            max_value=1.0,
            value=st.session_state.configuracion_voz['volumen'],
            step=0.1
        )
        
        # Pausas personalizadas
        pausa_verso = st.slider(
            "Pausa entre versos (segundos)",
            min_value=0.1,
            max_value=3.0,
            value=st.session_state.configuracion_voz['pausa_verso'],
            step=0.1
        )
        
        pausa_estrofa = st.slider(
            "Pausa entre estrofas (segundos)",
            min_value=0.5,
            max_value=5.0,
            value=st.session_state.configuracion_voz['pausa_estrofa'],
            step=0.1
        )
        
        # Guardar configuración
        if st.button("💾 Guardar Configuración"):
            st.session_state.configuracion_voz.update({
                'velocidad': velocidad,
                'volumen': volumen,
                'pausa_verso': pausa_verso,
                'pausa_estrofa': pausa_estrofa
            })
            st.success("Configuración guardada")
    
    with col2:
        st.subheader("🎭 Estilos de Recitado")
        
        estilo_preset = st.selectbox(
            "Presets de estilo:",
            [
                "Personalizado",
                "Lírico Suave",
                "Dramático Intenso", 
                "Melancólico",
                "Épico Solemne",
                "Romántico Íntimo"
            ]
        )
        
        presets = {
            "Lírico Suave": {'velocidad': 120, 'volumen': 0.7, 'pausa_verso': 1.2, 'pausa_estrofa': 2.5},
            "Dramático Intenso": {'velocidad': 180, 'volumen': 0.95, 'pausa_verso': 0.6, 'pausa_estrofa': 1.8},
            "Melancólico": {'velocidad': 100, 'volumen': 0.6, 'pausa_verso': 1.5, 'pausa_estrofa': 3.0},
            "Épico Solemne": {'velocidad': 140, 'volumen': 0.9, 'pausa_verso': 1.0, 'pausa_estrofa': 2.0},
            "Romántico Íntimo": {'velocidad': 110, 'volumen': 0.75, 'pausa_verso': 1.3, 'pausa_estrofa': 2.2}
        }
        
        if estilo_preset != "Personalizado" and st.button(f"Aplicar {estilo_preset}"):
            preset = presets[estilo_preset]
            st.session_state.configuracion_voz.update(preset)
            st.success(f"Estilo {estilo_preset} aplicado")
            st.rerun()
        
        # Test de voz mejorado
        st.subheader("🎤 Prueba de Voz")
        texto_prueba = st.text_area(
            "Texto de prueba:",
            value="Verde que te quiero verde,\nverde viento, verdes ramas.",
            height=100
        )
        
        col_test1, col_test2 = st.columns(2)
        
        with col_test1:
            if st.button("🔊 Probar Configuración"):
                if texto_prueba.strip():
                    probar_voz_segura(texto_prueba)
        
        with col_test2:
            if st.button("⏹️ Detener Voz"):
                detener_voz_segura()

def mostrar_resultados_analisis(app, texto):
    """Muestra los resultados del análisis poético"""
    st.markdown('<div style="background: white; padding: 2rem; border-radius: 15px; box-shadow: 0 5px 20px rgba(0,0,0,0.1); margin: 1rem 0;">', unsafe_allow_html=True)
    st.header("📊 Análisis Poético Completo")
    
    try:
        # Realizar análisis
        resultado = st.session_state.analizador.analisis_completo(texto)
        
        if "error" in resultado:
            st.error(resultado["error"])
            return
        
        # Métricas principales
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric("Versos", resultado['estadisticas']['total_versos'])
        with col2:
            st.metric("Sílabas totales", resultado['estadisticas']['total_silabas'])
        with col3:
            st.metric("Promedio sílabas", f"{resultado['estadisticas']['promedio_silabas']:.1f}")
        with col4:
            palabras_total = sum(len(v['texto'].split()) for v in resultado['versos_analizados'])
            st.metric("Palabras", palabras_total)
        with col5:
            estrofas = len([e for e in texto.split('\n\n') if e.strip()])
            st.metric("Estrofas", estrofas)
        
        # Análisis detallado por secciones
        col_left, col_right = st.columns(2)
        
        with col_left:
            # Análisis métrico por verso
            st.subheader("🎵 Análisis Métrico Detallado")
            
            for verso_data in resultado['versos_analizados']:
                with st.expander(f"Verso {verso_data['numero']}: {verso_data['silabas']} sílabas"):
                    st.markdown(f"""
                    <div class="verse-analysis">
                        <p><strong>Texto:</strong> "{verso_data['texto']}"</p>
                        <p><strong>Sílabas:</strong> {verso_data['silabas']}</p>
                        <p><strong>Metro:</strong> {verso_data['metro']}</p>
                        <p><strong>Acentos:</strong> {', '.join(map(str, verso_data['acentos'])) if verso_data['acentos'] else 'No detectados'}</p>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Análisis de rimas
            st.subheader("🎼 Análisis de Rimas")
            versos = [v.strip() for v in texto.split('\n') if v.strip()]
            esquema_rimas = st.session_state.detector_rimas.detectar_esquema(versos)
            tipo_rima = st.session_state.detector_rimas.clasificar_rima(esquema_rimas)
            
            st.markdown(f"""
            <div class="metric-card">
                <h4>Esquema de Rimas: {tipo_rima}</h4>
                <div class="rhyme-pattern">
                    Patrón: {''.join(esquema_rimas)}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Detalle de rimas
            for i, (verso, letra) in enumerate(zip(versos, esquema_rimas), 1):
                st.text(f"Verso {i} ({letra}): {verso}")
        
        with col_right:
            # Resumen métrico
            st.subheader("📝 Resumen Métrico")
            st.markdown(f"""
            <div class="metric-card">
                <h4>{resultado['metro_dominante']}</h4>
                <p><strong>Regularidad:</strong> {resultado['regularidad_metrica']}</p>
                <p><strong>Ritmo:</strong> {resultado['analisis_ritmico']['tipo']}</p>
                <p><strong>Regularidad rítmica:</strong> {resultado['analisis_ritmico']['regularidad']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Gráfico de distribución silábica
            st.subheader("📊 Distribución de Sílabas")
            silabas_por_verso = [v['silabas'] for v in resultado['versos_analizados']]
            
            fig = px.bar(
                x=list(range(1, len(silabas_por_verso) + 1)),
                y=silabas_por_verso,
                labels={'x': 'Número de Verso', 'y': 'Sílabas'},
                title="Sílabas por Verso"
            )
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
    
    except Exception as e:
        st.error(f"Error en análisis: {e}")
    
    st.markdown('</div>', unsafe_allow_html=True)

def mostrar_estadisticas(app):
    """Pestaña de estadísticas"""
    st.header("📊 Estadísticas y Análisis Avanzado")
    
    if not st.session_state.historial_analisis:
        st.info("Realiza algunos análisis para ver estadísticas detalladas")
        return
    
    # Estadísticas generales
    st.subheader("📈 Resumen General")
    
    total_analisis = len(st.session_state.historial_analisis)
    total_versos = sum(a['estadisticas']['total_versos'] for a in st.session_state.historial_analisis)
    total_palabras = sum(a['estadisticas'].get('total_palabras', 0) for a in st.session_state.historial_analisis)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Poemas analizados", total_analisis)
    with col2:
        st.metric("Versos totales", total_versos)
    with col3:
        st.metric("Palabras totales", total_palabras)
    with col4:
        avg_versos = total_versos / total_analisis if total_analisis > 0 else 0
        st.metric("Promedio versos/poema", f"{avg_versos:.1f}")

def mostrar_mis_poemas(app):
    """Pestaña para gestionar poemas guardados"""
    st.header("💾 Mis Poemas Guardados")
    
    if st.session_state.poemas_guardados:
        for titulo, datos in st.session_state.poemas_guardados.items():
            with st.expander(f"📄 {titulo}"):
                st.markdown(f"**Fecha:** {datos['fecha']}")
                st.markdown(f"**Versos:** {datos['estadisticas']['versos']}")
                st.markdown(f"**Palabras:** {datos['estadisticas']['palabras']}")
                
                st.markdown("**Contenido:**")
                st.text_area("", value=datos['contenido'], height=200, disabled=True, key=f"view_{titulo}")
                
                col_btn1, col_btn2, col_btn3 = st.columns(3)
                
                with col_btn1:
                    if st.button("🔊 Recitar", key=f"recitar_{titulo}"):
                        recitar_poema_seguro(app, datos['contenido'])
                
                with col_btn2:
                    if st.button("📝 Editar", key=f"editar_{titulo}"):
                        st.session_state.texto_ejemplo_cargado = datos['contenido']
                        st.session_state.cargar_ejemplo = True
                        st.success("Poema cargado en el editor")
                
                with col_btn3:
                    if st.button("🗑️ Eliminar", key=f"eliminar_{titulo}"):
                        del st.session_state.poemas_guardados[titulo]
                        st.success("Poema eliminado")
                        st.rerun()
    else:
        st.info("No tienes poemas guardados. Guarda algunos desde la pestaña de análisis.")

def mostrar_configuracion(app):
    """Pestaña de configuración avanzada"""
    st.header("⚙️ Configuración Avanzada")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🔧 Diagnóstico del Sistema")
        
        # Información detallada del sistema de voz
        try:
            stats = st.session_state.sistema_voz.obtener_estadisticas_voz()
            
            st.write("**Sistema de voz:**")
            st.json(stats)
            
            # Botón para reinicializar sistema de voz
            if st.button("🔄 Reinicializar Sistema de Voz"):
                try:
                    from utils.voz import crear_sistema_voz
                    st.session_state.sistema_voz = crear_sistema_voz()
                    st.success("Sistema de voz reinicializado")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error reinicializando: {e}")
            
        except Exception as e:
            st.error(f"Error obteniendo información del sistema: {e}")
    
    with col2:
        st.subheader("💾 Gestión de Datos")
        
        # Backup y restauración
        if st.button("📤 Exportar Configuración"):
            config_data = {
                'configuracion_voz': st.session_state.configuracion_voz,
                'poemas_guardados': st.session_state.poemas_guardados,
                'historial_analisis': st.session_state.historial_analisis
            }
            
            st.download_button(
                label="💾 Descargar Backup",
                data=json.dumps(config_data, indent=2, default=str),
                file_name=f"poetry_analyzer_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )

# Funciones auxiliares para manejo de voz y análisis

def recitar_poema_seguro(app, texto):
    """Función segura para recitar un poema"""
    try:
        with st.spinner("Iniciando recitado..."):
            success = st.session_state.sistema_voz.hablar_con_config(
                texto, st.session_state.configuracion_voz
            )
            
            if success:
                st.success("🔊 Recitado iniciado")
                
                # Mostrar controles
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("⏸️ Pausar", key="pause_main"):
                        st.session_state.sistema_voz.pausar()
                        st.info("Recitado pausado")
                
                with col2:
                    if st.button("⏹️ Detener", key="stop_main"):
                        st.session_state.sistema_voz.detener()
                        st.info("Recitado detenido")
            else:
                st.warning("⚠️ Error iniciando recitado - verifica configuración de voz")
                
    except Exception as e:
        st.error(f"Error en recitado: {e}")
        # Sugerir soluciones
        st.markdown("""
        **Posibles soluciones:**
        1. Reinicia la aplicación
        2. Verifica que tu sistema tiene síntesis de voz habilitada
        3. Intenta con un texto más corto
        """)

def probar_voz_segura(texto_prueba):
    """Prueba la configuración de voz de forma segura"""
    try:
        with st.spinner("Reproduciendo prueba..."):
            success = st.session_state.sistema_voz.hablar_con_config(
                texto_prueba, st.session_state.configuracion_voz
            )
            
            if success:
                st.info("🔊 Reproduciendo audio de prueba...")
            else:
                st.warning("⚠️ Error en prueba de voz")
                
    except Exception as e:
        st.error(f"Error en prueba de voz: {e}")

def detener_voz_segura():
    """Detiene la síntesis de voz de forma segura"""
    try:
        st.session_state.sistema_voz.detener()
        st.info("🛑 Síntesis de voz detenida")
    except Exception as e:
        st.error(f"Error deteniendo voz: {e}")

def realizar_analisis_completo(app, texto):
    """Realiza un análisis completo y lo guarda en el historial"""
    try:
        resultado = st.session_state.analizador.analisis_completo(texto)
        
        if "error" not in resultado:
            # Agregar al historial
            resultado['fecha'] = datetime.now()
            resultado['texto_original'] = texto
            st.session_state.historial_analisis.append(resultado)
            
            st.success("✅ Análisis completado y guardado en historial")
        else:
            st.error(resultado["error"])
    except Exception as e:
        st.error(f"Error en análisis: {e}")

def guardar_poema(app, texto):
    """Guarda un poema en la colección personal"""
    titulo = st.text_input("Título del poema:", key="titulo_guardar")
    
    if titulo and st.button("💾 Confirmar Guardado"):
        try:
            versos = [v.strip() for v in texto.split('\n') if v.strip()]
            palabras = sum(len(v.split()) for v in versos)
            
            st.session_state.poemas_guardados[titulo] = {
                'contenido': texto,
                'fecha': datetime.now().strftime('%Y-%m-%d %H:%M'),
                'estadisticas': {
                    'versos': len(versos),
                    'palabras': palabras,
                    'caracteres': len(texto)
                }
            }
            
            st.success(f"Poema '{titulo}' guardado exitosamente")
        except Exception as e:
            st.error(f"Error guardando poema: {e}")

def exportar_poema(app, texto):
    """Exporta un poema en diferentes formatos"""
    formato = st.selectbox("Formato de exportación:", ["TXT", "PDF", "HTML", "JSON"])
    
    if st.button("📄 Exportar"):
        try:
            if formato == "TXT":
                st.download_button(
                    "💾 Descargar TXT",
                    data=texto,
                    file_name=f"poema_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain"
                )
                st.success("Archivo TXT generado")
            else:
                st.info(f"Exportación a {formato} en desarrollo")
        except Exception as e:
            st.error(f"Error en exportación: {e}")

if __name__ == "__main__":
    main()