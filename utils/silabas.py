import re

class ContadorSilabas:
    def __init__(self):
        # Vocales y consonantes
        self.vocales = 'aeiouáéíóúü'
        self.consonantes = 'bcdfghjklmnñpqrstvwxyz'
        
        # Diptongos y triptongos
        self.diptongos_crecientes = ['ia', 'ie', 'io', 'iu', 'ua', 'ue', 'ui', 'uo']
        self.diptongos_decrecientes = ['ai', 'au', 'ei', 'eu', 'oi', 'ou']
        self.diptongos = self.diptongos_crecientes + self.diptongos_decrecientes
        
        self.triptongos = ['iau', 'iei', 'uai', 'uei', 'uou', 'iou']
        
        # Hiatos (combinaciones que se separan)
        self.hiatos_acentuados = [
            'aá', 'aé', 'aí', 'aó', 'aú',
            'eá', 'eé', 'eí', 'eó', 'eú', 
            'iá', 'ié', 'ií', 'ió', 'iú',
            'oá', 'oé', 'oí', 'oó', 'oú',
            'uá', 'ué', 'uí', 'uó', 'uú'
        ]
        
        # Consonantes que pueden formar grupos consonánticos
        self.grupos_consonanticos = [
            'bl', 'br', 'cl', 'cr', 'dr', 'fl', 'fr', 'gl', 'gr',
            'pl', 'pr', 'tr', 'ch', 'll', 'rr'
        ]
        
        # Palabras comunes con acentuación especial
        self.palabras_especiales = {
            'país': 2, 'raíz': 2, 'maíz': 2, 'baúl': 2,
            'río': 2, 'frío': 2, 'día': 2, 'guía': 2,
            'había': 3, 'tenía': 3, 'quería': 3, 'podía': 3,
            'continúa': 4, 'evalúa': 4, 'actúa': 3
        }
    
    def limpiar_palabra(self, palabra):
        """Limpia la palabra de signos de puntuación manteniendo acentos"""
        palabra = re.sub(r'[^\w\sáéíóúüñ]', '', palabra.lower())
        return palabra.strip()
    
    def es_vocal(self, letra):
        """Verifica si una letra es vocal"""
        return letra.lower() in self.vocales
    
    def es_vocal_tonica(self, letra):
        """Verifica si una letra es vocal tónica"""
        return letra.lower() in 'áéíóú'
    
    def es_vocal_cerrada(self, letra):
        """Verifica si es vocal cerrada (i, u)"""
        return letra.lower() in 'iuíú'
    
    def es_vocal_abierta(self, letra):
        """Verifica si es vocal abierta (a, e, o)"""
        return letra.lower() in 'aeoáéó'
    
    def detectar_acentuacion(self, palabra):
        """Detecta si la palabra es aguda, llana o esdrújula"""
        palabra_limpia = self.limpiar_palabra(palabra)
        
        # Buscar vocal tónica
        posicion_tonica = -1
        for i, letra in enumerate(palabra_limpia):
            if self.es_vocal_tonica(letra):
                posicion_tonica = i
                break
        
        # Si no hay tilde, aplicar reglas generales
        if posicion_tonica == -1:
            # Palabras terminadas en vocal, n, s son llanas
            ultima_letra = palabra_limpia[-1] if palabra_limpia else ''
            if ultima_letra in 'aeiounsáéíóú':
                return 'llana'
            else:
                return 'aguda'
        
        # Contar sílabas hasta la tónica
        silabas_antes = self.contar_silabas(palabra_limpia[:posicion_tonica + 1])
        silabas_totales = self.contar_silabas(palabra_limpia)
        posicion_desde_final = silabas_totales - silabas_antes + 1
        
        if posicion_desde_final == 1:
            return 'aguda'
        elif posicion_desde_final == 2:
            return 'llana'
        elif posicion_desde_final >= 3:
            return 'esdrujula'
        
        return 'llana'  # Por defecto
    
    def aplicar_sinalefa(self, palabras):
        """Aplica la sinalefa entre palabras"""
        if len(palabras) < 2:
            return sum(self.contar_silabas(p) for p in palabras)
        
        silabas_total = 0
        sinalefas = 0
        
        for i in range(len(palabras)):
            silabas_palabra = self.contar_silabas(palabras[i])
            silabas_total += silabas_palabra
            
            # Verificar sinalefa con la siguiente palabra
            if i < len(palabras) - 1:
                palabra_actual = self.limpiar_palabra(palabras[i])
                palabra_siguiente = self.limpiar_palabra(palabras[i + 1])
                
                if palabra_actual and palabra_siguiente:
                    ultima_letra = palabra_actual[-1]
                    primera_letra = palabra_siguiente[0]
                    
                    # Sinalefa: vocal final + vocal inicial
                    if self.es_vocal(ultima_letra) and self.es_vocal(primera_letra):
                        # Verificar excepciones (vocal tónica + vocal)
                        if not (self.es_vocal_tonica(ultima_letra) and self.es_vocal_abierta(primera_letra)):
                            sinalefas += 1
        
        return silabas_total - sinalefas
    
    def detectar_diptongos_triptongos(self, palabra):
        """Detecta diptongos y triptongos en una palabra"""
        palabra = palabra.lower()
        posiciones_especiales = []
        
        # Buscar triptongos primero
        for triptongo in self.triptongos:
            pos = 0
            while pos <= len(palabra) - 3:
                if palabra[pos:pos+3] == triptongo:
                    posiciones_especiales.append(('triptongo', pos, pos+2))
                    pos += 3
                else:
                    pos += 1
        
        # Buscar diptongos (evitando posiciones de triptongos)
        for diptongo in self.diptongos:
            pos = 0
            while pos <= len(palabra) - 2:
                if palabra[pos:pos+2] == diptongo:
                    # Verificar que no esté dentro de un triptongo
                    en_triptongo = any(
                        start <= pos <= end or start <= pos+1 <= end
                        for tipo, start, end in posiciones_especiales
                        if tipo == 'triptongo'
                    )
                    if not en_triptongo:
                        posiciones_especiales.append(('diptongo', pos, pos+1))
                    pos += 2
                else:
                    pos += 1
        
        # Detectar hiatos
        for hiato in self.hiatos_acentuados:
            pos = 0
            while pos <= len(palabra) - 2:
                if palabra[pos:pos+2] == hiato:
                    posiciones_especiales.append(('hiato', pos, pos+1))
                    pos += 2
                else:
                    pos += 1
        
        return posiciones_especiales
    
    def contar_silabas(self, palabra):
        """Cuenta las sílabas de una palabra"""
        if not palabra:
            return 0
        
        palabra_original = palabra
        palabra = self.limpiar_palabra(palabra)
        
        if not palabra:
            return 0
        
        # Verificar palabras especiales
        if palabra in self.palabras_especiales:
            return self.palabras_especiales[palabra]
        
        # Detectar patrones especiales
        patrones_especiales = self.detectar_diptongos_triptongos(palabra)
        
        # Contar núcleos silábicos
        silabas = 0
        i = 0
        
        while i < len(palabra):
            if self.es_vocal(palabra[i]):
                # Verificar si es parte de un patrón especial
                en_patron = False
                
                for tipo, inicio, fin in patrones_especiales:
                    if inicio <= i <= fin:
                        if tipo in ['triptongo', 'diptongo']:
                            silabas += 1
                            i = fin + 1
                            en_patron = True
                            break
                        elif tipo == 'hiato':
                            # Cada vocal del hiato cuenta como sílaba separada
                            silabas += 1
                            i += 1
                            en_patron = True
                            break
                
                if not en_patron:
                    # Vocal aislada
                    silabas += 1
                    i += 1
            else:
                i += 1
        
        return max(1, silabas)
    
    def contar_silabas_verso(self, verso):
        """Cuenta las sílabas de un verso aplicando reglas métricas"""
        if not verso:
            return 0
        
        # Limpiar y dividir en palabras
        palabras = verso.split()
        if not palabras:
            return 0
        
        # Contar sílabas con sinalefa
        silabas_con_sinalefa = self.aplicar_sinalefa(palabras)
        
        # Aplicar regla del final del verso
        ultima_palabra = self.limpiar_palabra(palabras[-1])
        if ultima_palabra:
            acentuacion = self.detectar_acentuacion(ultima_palabra)
            
            if acentuacion == 'aguda':
                silabas_con_sinalefa += 1  # Se añade una sílaba
            elif acentuacion == 'esdrujula':
                silabas_con_sinalefa -= 1  # Se quita una sílaba
            # Las llanas no cambian
        
        return max(1, silabas_con_sinalefa)
    
    def analizar_palabra_detallado(self, palabra):
        """Análisis detallado de una palabra"""
        palabra_limpia = self.limpiar_palabra(palabra)
        
        if not palabra_limpia:
            return {
                'palabra': palabra,
                'silabas': 0,
                'acentuacion': 'indefinida',
                'patrones': [],
                'division_silabica': []
            }
        
        silabas = self.contar_silabas(palabra_limpia)
        acentuacion = self.detectar_acentuacion(palabra_limpia)
        patrones = self.detectar_diptongos_triptongos(palabra_limpia)
        division = self.dividir_en_silabas(palabra_limpia)
        
        return {
            'palabra': palabra,
            'palabra_limpia': palabra_limpia,
            'silabas': silabas,
            'acentuacion': acentuacion,
            'patrones': patrones,
            'division_silabica': division
        }
    
    def dividir_en_silabas(self, palabra):
        """Divide una palabra en sílabas"""
        if not palabra:
            return []
        
        palabra = self.limpiar_palabra(palabra)
        patrones = self.detectar_diptongos_triptongos(palabra)
        
        silabas = []
        i = 0
        silaba_actual = ""
        
        while i < len(palabra):
            letra = palabra[i]
            
            # Verificar si está en un patrón especial
            en_patron = False
            for tipo, inicio, fin in patrones:
                if inicio <= i <= fin:
                    if tipo in ['diptongo', 'triptongo']:
                        # Añadir todo el patrón a la sílaba actual
                        silaba_actual += palabra[inicio:fin+1]
                        i = fin + 1
                        en_patron = True
                        break
                    elif tipo == 'hiato':
                        # Separar en sílabas diferentes
                        if silaba_actual or i == inicio:
                            silaba_actual += letra
                            silabas.append(silaba_actual)
                            silaba_actual = ""
                        i += 1
                        en_patron = True
                        break
            
            if not en_patron:
                silaba_actual += letra
                
                # Reglas de división silábica
                if i < len(palabra) - 1:
                    siguiente = palabra[i + 1]
                    
                    # Si vocal seguida de consonante, posible corte
                    if self.es_vocal(letra) and not self.es_vocal(siguiente):
                        # Mirar adelante para decidir dónde cortar
                        j = i + 1
                        consonantes = ""
                        
                        while j < len(palabra) and not self.es_vocal(palabra[j]):
                            consonantes += palabra[j]
                            j += 1
                        
                        # Aplicar reglas de división
                        if len(consonantes) == 1:
                            # Una consonante va con la vocal siguiente
                            pass
                        elif len(consonantes) == 2:
                            # Dos consonantes: verificar si forman grupo
                            if consonantes in self.grupos_consonanticos:
                                # Grupo consonántico va junto
                                pass
                            else:
                                # Separar consonantes
                                silaba_actual += consonantes[0]
                                silabas.append(silaba_actual)
                                silaba_actual = ""
                                i += 1
                        else:
                            # Tres o más consonantes: primera va con vocal anterior
                            silaba_actual += consonantes[0]
                            silabas.append(silaba_actual)
                            silaba_actual = ""
                            i += 1
                
                i += 1
        
        if silaba_actual:
            silabas.append(silaba_actual)
        
        return silabas if silabas else [palabra]
    
    def analizar_verso_completo(self, verso):
        """Análisis completo de un verso"""
        palabras = verso.split()
        analisis_palabras = []
        
        for palabra in palabras:
            analisis = self.analizar_palabra_detallado(palabra)
            analisis_palabras.append(analisis)
        
        silabas_metricas = self.contar_silabas_verso(verso)
        silabas_gramaticales = sum(self.contar_silabas(p) for p in palabras)
        sinalefas = silabas_gramaticales - silabas_metricas
        
        # Ajuste por acentuación final
        if palabras:
            ultima_palabra = self.limpiar_palabra(palabras[-1])
            acentuacion_final = self.detectar_acentuacion(ultima_palabra)
            
            if acentuacion_final == 'aguda':
                sinalefas -= 1  # Se añadió una sílaba
            elif acentuacion_final == 'esdrujula':
                sinalefas += 1  # Se quitó una sílaba
        
        return {
            'verso': verso,
            'palabras_analizadas': analisis_palabras,
            'silabas_metricas': silabas_metricas,
            'silabas_gramaticales': silabas_gramaticales,
            'sinalefas_aplicadas': max(0, sinalefas),
            'acentuacion_final': acentuacion_final if palabras else 'indefinida'
        }