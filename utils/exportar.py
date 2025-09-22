import json
import csv
from datetime import datetime
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.lib import colors
from reportlab.lib.fonts import addMapping
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import io
import base64

class ExportadorPoesia:
    def __init__(self):
        self.setup_styles()
    
    def setup_styles(self):
        """Configura los estilos para documentos"""
        self.styles = getSampleStyleSheet()
        
        # Estilo para título principal
        self.styles.add(ParagraphStyle(
            name='TituloPoesia',
            parent=self.styles['Title'],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.darkblue,
            fontName='Times-Bold'
        ))
        
        # Estilo para subtítulos
        self.styles.add(ParagraphStyle(
            name='SubtituloPoesia',
            parent=self.styles['Heading2'],
            fontSize=16,
            spaceBefore=20,
            spaceAfter=15,
            alignment=TA_CENTER,
            textColor=colors.grey,
            fontName='Times-Italic'
        ))
        
        # Estilo para versos
        self.styles.add(ParagraphStyle(
            name='VersoPoesia',
            parent=self.styles['Normal'],
            fontSize=12,
            spaceBefore=3,
            spaceAfter=3,
            alignment=TA_LEFT,
            leftIndent=0.5*inch,
            fontName='Times-Roman',
            leading=18
        ))
        
        # Estilo para estrofas
        self.styles.add(ParagraphStyle(
            name='EstrofaSeparador',
            parent=self.styles['Normal'],
            fontSize=12,
            spaceBefore=15,
            spaceAfter=15,
            alignment=TA_CENTER
        ))
        
        # Estilo para metadatos
        self.styles.add(ParagraphStyle(
            name='MetadatosPoesia',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceBefore=10,
            spaceAfter=10,
            alignment=TA_CENTER,
            textColor=colors.grey,
            fontName='Times-Italic'
        ))
        
        # Estilo para análisis técnico
        self.styles.add(ParagraphStyle(
            name='AnalisisTecnico',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceBefore=5,
            spaceAfter=5,
            alignment=TA_LEFT,
            leftIndent=0.25*inch,
            fontName='Courier'
        ))
    
    def exportar_pdf(self, texto, titulo="Mi Poema", metadatos=None, incluir_analisis=False):
        """Exporta un poema a PDF con formato elegante"""
        buffer = io.BytesIO()
        
        try:
            doc = SimpleDocTemplate(
                buffer,
                pagesize=A4,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=72
            )
            
            story = []
            
            # Título principal
            story.append(Paragraph(titulo, self.styles['TituloPoesia']))
            story.append(Spacer(1, 20))
            
            # Metadatos si se proporcionan
            if metadatos:
                if metadatos.get('autor'):
                    story.append(Paragraph(f"Por: {metadatos['autor']}", self.styles['MetadatosPoesia']))
                
                if metadatos.get('fecha'):
                    story.append(Paragraph(f"Fecha: {metadatos['fecha']}", self.styles['MetadatosPoesia']))
                
                if metadatos.get('descripcion'):
                    story.append(Paragraph(metadatos['descripcion'], self.styles['MetadatosPoesia']))
                
                story.append(Spacer(1, 30))
            
            # Procesar el poema
            estrofas = [e.strip() for e in texto.split('\n\n') if e.strip()]
            
            if not estrofas:
                estrofas = [texto.strip()]
            
            for i, estrofa in enumerate(estrofas):
                versos = [v.strip() for v in estrofa.split('\n') if v.strip()]
                
                for verso in versos:
                    if verso:
                        story.append(Paragraph(verso, self.styles['VersoPoesia']))
                
                # Separador entre estrofas (excepto la última)
                if i < len(estrofas) - 1:
                    story.append(Spacer(1, 20))
            
            # Análisis técnico si se solicita
            if incluir_analisis and metadatos and 'analisis' in metadatos:
                story.append(PageBreak())
                story.append(Paragraph("Análisis Métrico", self.styles['TituloPoesia']))
                story.append(Spacer(1, 20))
                
                analisis = metadatos['analisis']
                
                story.append(Paragraph(f"Metro dominante: {analisis.get('metro_dominante', 'N/A')}", 
                                     self.styles['AnalisisTecnico']))
                story.append(Paragraph(f"Esquema de rimas: {analisis.get('esquema_rimas', 'N/A')}", 
                                     self.styles['AnalisisTecnico']))
                story.append(Paragraph(f"Total de versos: {analisis.get('total_versos', 'N/A')}", 
                                     self.styles['AnalisisTecnico']))
                story.append(Paragraph(f"Total de palabras: {analisis.get('total_palabras', 'N/A')}", 
                                     self.styles['AnalisisTecnico']))
            
            # Pie de página
            story.append(Spacer(1, 50))
            story.append(Paragraph(f"Generado con Analizador Poético Pro - {datetime.now().strftime('%d/%m/%Y %H:%M')}", 
                                 self.styles['MetadatosPoesia']))
            
            doc.build(story)
            buffer.seek(0)
            return buffer.getvalue()
            
        except Exception as e:
            print(f"Error generando PDF: {e}")
            return None
    
    def exportar_txt(self, texto, titulo="Mi Poema", metadatos=None):
        """Exporta a formato TXT plano"""
        contenido = []
        
        # Encabezado
        contenido.append("=" * 60)
        contenido.append(titulo.upper().center(60))
        contenido.append("=" * 60)
        contenido.append("")
        
        # Metadatos
        if metadatos:
            if metadatos.get('autor'):
                contenido.append(f"Autor: {metadatos['autor']}")
            if metadatos.get('fecha'):
                contenido.append(f"Fecha: {metadatos['fecha']}")
            if metadatos.get('descripcion'):
                contenido.append(f"Descripción: {metadatos['descripcion']}")
            contenido.append("")
        
        contenido.append("-" * 40)
        contenido.append("")
        
        # Contenido del poema
        contenido.append(texto)
        contenido.append("")
        contenido.append("-" * 40)
        contenido.append(f"Generado el: {datetime.now().strftime('%d/%m/%Y a las %H:%M:%S')}")
        contenido.append("Analizador Poético Pro")
        
        return "\n".join(contenido)
    
    def exportar_html(self, texto, titulo="Mi Poema", metadatos=None, incluir_analisis=False):
        """Exporta a formato HTML con estilos CSS"""
        css_styles = """
        <style>
            body {
                font-family: 'Times New Roman', serif;
                max-width: 800px;
                margin: 0 auto;
                padding: 40px 20px;
                line-height: 1.6;
                background-color: #fafafa;
                color: #333;
            }
            
            .header {
                text-align: center;
                margin-bottom: 40px;
                border-bottom: 2px solid #ddd;
                padding-bottom: 20px;
            }
            
            .titulo {
                font-size: 2.5em;
                font-weight: bold;
                color: #2c3e50;
                margin-bottom: 10px;
                text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
            }
            
            .metadatos {
                font-style: italic;
                color: #666;
                margin-bottom: 10px;
            }
            
            .poema {
                background: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                margin: 30px 0;
            }
            
            .estrofa {
                margin-bottom: 25px;
            }
            
            .verso {
                margin: 5px 0;
                padding-left: 20px;
                font-size: 1.1em;
                line-height: 1.8;
            }
            
            .analisis {
                background: #f8f9fa;
                padding: 20px;
                border-radius: 8px;
                border-left: 4px solid #007bff;
                margin-top: 30px;
            }
            
            .analisis h3 {
                color: #007bff;
                margin-top: 0;
            }
            
            .footer {
                text-align: center;
                margin-top: 40px;
                padding-top: 20px;
                border-top: 1px solid #ddd;
                font-size: 0.9em;
                color: #999;
            }
            
            @media print {
                body { background: white; }
                .poema { box-shadow: none; }
            }
        </style>
        """
        
        html_content = f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{titulo}</title>
            {css_styles}
        </head>
        <body>
            <div class="header">
                <h1 class="titulo">{titulo}</h1>
        """
        
        # Agregar metadatos
        if metadatos:
            if metadatos.get('autor'):
                html_content += f'<p class="metadatos">Por: {metadatos["autor"]}</p>'
            if metadatos.get('fecha'):
                html_content += f'<p class="metadatos">Fecha: {metadatos["fecha"]}</p>'
            if metadatos.get('descripcion'):
                html_content += f'<p class="metadatos">{metadatos["descripcion"]}</p>'
        
        html_content += "</div>\n<div class=\"poema\">\n"
        
        # Procesar el poema
        estrofas = [e.strip() for e in texto.split('\n\n') if e.strip()]
        
        if not estrofas:
            estrofas = [texto.strip()]
        
        for estrofa in estrofas:
            html_content += '<div class="estrofa">\n'
            
            versos = [v.strip() for v in estrofa.split('\n') if v.strip()]
            for verso in versos:
                if verso:
                    html_content += f'<div class="verso">{verso}</div>\n'
            
            html_content += '</div>\n'
        
        html_content += "</div>\n"
        
        # Análisis si se incluye
        if incluir_analisis and metadatos and 'analisis' in metadatos:
            analisis = metadatos['analisis']
            html_content += f"""
            <div class="analisis">
                <h3>Análisis Métrico</h3>
                <p><strong>Metro dominante:</strong> {analisis.get('metro_dominante', 'N/A')}</p>
                <p><strong>Esquema de rimas:</strong> {analisis.get('esquema_rimas', 'N/A')}</p>
                <p><strong>Total de versos:</strong> {analisis.get('total_versos', 'N/A')}</p>
                <p><strong>Total de palabras:</strong> {analisis.get('total_palabras', 'N/A')}</p>
            </div>
            """
        
        # Footer
        html_content += f"""
            <div class="footer">
                <p>Generado con Analizador Poético Pro</p>
                <p>{datetime.now().strftime('%d de %B de %Y a las %H:%M')}</p>
            </div>
        </body>
        </html>
        """
        
        return html_content
    
    def exportar_json(self, texto, titulo="Mi Poema", metadatos=None, analisis=None):
        """Exporta a formato JSON estructurado"""
        versos = [v.strip() for v in texto.split('\n') if v.strip()]
        estrofas = []
        
        estrofas_raw = [e.strip() for e in texto.split('\n\n') if e.strip()]
        
        for i, estrofa_raw in enumerate(estrofas_raw):
            versos_estrofa = [v.strip() for v in estrofa_raw.split('\n') if v.strip()]
            estrofas.append({
                'numero': i + 1,
                'versos': versos_estrofa,
                'total_versos': len(versos_estrofa)
            })
        
        datos = {
            'poema': {
                'titulo': titulo,
                'contenido_completo': texto,
                'estrofas': estrofas,
                'estadisticas_basicas': {
                    'total_versos': len(versos),
                    'total_estrofas': len(estrofas),
                    'total_palabras': sum(len(v.split()) for v in versos),
                    'total_caracteres': len(texto)
                }
            },
            'metadatos': metadatos or {},
            'analisis': analisis or {},
            'exportacion': {
                'fecha': datetime.now().isoformat(),
                'version_app': '1.0.0',
                'formato': 'JSON'
            }
        }
        
        return json.dumps(datos, indent=2, ensure_ascii=False)
    
    def exportar_csv_analisis(self, lista_poemas):
        """Exporta análisis de múltiples poemas a CSV"""
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Encabezados
        headers = [
            'Título', 'Fecha', 'Versos', 'Palabras', 'Estrofas',
            'Metro Dominante', 'Esquema Rimas', 'Tipo Rima',
            'Regularidad Métrica', 'Contenido'
        ]
        writer.writerow(headers)
        
        # Datos
        for poema in lista_poemas:
            row = [
                poema.get('titulo', ''),
                poema.get('fecha', ''),
                poema.get('estadisticas', {}).get('total_versos', 0),
                poema.get('estadisticas', {}).get('total_palabras', 0),
                poema.get('estadisticas', {}).get('total_estrofas', 0),
                poema.get('analisis', {}).get('metro_dominante', ''),
                poema.get('analisis', {}).get('esquema_rimas', ''),
                poema.get('analisis', {}).get('tipo_rima', ''),
                poema.get('analisis', {}).get('regularidad_metrica', ''),
                poema.get('contenido', '')[:100] + '...' if len(poema.get('contenido', '')) > 100 else poema.get('contenido', '')
            ]
            writer.writerow(row)
        
        output.seek(0)
        return output.getvalue()
    
    def exportar_markdown(self, texto, titulo="Mi Poema", metadatos=None):
        """Exporta a formato Markdown"""
        contenido = []
        
        # Título principal
        contenido.append(f"# {titulo}")
        contenido.append("")
        
        # Metadatos
        if metadatos:
            if metadatos.get('autor'):
                contenido.append(f"**Autor:** {metadatos['autor']}")
            if metadatos.get('fecha'):
                contenido.append(f"**Fecha:** {metadatos['fecha']}")
            if metadatos.get('descripcion'):
                contenido.append(f"**Descripción:** {metadatos['descripcion']}")
            contenido.append("")
        
        contenido.append("---")
        contenido.append("")
        
        # Contenido del poema
        estrofas = [e.strip() for e in texto.split('\n\n') if e.strip()]
        
        if not estrofas:
            estrofas = [texto.strip()]
        
        for i, estrofa in enumerate(estrofas):
            versos = [v.strip() for v in estrofa.split('\n') if v.strip()]
            
            for verso in versos:
                if verso:
                    contenido.append(f"> {verso}")
            
            if i < len(estrofas) - 1:
                contenido.append(">")
                contenido.append("")
        
        contenido.append("")
        contenido.append("---")
        contenido.append("")
        contenido.append(f"*Generado el {datetime.now().strftime('%d de %B de %Y')} con Analizador Poético Pro*")
        
        return "\n".join(contenido)
    
    def crear_antologia_pdf(self, lista_poemas, titulo_antologia="Mi Antología Poética"):
        """Crea una antología completa en PDF"""
        buffer = io.BytesIO()
        
        try:
            doc = SimpleDocTemplate(
                buffer,
                pagesize=A4,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=72
            )
            
            story = []
            
            # Página de título
            story.append(Paragraph(titulo_antologia, self.styles['TituloPoesia']))
            story.append(Spacer(1, 30))
            story.append(Paragraph(f"Colección de {len(lista_poemas)} poemas", self.styles['SubtituloPoesia']))
            story.append(Spacer(1, 20))
            story.append(Paragraph(f"Compilado el {datetime.now().strftime('%d de %B de %Y')}", self.styles['MetadatosPoesia']))
            story.append(PageBreak())
            
            # Índice
            story.append(Paragraph("Índice", self.styles['TituloPoesia']))
            story.append(Spacer(1, 20))
            
            for i, poema in enumerate(lista_poemas, 1):
                titulo_poema = poema.get('titulo', f'Poema {i}')
                story.append(Paragraph(f"{i}. {titulo_poema}", self.styles['Normal']))
            
            story.append(PageBreak())
            
            # Poemas
            for i, poema in enumerate(lista_poemas, 1):
                titulo_poema = poema.get('titulo', f'Poema {i}')
                contenido_poema = poema.get('contenido', '')
                
                story.append(Paragraph(titulo_poema, self.styles['TituloPoesia']))
                story.append(Spacer(1, 20))
                
                # Metadatos del poema si existen
                if poema.get('fecha'):
                    story.append(Paragraph(f"Fecha: {poema['fecha']}", self.styles['MetadatosPoesia']))
                    story.append(Spacer(1, 10))
                
                # Contenido
                estrofas = [e.strip() for e in contenido_poema.split('\n\n') if e.strip()]
                
                if not estrofas:
                    estrofas = [contenido_poema.strip()]
                
                for j, estrofa in enumerate(estrofas):
                    versos = [v.strip() for v in estrofa.split('\n') if v.strip()]
                    
                    for verso in versos:
                        if verso:
                            story.append(Paragraph(verso, self.styles['VersoPoesia']))
                    
                    if j < len(estrofas) - 1:
                        story.append(Spacer(1, 15))
                
                # Separador entre poemas
                if i < len(lista_poemas):
                    story.append(PageBreak())
            
            doc.build(story)
            buffer.seek(0)
            return buffer.getvalue()
            
        except Exception as e:
            print(f"Error generando antología PDF: {e}")
            return None
    
    def obtener_formatos_disponibles(self):
        """Retorna lista de formatos de exportación disponibles"""
        return {
            'pdf': {
                'nombre': 'PDF Elegante',
                'descripcion': 'Documento PDF con formato profesional',
                'extension': '.pdf',
                'mime_type': 'application/pdf'
            },
            'html': {
                'nombre': 'HTML Estilizado',
                'descripcion': 'Página web con estilos CSS',
                'extension': '.html',
                'mime_type': 'text/html'
            },
            'txt': {
                'nombre': 'Texto Plano',
                'descripcion': 'Archivo de texto simple',
                'extension': '.txt',
                'mime_type': 'text/plain'
            },
            'json': {
                'nombre': 'JSON Estructurado',
                'descripcion': 'Datos estructurados en formato JSON',
                'extension': '.json',
                'mime_type': 'application/json'
            },
            'markdown': {
                'nombre': 'Markdown',
                'descripcion': 'Formato Markdown para documentación',
                'extension': '.md',
                'mime_type': 'text/markdown'
            },
            'csv': {
                'nombre': 'CSV Análisis',
                'descripcion': 'Hoja de cálculo con análisis métrico',
                'extension': '.csv',
                'mime_type': 'text/csv'
            }
        }