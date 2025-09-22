import re
from collections import Counter
from .silabas import ContadorSilabas

class AnalizadorMetrico:
    def __init__(self):
        self.contador_silabas = ContadorSilabas()
        
        # Definiciones métricas clásicas españolas
        self.metros_clasicos = {
            4: "Tetrasílabo",
            5: "Pentasílabo", 
            6: "Hexasílabo",
            7: "Heptasílabo",
            8: "Octosílabo",
            9: "Eneasílabo",
            10: "Decasílabo",
            11: "Endecasílabo",
            12: "Dodecasílabo",
            13: "Tridecasílabo",
            14: "Alejandrino",
            15: "Pentadecasílabo",
            16: "Hexadecasílabo"
        }
        
        # Patrones rítmicos comunes
        self.patrones_ritmo = {
            'yámbico': [2, 4, 6, 8, 10],  # Átona-tónica
            'trocaico': [1, 3, 5, 7, 9],  # Tónica-átona
            'dactílico': [1, 4, 7, 10],   # Tónica-átona-átona
            'anapéstico': [3, 6, 9, 12],  # Átona-átona-tónica
            'anfíbraco': [2, 5, 8, 11]    # Átona-tónica-átona
        }
    
    def clasificar_metro(self, silabas):
        """Clasifica el metro según el número de sílabas"""
        if silabas in self.metros_clasicos:
            return self.metros_clasicos[silabas]
        elif silabas < 4:
            return "Verso de arte menor (irregular)"
        elif silabas <= 8:
            return f"Verso de arte menor ({silabas} sílabas)"
        else:
            return f"Verso de arte mayor ({silabas} sílabas)"
    
    def detectar_metro_dominante(self, lista_silabas):
        """Detecta el metro más común en una serie de versos"""
        if not lista_silabas:
            return "Indeterminado"
        
        contador = Counter(lista_silabas)
        metro_comun = contador.most_common(1)[0][0]
        
        # Verificar si hay regularidad mínima
        frecuencia = contador[metro_comun] / len(lista_silabas)
        
        if frecuencia >= 0.6:  # 60% o más de los versos
            return f"{self.clasificar_metro(metro_comun)} (regular)"
        elif frecuencia >= 0.4:  # 40-59% de los versos
            return f"{self.clasificar_metro(metro_comun)} (semi-regular)"
        else:
            return "Verso libre (métrica irregular)"
    
    def calcular_regularidad(self, lista_silabas):
        """Calcula el grado de regularidad métrica"""
        if len(lista_silabas) < 2:
            return "Insuficientes versos para análisis"
        
        contador = Counter(lista_silabas)
        metro_principal = contador.most_common(1)[0][0]
        frecuencia_principal = contador[metro_principal] / len(lista_silabas)
        
        if frecuencia_principal >= 0.8:
            return "Muy regular"
        elif frecuencia_principal >= 0.6:
            return "Regular"
        elif frecuencia_principal >= 0.4:
            return "Semi-regular"
        else:
            return "Irregular (verso libre)"
    
    def detectar_acentos(self, verso):
        """Detecta posibles posiciones acentuales en un verso"""
        palabras = verso.lower().split()
        acentos = []
        posicion = 0
        
        for palabra in palabras:
            silabas_palabra = self.contador_silabas.contar_silabas(palabra)
            
            # Detectar acento principal de la palabra
            if self._es_aguda(palabra):
                acento_palabra = silabas_palabra - 1
            elif self._es_esdrujula(palabra):
                acento_palabra = silabas_palabra - 3
            else:  # Llana
                acento_palabra = silabas_palabra - 2
            
            if acento_palabra >= 0:
                acentos.append(posicion + acento_palabra)
            
            posicion += silabas_palabra
        
        return acentos
    
    def analizar_ritmo(self, versos):
        """Analiza el patrón rítmico de los versos"""
        if not versos:
            return {"tipo": "Indeterminado", "regularidad": "Sin datos", "acentos_comunes": []}
        
        todos_acentos = []
        for verso in versos:
            acentos = self.detectar_acentos(verso)
            todos_acentos.extend(acentos)
        
        if not todos_acentos:
            return {"tipo": "Indeterminado", "regularidad": "Sin acentos detectados", "acentos_comunes": []}
        
        # Encontrar posiciones acentuales más comunes
        contador_acentos = Counter(todos_acentos)
        acentos_comunes = [pos for pos, freq in contador_acentos.most_common(5)]
        
        # Detectar patrón rítmico
        ritmo_detectado = self._detectar_patron_ritmico(acentos_comunes)
        
        # Calcular regularidad rítmica
        total_versos = len(versos)
        versos_con_patron = sum(1 for verso in versos if self._verso_sigue_patron(verso, ritmo_detectado))
        regularidad_ritmica = f"{(versos_con_patron/total_versos)*100:.1f}% de los versos"
        
        return {
            "tipo": ritmo_detectado,
            "regularidad": regularidad_ritmica,
            "acentos_comunes": acentos_comunes[:3]  # Top 3
        }
    
    def _es_aguda(self, palabra):
        """Determina si una palabra es aguda"""
        # Simplificado: palabras que terminan en vocal, n, s son llanas por defecto
        # Las que terminan en consonante (excepto n,s) son agudas
        palabra = palabra.lower().strip('.,!?;:"()[]')
        if not palabra:
            return False
        
        ultima_letra = palabra[-1]
        if ultima_letra in 'aeiouáéíóúns':
            return False  # Probablemente llana
        return True  # Probablemente aguda
    
    def _es_esdrujula(self, palabra):
        """Detecta palabras esdrújulas por patrones comunes"""
        palabra = palabra.lower()
        
        # Patrones comunes de esdrújulas
        patrones_esdrujulas = [
            r'.*[áéíóú].*[aeiou].*[aeiou]$',  # Vocal acentuada seguida de dos átonas
            r'.*ico$', r'.*ica$',  # -ico, -ica
            r'.*ulo$', r'.*ula$',  # -ulo, -ula
            r'.*ido$', r'.*ida$'   # -ido, -ida (algunos casos)
        ]
        
        for patron in patrones_esdrujulas:
            if re.match(patron, palabra):
                return True
        
        return False
    
    def _detectar_patron_ritmico(self, acentos_comunes):
        """Detecta el patrón rítmico basado en acentos comunes"""
        if not acentos_comunes:
            return "Indeterminado"
        
        # Comparar con patrones conocidos
        mejor_coincidencia = ""
        max_coincidencias = 0
        
        for nombre_patron, posiciones in self.patrones_ritmo.items():
            coincidencias = len(set(acentos_comunes[:5]) & set(posiciones))
            if coincidencias > max_coincidencias:
                max_coincidencias = coincidencias
                mejor_coincidencia = nombre_patron
        
        if max_coincidencias >= 2:
            return f"Tendencia {mejor_coincidencia}"
        else:
            return "Ritmo libre"
    
    def _verso_sigue_patron(self, verso, patron):
        """Verifica si un verso sigue un patrón rítmico específico"""
        if "libre" in patron.lower() or "indeterminado" in patron.lower():
            return True  # Todos los versos "siguen" un patrón libre
        
        acentos_verso = self.detectar_acentos(verso)
        
        # Simplificado: si tiene al menos 2 acentos en posiciones esperadas
        for nombre_patron, posiciones in self.patrones_ritmo.items():
            if nombre_patron in patron.lower():
                coincidencias = len(set(acentos_verso) & set(posiciones))
                return coincidencias >= 2
        
        return False
    
    def analisis_completo(self, texto):
        """Realiza un análisis métrico completo del texto"""
        versos = [v.strip() for v in texto.split('\n') if v.strip()]
        
        if not versos:
            return {"error": "No se encontraron versos válidos"}
        
        # Análisis por verso
        analisis_versos = []
        silabas_total = []
        
        for i, verso in enumerate(versos, 1):
            silabas = self.contador_silabas.contar_silabas_verso(verso)
            metro = self.clasificar_metro(silabas)
            acentos = self.detectar_acentos(verso)
            
            analisis_versos.append({
                'numero': i,
                'texto': verso,
                'silabas': silabas,
                'metro': metro,
                'acentos': acentos
            })
            
            silabas_total.append(silabas)
        
        # Análisis global
        metro_dominante = self.detectar_metro_dominante(silabas_total)
        regularidad = self.calcular_regularidad(silabas_total)
        ritmo = self.analizar_ritmo(versos)
        
        return {
            'versos_analizados': analisis_versos,
            'metro_dominante': metro_dominante,
            'regularidad_metrica': regularidad,
            'analisis_ritmico': ritmo,
            'estadisticas': {
                'total_versos': len(versos),
                'total_silabas': sum(silabas_total),
                'promedio_silabas': sum(silabas_total) / len(silabas_total),
                'metro_mas_comun': Counter(silabas_total).most_common(1)[0] if silabas_total else None
            }
        }