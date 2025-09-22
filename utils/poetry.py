import streamlit as st
import pyttsx3
import threading
import time
from utils.metrica import AnalizadorMetrico
from utils.silabas import ContadorSilabas
from utils.rimas import DetectorRimas
import io
import base64

# Configuración de la página
st.set_page_config(
    page_title="Analizador Poético Pro",
    page_icon="🎭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado para mejor apariencia
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #667eea;
        margin: 0.5rem 0;
    }
    .verse-analysis {
        background: #ffffff;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #e0e0e0;
        margin: 0.5rem 0;
    }
    .rhyme-pattern {
        font-family: 'Courier New', monospace;
        background: #f0f0f0;
        padding: 0.5rem;
        border-radius: 4px;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

class SistemaVoz:
    def __init__(self):
        self.engine = None
        self.inicializar_voz()
    
    def inicializar_voz(self):
        try:
            self.engine = pyttsx3.init()
            voices = self.engine.getProperty('voices')
            
            # Buscar voz en español
            spanish_voice = None
            for voice in voices:
                if 'spanish' in voice.name.lower() or 'españa' in voice.name.lower():
                    spanish_voice = voice.id
                    break
            
            if spanish_voice:
                self.engine.setProperty('voice', spanish_voice)
            
            # Configurar velocidad y volumen para poesía
            self.engine.setProperty('rate', 150)  # Más lento para poesía
            self.engine.setProperty('volume', 0.9)
            
        except Exception as e:
            st.error(f"Error inicializando síntesis de voz: {e}")
    
    def hablar(self, texto, velocidad=150, pausa_verso=0.8):
        if not self.engine:
            return False
        
        try:
            self.engine.setProperty('rate', velocidad)
            
            # Procesar poesía línea por línea con pausas
            versos = texto.split('\n')
            for verso in versos:
                if verso.strip():
                    self.engine.say(verso)
                    self.engine.runAndWait()
                    time.sleep(pausa_verso)
                else:
                    time.sleep(pausa_verso * 2)  # Pausa más larga entre estrofas
            
            return True
        except Exception as e:
            st.error(f"Error en síntesis de voz: {e}")
            return False

def main():
    # Header principal
    st.markdown("""
    <div class="main-header">
        <h1>🎭 Analizador Poético Pro</h1>
        <p>Análisis métrico avanzado con síntesis de voz especializada en poesía</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Inicializar componentes
    if 'analizador' not in st.session_state:
        st.session_state.analizador = AnalizadorMetrico()
        st.session_state.contador = ContadorSilabas()
        st.session_state.detector_rimas = DetectorRimas()
        st.session_state.sistema_voz = SistemaVoz()
    
    # Sidebar con controles
    with st.sidebar:
        st.header("🎛️ Controles de Voz")
        
        velocidad_voz = st.slider("Velocidad de lectura", 100, 250, 150)
        pausa_verso = st.slider("Pausa entre versos (seg)", 0.2, 2.0, 0.8)
        
        st.header("📊 Tipo de Análisis")
        analisis_basico = st.checkbox("Análisis básico", True)
        analisis_metrico = st.checkbox("Análisis métrico avanzado", True)
        analisis_rimas = st.checkbox("Detección de rimas", True)
        analisis_ritmo = st.checkbox("Análisis de ritmo", True)
    
    # Input principal
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("✍️ Escribe tu poesía")
        texto_poesia = st.text_area(
            "Introduce tu poema aquí:",
            height=300,
            placeholder="""En un lugar de la Mancha,
de cuyo nombre no quiero acordarme,
no ha mucho tiempo que vivía
un hidalgo de los de lanza en astillero..."""
        )
        
        # Botones de acción
        col_btn1, col_btn2, col_btn3 = st.columns(3)
        
        with col_btn1:
            if st.button("🔊 Recitar Poema", type="primary"):
                if texto_poesia.strip():
                    with st.spinner("Recitando poema..."):
                        def recitar():
                            st.session_state.sistema_voz.hablar(
                                texto_poesia, velocidad_voz, pausa_verso
                            )
                        
                        thread = threading.Thread(target=recitar)
                        thread.daemon = True
                        thread.start()
                        st.success("Recitado iniciado")
                else:
                    st.warning("Escribe un poema primero")
        
        with col_btn2:
            if st.button("📈 Analizar"):
                if texto_poesia.strip():
                    st.session_state.ultimo_analisis = texto_poesia
                    st.rerun()
        
        with col_btn3:
            if st.button("🧹 Limpiar"):
                st.rerun()
    
    with col2:
        st.subheader("🎨 Ejemplos")
        ejemplo = st.selectbox("Cargar ejemplo:", [
            "Seleccionar...",
            "Romance clásico",
            "Soneto",
            "Verso libre",
            "Redondilla"
        ])
        
        ejemplos = {
            "Romance clásico": """Que por mayo era, por mayo,
cuando hace la calor,
cuando los trigos encañan
y están los campos en flor.""",
            
            "Soneto": """Mientras por competir con tu cabello
oro bruñido al sol relumbra en vano,
mientras con menosprecio en medio el llano
mira tu blanca frente el lilio bello.""",
            
            "Verso libre": """Verde que te quiero verde.
Verde viento. Verdes ramas.
El barco sobre la mar
y el caballo en la montaña.""",
            
            "Redondilla": """En tanto que de rosa y azucena
se muestra la color en vuestro gesto,
y que vuestro mirar ardiente, honesto,
enciende al corazón y lo refrena."""
        }
        
        if ejemplo != "Seleccionar..." and ejemplo in ejemplos:
            if st.button(f"📋 Usar {ejemplo}"):
                st.session_state.texto_ejemplo = ejemplos[ejemplo]
                st.rerun()
    
    # Cargar ejemplo si está seleccionado
    if 'texto_ejemplo' in st.session_state:
        texto_poesia = st.session_state.texto_ejemplo
        del st.session_state.texto_ejemplo
    
    # Análisis del texto
    if texto_poesia.strip() and 'ultimo_analisis' in st.session_state:
        st.header("📊 Análisis Poético")
        
        versos = [v.strip() for v in texto_poesia.split('\n') if v.strip()]
        
        if analisis_basico:
            st.subheader("📈 Análisis Básico")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Versos", len(versos))
            with col2:
                palabras = sum(len(v.split()) for v in versos)
                st.metric("Palabras", palabras)
            with col3:
                estrofas = len([e for e in texto_poesia.split('\n\n') if e.strip()])
                st.metric("Estrofas", estrofas)
            with col4:
                caracteres = len(texto_poesia.replace(' ', ''))
                st.metric("Caracteres", caracteres)
        
        if analisis_metrico:
            st.subheader("🎵 Análisis Métrico")
            
            # Análisis por verso
            analisis_versos = []
            for i, verso in enumerate(versos, 1):
                silabas = st.session_state.contador.contar_silabas_verso(verso)
                tipo_metro = st.session_state.analizador.clasificar_metro(silabas)
                
                analisis_versos.append({
                    'numero': i,
                    'verso': verso,
                    'silabas': silabas,
                    'tipo': tipo_metro
                })
            
            # Mostrar análisis
            for analisis in analisis_versos:
                st.markdown(f"""
                <div class="verse-analysis">
                    <strong>Verso {analisis['numero']}:</strong> {analisis['silabas']} sílabas ({analisis['tipo']})<br>
                    <em>"{analisis['verso']}"</em>
                </div>
                """, unsafe_allow_html=True)
            
            # Estadísticas métricas
            silabas_total = [a['silabas'] for a in analisis_versos]
            metro_dominante = st.session_state.analizador.detectar_metro_dominante(silabas_total)
            
            st.markdown(f"""
            <div class="metric-card">
                <h4>Metro dominante: {metro_dominante}</h4>
                <p>Promedio de sílabas: {sum(silabas_total)/len(silabas_total):.1f}</p>
                <p>Regularidad métrica: {st.session_state.analizador.calcular_regularidad(silabas_total)}</p>
            </div>
            """, unsafe_allow_html=True)
        
        if analisis_rimas:
            st.subheader("🎼 Análisis de Rimas")
            
            esquema_rimas = st.session_state.detector_rimas.detectar_esquema(versos)
            tipo_rima = st.session_state.detector_rimas.clasificar_rima(esquema_rimas)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Esquema de rimas:**")
                for i, letra in enumerate(esquema_rimas, 1):
                    st.markdown(f"Verso {i}: **{letra}** - _{versos[i-1]}_")
            
            with col2:
                st.markdown(f"""
                <div class="metric-card">
                    <h4>Tipo de rima: {tipo_rima}</h4>
                    <div class="rhyme-pattern">
                        Patrón: {''.join(esquema_rimas)}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        if analisis_ritmo:
            st.subheader("🥁 Análisis de Ritmo")
            
            ritmo = st.session_state.analizador.analizar_ritmo(versos)
            
            st.markdown(f"""
            <div class="metric-card">
                <h4>Análisis rítmico:</h4>
                <p><strong>Ritmo detectado:</strong> {ritmo['tipo']}</p>
                <p><strong>Regularidad:</strong> {ritmo['regularidad']}</p>
                <p><strong>Acentos dominantes:</strong> {', '.join(map(str, ritmo['acentos_comunes']))}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666;">
        🎭 Analizador Poético Pro - Especializado en métrica española
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()