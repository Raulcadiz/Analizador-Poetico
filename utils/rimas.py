import re
from collections import Counter

class DetectorRimas:
    def __init__(self):
        self.vocales = 'aeiouáéíóúü'
        
        # Patrones de rima conocidos
        self.patrones_clasicos = {
            'ABAB': 'Rima cruzada',
            'AABB': 'Rima pareada',
            'ABBA': 'Rima abrazada',
            'AAAA': 'Rima monorrima',
            'ABCB': 'Rima asonante en pares',
            'ABAB CDCD EFEF GG': 'Soneto shakesperiano',
            'ABBA ABBA CDC DCD': 'Soneto petrarquista',
            'ABAB ABAB CDC DCD': 'Soneto francés'
        }
        
        # Terminaciones comunes para rimas
        self.terminaciones_comunes = {
            'amor': ['dolor', 'honor', 'temor', 'calor', 'clamor', 'fulgor'],
            'vida': ['herida', 'partida', 'querida', 'medida', 'salida'],
            'alma': ['calma', 'palma', 'balma'],
            'muerte': ['suerte', 'fuerte'],
            'cielo': ['vuelo', 'suelo', 'anhelo', 'desvelo'],
            'mar': ['lugar', 'hogar', 'pesar', 'brillar'],
            'sol': ['español', 'caracol', 'farol'],
            'luna': ['fortuna', 'ninguna', 'laguna']
        }
    
    def extraer_terminacion_rima(self, verso):
        """Extrae la terminación del verso para análisis de rima"""
        # Limpiar el verso
        verso_limpio = re.sub(r'[^\w\sáéíóúüñ]', '', verso.lower()).strip()
        
        if not verso_limpio:
            return ""
        
        palabras = verso_limpio.split()
        if not palabras:
            return ""
        
        ultima_palabra = palabras[-1]
        
        # Extraer terminación desde la última vocal tónica
        terminacion = self._extraer_desde_tonica(ultima_palabra)
        
        return terminacion
    
    def _extraer_desde_tonica(self, palabra):
        """Extrae la terminación desde la vocal tónica"""
        # Buscar vocal acentuada
        for i, letra in enumerate(palabra):
            if letra in 'áéíóú':
                return palabra[i:]
        
        # Si no hay tilde, aplicar reglas de acentuación
        if palabra.endswith(('a', 'e', 'i', 'o', 'u', 'n', 's')):
            # Palabra llana - acentuar penúltima sílaba
            vocales_pos = [i for i, c in enumerate(palabra) if c in self.vocales]
            if len(vocales_pos) >= 2:
                return palabra[vocales_pos[-2]:]
            elif len(vocales_pos) == 1:
                return palabra[vocales_pos[0]:]
        else:
            # Palabra aguda - acentuar última sílaba
            vocales_pos = [i for i, c in enumerate(palabra) if c in self.vocales]
            if vocales_pos:
                return palabra[vocales_pos[-1]:]
        
        return palabra[-3:] if len(palabra) >= 3 else palabra
    
    def son_rimas_consonantes(self, terminacion1, terminacion2):
        """Verifica si dos terminaciones forman rima consonante"""
        if not terminacion1 or not terminacion2:
            return False
        
        # Normalizar las terminaciones
        term1 = self._normalizar_terminacion(terminacion1)
        term2 = self._normalizar_terminacion(terminacion2)
        
        return term1 == term2 and len(term1) >= 2
    
    def son_rimas_asonantes(self, terminacion1, terminacion2):
        """Verifica si dos terminaciones forman rima asonante"""
        if not terminacion1 or not terminacion2:
            return False
        
        # Extraer solo las vocales
        vocales1 = ''.join(c for c in terminacion1 if c in self.vocales)
        vocales2 = ''.join(c for c in terminacion2 if c in self.vocales)
        
        # Normalizar vocales acentuadas
        vocales1 = self._normalizar_vocales(vocales1)
        vocales2 = self._normalizar_vocales(vocales2)
        
        return vocales1 == vocales2 and len(vocales1) >= 2
    
    def _normalizar_terminacion(self, terminacion):
        """Normaliza una terminación para comparación"""
        # Convertir acentos a versiones sin acento para rima consonante
        normalizacion = {
            'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u'
        }
        
        resultado = ""
        for char in terminacion.lower():
            resultado += normalizacion.get(char, char)
        
        return resultado
    
    def _normalizar_vocales(self, vocales):
        """Normaliza vocales para rima asonante"""
        normalizacion = {
            'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u'
        }
        
        resultado = ""
        for char in vocales.lower():
            resultado += normalizacion.get(char, char)
        
        return resultado
    
    def detectar_esquema(self, versos):
        """Detecta el esquema de rimas de una lista de versos"""
        if not versos:
            return []
        
        terminaciones = [self.extraer_terminacion_rima(verso) for verso in versos]
        esquema = []
        grupos_rima = {}
        letra_actual = 'A'
        
        for terminacion in terminaciones:
            if not terminacion:
                esquema.append('-')  # Verso sin rima
                continue
            
            # Buscar si rima con algún grupo existente
            grupo_encontrado = None
            
            for grupo, termins in grupos_rima.items():
                for term_existente in termins:
                    if (self.son_rimas_consonantes(terminacion, term_existente) or 
                        self.son_rimas_asonantes(terminacion, term_existente)):
                        grupo_encontrado = grupo
                        break
                if grupo_encontrado:
                    break
            
            if grupo_encontrado:
                # Añadir a grupo existente
                grupos_rima[grupo_encontrado].append(terminacion)
                esquema.append(grupo_encontrado)
            else:
                # Crear nuevo grupo
                grupos_rima[letra_actual] = [terminacion]
                esquema.append(letra_actual)
                letra_actual = chr(ord(letra_actual) + 1)
        
        return esquema
    
    def clasificar_rima(self, esquema):
        """Clasifica el tipo de rima basado en el esquema"""
        if not esquema:
            return "Sin rima"
        
        esquema_str = ''.join(esquema)
        
        # Verificar patrones clásicos conocidos
        for patron, nombre in self.patrones_clasicos.items():
            if patron in esquema_str or esquema_str.startswith(patron[:4]):
                return nombre
        
        # Análisis basado en estructura
        if len(set(esquema)) == 1 and esquema[0] != '-':
            return "Monorrima"
        
        if len(esquema) >= 4:
            # Verificar patrones de 4 versos
            cuarteto = esquema[:4]
            if cuarteto == ['A', 'B', 'A', 'B']:
                return "Rima cruzada (ABAB)"
            elif cuarteto == ['A', 'A', 'B', 'B']:
                return "Rima pareada (AABB)"
            elif cuarteto == ['A', 'B', 'B', 'A']:
                return "Rima abrazada (ABBA)"
        
        # Análisis de regularidad
        parejas = sum(1 for i in range(0, len(esquema)-1, 2) 
                     if i+1 < len(esquema) and esquema[i] == esquema[i+1])
        
        if parejas > len(esquema) // 3:
            return "Rima principalmente pareada"
        
        # Verificar rima alternada
        alternadas = sum(1 for i in range(len(esquema)-2) 
                        if esquema[i] == esquema[i+2])
        
        if alternadas > len(esquema) // 3:
            return "Rima principalmente alternada"
        
        return "Rima libre"
    
    def analizar_rimas_detallado(self, versos):
        """Análisis detallado de las rimas"""
        if not versos:
            return {"error": "No hay versos para analizar"}
        
        terminaciones = []
        analisis_versos = []
        
        for i, verso in enumerate(versos):
            terminacion = self.extraer_terminacion_rima(verso)
            terminaciones.append(terminacion)
            
            analisis_versos.append({
                'numero': i + 1,
                'verso': verso,
                'terminacion': terminacion,
                'palabra_final': verso.split()[-1] if verso.split() else ""
            })
        
        esquema = self.detectar_esquema(versos)
        tipo_rima = self.clasificar_rima(esquema)
        
        # Análizar calidad de las rimas
        rimas_consonantes = 0
        rimas_asonantes = 0
        
        for i in range(len(terminaciones)):
            for j in range(i+1, len(terminaciones)):
                if esquema[i] == esquema[j] and esquema[i] != '-':
                    if self.son_rimas_consonantes(terminaciones[i], terminaciones[j]):
                        rimas_consonantes += 1
                    elif self.son_rimas_asonantes(terminaciones[i], terminaciones[j]):
                        rimas_asonantes += 1
        
        # Detectar grupos de rima
        grupos_rima = {}
        for i, letra in enumerate(esquema):
            if letra != '-':
                if letra not in grupos_rima:
                    grupos_rima[letra] = []
                grupos_rima[letra].append({
                    'verso_num': i + 1,
                    'verso': versos[i],
                    'terminacion': terminaciones[i]
                })
        
        return {
            'esquema_rima': esquema,
            'tipo_rima': tipo_rima,
            'analisis_versos': analisis_versos,
            'grupos_rima': grupos_rima,
            'estadisticas': {
                'total_versos': len(versos),
                'versos_con_rima': len([e for e in esquema if e != '-']),
                'grupos_diferentes': len(set(esquema) - {'-'}),
                'rimas_consonantes': rimas_consonantes,
                'rimas_asonantes': rimas_asonantes,
                'porcentaje_rima': (len([e for e in esquema if e != '-']) / len(esquema)) * 100
            }
        }
    
    def sugerir_rimas(self, palabra):
        """Sugiere palabras que rimen con la palabra dada"""
        terminacion = self.extraer_terminacion_rima(palabra)
        
        if not terminacion:
            return []
        
        sugerencias = []
        
        # Buscar en terminaciones conocidas
        for base, rimas in self.terminaciones_comunes.items():
            if self.son_rimas_consonantes(terminacion, self.extraer_terminacion_rima(base)):
                sugerencias.extend(rimas[:5])  # Máximo 5 por grupo
        
        # Generar rimas automáticas basadas en patrones
        rimas_automaticas = self._generar_rimas_automaticas(terminacion)
        sugerencias.extend(rimas_automaticas)
        
        # Eliminar duplicados y la palabra original
        sugerencias = list(set(sugerencias))
        palabra_limpia = re.sub(r'[^\w\sáéíóúüñ]', '', palabra.lower()).strip()
        
        if palabra_limpia in sugerencias:
            sugerencias.remove(palabra_limpia)
        
        return sugerencias[:20]  # Máximo 20 sugerencias
    
    def _generar_rimas_automaticas(self, terminacion):
        """Genera rimas automáticas basadas en patrones comunes"""
        rimas = []
        
        # Patrones de sufijos comunes en español
        sufijos_comunes = {
            'ar': ['lugar', 'hogar', 'brillar', 'caminar', 'soñar'],
            'er': ['querer', 'poder', 'saber', 'tener', 'volver'],
            'ir': ['vivir', 'sentir', 'morir', 'partir', 'dormir'],
            'ón': ['corazón', 'pasión', 'razón', 'canción', 'emoción'],
            'ad': ['verdad', 'libertad', 'felicidad', 'bondad', 'eternidad'],
            'or': ['amor', 'dolor', 'honor', 'calor', 'fulgor'],
            'ida': ['vida', 'herida', 'querida', 'partida', 'medida'],
            'eza': ['belleza', 'tristeza', 'pureza', 'grandeza', 'certeza']
        }
        
        # Buscar patrones que coincidan
        for sufijo, palabras in sufijos_comunes.items():
            if terminacion.endswith(sufijo):
                rimas.extend(palabras)
        
        return rimas[:10]
    
    def evaluar_calidad_rima(self, palabra1, palabra2):
        """Evalúa la calidad de la rima entre dos palabras"""
        term1 = self.extraer_terminacion_rima(palabra1)
        term2 = self.extraer_terminacion_rima(palabra2)
        
        if self.son_rimas_consonantes(term1, term2):
            # Evaluar consonante por longitud de coincidencia
            coincidencia = 0
            min_len = min(len(term1), len(term2))
            
            for i in range(min_len):
                if term1[-(i+1)] == term2[-(i+1)]:
                    coincidencia += 1
                else:
                    break
            
            if coincidencia >= 3:
                return {"tipo": "Consonante rica", "puntuacion": 95 + coincidencia}
            elif coincidencia >= 2:
                return {"tipo": "Consonante", "puntuacion": 80 + coincidencia * 3}
            else:
                return {"tipo": "Consonante pobre", "puntuacion": 60}
        
        elif self.son_rimas_asonantes(term1, term2):
            vocales1 = ''.join(c for c in term1 if c in self.vocales)
            vocales2 = ''.join(c for c in term2 if c in self.vocales)
            
            if len(vocales1) >= 3:
                return {"tipo": "Asonante rica", "puntuacion": 70}
            elif len(vocales1) == 2:
                return {"tipo": "Asonante", "puntuacion": 60}
            else:
                return {"tipo": "Asonante pobre", "puntuacion": 40}
        
        else:
            return {"tipo": "Sin rima", "puntuacion": 0}
    
    def detectar_licencias_poeticas(self, versos):
        """Detecta licencias poéticas utilizadas en la rima"""
        licencias = []
        
        for i, verso in enumerate(versos):
            # Detectar sinalefas que afecten la rima
            palabras = verso.split()
            if len(palabras) >= 2:
                for j in range(len(palabras) - 1):
                    palabra_actual = palabras[j]
                    palabra_siguiente = palabras[j + 1]
                    
                    if (palabra_actual.endswith(tuple(self.vocales)) and 
                        palabra_siguiente.startswith(tuple(self.vocales))):
                        licencias.append({
                            'tipo': 'Sinalefa',
                            'verso': i + 1,
                            'descripcion': f"'{palabra_actual} {palabra_siguiente}'"
                        })
            
            # Detectar hiatos forzados
            if 'poesía' in verso.lower() or 'día' in verso.lower():
                licencias.append({
                    'tipo': 'Hiato',
                    'verso': i + 1,
                    'descripcion': 'Separación de vocales que normalmente formarían diptongo'
                })
        
        return licencias