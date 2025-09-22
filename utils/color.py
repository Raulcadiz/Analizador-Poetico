# Añadir esta función en app.py después de la función main()

def crear_css_dinamico():
    """CSS mejorado con colores dinámicos para el textarea"""
    return """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Crimson+Text:ital,wght@0,400;0,600;1,400&display=swap');
    
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
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
    
    /* Estilos para textarea con colores dinámicos */
    .stTextArea textarea {
        font-family: 'Crimson Text', serif !important;
        font-size: 16px !important;
        line-height: 1.8 !important;
        transition: all 0.3s ease !important;
        border-radius: 8px !important;
    }
    
    /* Colores por número de sílabas */
    .silabas-8 {
        background-color: #e8f5e8 !important;
        border: 2px solid #4caf50 !important;
        color: #2e7d32 !important;
    }
    
    .silabas-11 {
        background-color: #fff3e0 !important;
        border: 2px solid #ff9800 !important;
        color: #e65100 !important;
    }
    
    .silabas-14 {
        background-color: #fffde7 !important;
        border: 2px solid #ffeb3b !important;
        color: #f57f17 !important;
    }
    
    .silabas-exceso {
        background-color: #ffebee !important;
        border: 2px solid #f44336 !important;
        color: #c62828 !important;
    }
    
    .silabas-normal {
        background-color: #fafafa !important;
        border: 2px solid #e0e0e0 !important;
        color: #333 !important;
    }
    
    .metric-card {
        background: linear-gradient(145deg, #f8f9fa, #e9ecef);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid #667eea;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        transition: transform 0.2s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
    }
    
    .verse-analysis {
        background: #ffffff;
        padding: 1.5rem;
        border-radius: 12px;
        border: 2px solid #e0e0e0;
        margin: 1rem 0;
        font-family: 'Crimson Text', serif;
        line-height: 1.8;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    
    .rhyme-pattern {
        font-family: 'Courier New', monospace;
        background: #f0f0f0;
        padding: 1rem;
        border-radius: 8px;
        display: inline-block;
        font-weight: bold;
        border-left: 4px solid #764ba2;
    }
    
    /* Indicador de sílabas */
    .silabas-indicator {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 14px;
        margin: 10px 0;
        display: inline-block;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
    }
    
    .voice-status-card {
        background: #e3f2fd;
        border: 2px solid #2196f3;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .voice-error-card {
        background: #ffebee;
        border: 2px solid #f44336;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .voice-success-card {
        background: #e8f5e8;
        border: 2px solid #4caf50;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>

<script>
function actualizarColorTexto() {
    const textarea = document.querySelector('.stTextArea textarea');
    if (!textarea) return;
    
    const texto = textarea.value;
    const lineas = texto.split('\\n');
    const lineaActual = lineas[textarea.value.substr(0, textarea.selectionStart).split('\\n').length - 1];
    
    if (!lineaActual || lineaActual.trim() === '') {
        textarea.className = textarea.className.replace(/silabas-\\w+/g, '') + ' silabas-normal';
        return;
    }
    
    // Aquí deberías calcular las sílabas (simplificado)
    const palabras = lineaActual.trim().split(/\\s+/);
    const silabas = contarSilabasAproximado(palabras);
    
    // Remover clases anteriores
    textarea.className = textarea.className.replace(/silabas-\\w+/g, '');
    
    // Añadir nueva clase según sílabas
    if (silabas === 8) {
        textarea.className += ' silabas-8';
    } else if (silabas === 11) {
        textarea.className += ' silabas-11';
    } else if (silabas === 14) {
        textarea.className += ' silabas-14';
    } else if (silabas > 14) {
        textarea.className += ' silabas-exceso';
    } else {
        textarea.className += ' silabas-normal';
    }
    
    // Actualizar indicador
    actualizarIndicadorSilabas(silabas);
}

function contarSilabasAproximado(palabras) {
    let total = 0;
    for (let palabra of palabras) {
        total += contarSilabasPalabra(palabra);
    }
    return total;
}

function contarSilabasPalabra(palabra) {
    // Conteo simplificado - en producción usar el contador Python
    const vocales = 'aeiouáéíóúü';
    let silabas = 0;
    let anteriorEsVocal = false;
    
    for (let i = 0; i < palabra.length; i++) {
        const letra = palabra[i].toLowerCase();
        const esVocal = vocales.includes(letra);
        
        if (esVocal && !anteriorEsVocal) {
            silabas++;
        }
        anteriorEsVocal = esVocal;
    }
    
    return Math.max(1, silabas);
}

function actualizarIndicadorSilabas(silabas) {
    let indicador = document.querySelector('.silabas-indicator');
    if (!indicador) {
        indicador = document.createElement('div');
        indicador.className = 'silabas-indicator';
        const container = document.querySelector('.stTextArea').parentNode;
        container.insertBefore(indicador, container.firstChild);
    }
    
    let color = '#667eea';
    let texto = `${silabas} sílabas`;
    
    if (silabas === 8) {
        color = '#4caf50';
        texto += ' (Octosílabo) ✓';
    } else if (silabas === 11) {
        color = '#ff9800';
        texto += ' (Endecasílabo) ✓';
    } else if (silabas === 14) {
        color = '#ffeb3b';
        texto += ' (Alejandrino) ✓';
    } else if (silabas > 14) {
        color = '#f44336';
        texto += ' (Exceso)';
    }
    
    indicador.style.background = color;
    indicador.textContent = texto;
}

// Activar el listener cuando se carga la página
document.addEventListener('DOMContentLoaded', function() {
    setTimeout(() => {
        const textarea = document.querySelector('.stTextArea textarea');
        if (textarea) {
            textarea.addEventListener('input', actualizarColorTexto);
            textarea.addEventListener('keyup', actualizarColorTexto);
            textarea.addEventListener('click', actualizarColorTexto);
        }
    }, 1000);
});
</script>
"""

# Función para mostrar análisis en tiempo real
def mostrar_analisis_tiempo_real(app, texto_actual):
    """Muestra análisis de sílabas en tiempo real"""
    if not texto_actual.strip():
        return
    
    lineas = texto_actual.split('\n')
    linea_actual = lineas[-1] if lineas else ""
    
    if linea_actual.strip():
        silabas = app.session_state.contador.contar_silabas_verso(linea_actual)
        
        # Crear indicador visual
        color = "#e0e0e0"
        emoji = "📝"
        mensaje = f"{silabas} sílabas"
        
        if silabas == 8:
            color = "#4caf50"
            emoji = "✅"
            mensaje += " (Octosílabo)"
        elif silabas == 11:
            color = "#ff9800"
            emoji = "🔥"
            mensaje += " (Endecasílabo)"
        elif silabas == 14:
            color = "#ffeb3b"
            emoji = "⭐"
            mensaje += " (Alejandrino)"
        elif silabas > 14:
            color = "#f44336"
            emoji = "⚠️"
            mensaje += " (Exceso)"
        
        st.markdown(f"""
        <div style="background: {color}; color: white; padding: 8px 16px; 
                    border-radius: 20px; display: inline-block; margin: 5px 0;
                    font-weight: bold; font-size: 14px;">
            {emoji} {mensaje}
        </div>
        """, unsafe_allow_html=True)