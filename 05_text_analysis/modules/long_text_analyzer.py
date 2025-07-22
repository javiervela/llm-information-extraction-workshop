# long_text_analyzer.py
"""
Módulo para análisis de textos largos con Ollama
Extrae palabras clave y genera resúmenes pormenorizados de transcripciones y documentos largos
"""

import requests
import json
import re
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import argparse
import sys
from pathlib import Path

@dataclass
class TextAnalysis:
    """Estructura para almacenar los resultados del análisis"""
    keywords: List[str]
    summary: str
    key_topics: List[str]
    sentiment: str
    word_count: int
    reading_time: int
    speakers: List[str]  # Para transcripciones con múltiples hablantes

class LongTextAnalyzer:
    """Analizador de textos largos usando Ollama"""
    
    def __init__(self, model_name: str = "llama3.1", ollama_url: str = "http://localhost:11434"):
        self.model_name = model_name
        self.ollama_url = ollama_url
        self.max_chunk_size = 4000  # Tamaño máximo por chunk para evitar límites de contexto
        
    def _call_ollama(self, prompt: str, system_prompt: str = "") -> str:
        """Realiza una llamada a Ollama y retorna la respuesta"""
        try:
            payload = {
                "model": self.model_name,
                "prompt": prompt,
                "stream": False,
                "system": system_prompt,
                "options": {
                    "temperature": 0.1,
                    "top_p": 0.9,
                    "num_ctx": 8192
                }
            }
            
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json=payload,
                timeout=120
            )
            response.raise_for_status()
            return response.json()["response"].strip()
        
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error conectando con Ollama: {e}")
    
    def _chunk_text(self, text: str) -> List[str]:
        """Divide el texto en chunks manejables"""
        # Divide por párrafos primero
        paragraphs = text.split('\n\n')
        chunks = []
        current_chunk = ""
        
        for paragraph in paragraphs:
            # Si el párrafo solo es muy largo, lo dividimos por oraciones
            if len(paragraph) > self.max_chunk_size:
                sentences = re.split(r'[.!?]+', paragraph)
                for sentence in sentences:
                    if len(current_chunk + sentence) > self.max_chunk_size:
                        if current_chunk:
                            chunks.append(current_chunk.strip())
                            current_chunk = sentence
                        else:
                            # Si una sola oración es muy larga, la dividimos forzosamente
                            chunks.append(sentence[:self.max_chunk_size])
                    else:
                        current_chunk += sentence
            else:
                if len(current_chunk + paragraph) > self.max_chunk_size:
                    chunks.append(current_chunk.strip())
                    current_chunk = paragraph
                else:
                    current_chunk += "\n\n" + paragraph
        
        if current_chunk.strip():
            chunks.append(current_chunk.strip())
        
        return chunks
    
    def extract_keywords(self, text: str) -> List[str]:
        """Extrae palabras clave del texto"""
        chunks = self._chunk_text(text)
        all_keywords = []
        
        system_prompt = """Eres un experto en análisis de texto. Tu tarea es extraer las palabras clave más importantes y relevantes del texto proporcionado."""
        
        for chunk in chunks:
            prompt = f"""
            Analiza el siguiente texto y extrae las 10-15 palabras clave más importantes.
            
            INSTRUCCIONES:
            - Incluye tanto términos simples como frases clave
            - Prioriza conceptos, nombres propios, y temas centrales
            - Evita palabras vacías o muy genéricas
            - Presenta las palabras separadas por comas
            - No incluyas explicaciones adicionales
            
            TEXTO A ANALIZAR:
            {chunk}
            
            PALABRAS CLAVE:
            """
            
            response = self._call_ollama(prompt, system_prompt)
            chunk_keywords = [kw.strip() for kw in response.split(',')]
            all_keywords.extend(chunk_keywords)
        
        # Consolidar y filtrar keywords duplicadas
        unique_keywords = list(set(all_keywords))
        
        # Si tenemos muchas keywords, seleccionar las más relevantes
        if len(unique_keywords) > 20:
            consolidation_prompt = f"""
            De la siguiente lista de palabras clave, selecciona las 15-20 más importantes y relevantes para el texto:
            
            {', '.join(unique_keywords)}
            
            Presenta solo las palabras seleccionadas, separadas por comas:
            """
            
            response = self._call_ollama(consolidation_prompt, system_prompt)
            unique_keywords = [kw.strip() for kw in response.split(',')]
        
        return unique_keywords[:20]  # Limitar a máximo 20 keywords
    
    def generate_detailed_summary(self, text: str) -> str:
        """Genera un resumen detallado del texto"""
        chunks = self._chunk_text(text)
        chunk_summaries = []
        
        system_prompt = """Eres un experto en síntesis y análisis de contenido. Creas resúmenes detallados, estructurados y comprensivos."""
        
        # Generar resumen para cada chunk
        for i, chunk in enumerate(chunks):
            prompt = f"""
            Crea un resumen detallado del siguiente fragmento de texto (parte {i+1} de {len(chunks)}):
            
            INSTRUCCIONES:
            - Incluye los puntos más importantes y detalles relevantes
            - Mantén la estructura lógica del contenido
            - No omitas información crucial
            - Usa un estilo claro y profesional
            
            TEXTO:
            {chunk}
            
            RESUMEN DETALLADO:
            """
            
            chunk_summary = self._call_ollama(prompt, system_prompt)
            chunk_summaries.append(chunk_summary)
        
        # Consolidar todos los resúmenes
        if len(chunk_summaries) > 1:
            consolidation_prompt = f"""
            Consolida los siguientes resúmenes parciales en un resumen final cohesivo y bien estructurado:
            
            RESÚMENES PARCIALES:
            {' '.join([f"PARTE {i+1}: {summary}" for i, summary in enumerate(chunk_summaries)])}
            
            INSTRUCCIONES PARA EL RESUMEN FINAL:
            - Crea un resumen fluido y bien estructurado
            - Elimina redundancias entre las partes
            - Mantén todos los puntos importantes
            - Organiza la información de manera lógica
            - Incluye una introducción y conclusión si es apropiado
            
            RESUMEN FINAL:
            """
            
            final_summary = self._call_ollama(consolidation_prompt, system_prompt)
            return final_summary
        else:
            return chunk_summaries[0]
    
    def extract_key_topics(self, text: str) -> List[str]:
        """Identifica los temas clave del texto"""
        system_prompt = """Eres un experto en análisis temático. Identificas los temas principales tratados en un texto."""
        
        # Para textos largos, usar una muestra representativa
        sample_text = text[:3000] + "..." + text[-1000:] if len(text) > 4000 else text
        
        prompt = f"""
        Identifica los 5-8 temas principales tratados en el siguiente texto:
        
        INSTRUCCIONES:
        - Enumera temas específicos y concretos
        - Usa frases descriptivas claras
        - Ordena por importancia/relevancia
        - Evita temas demasiado genéricos
        
        TEXTO:
        {sample_text}
        
        TEMAS PRINCIPALES (uno por línea):
        """
        
        response = self._call_ollama(prompt, system_prompt)
        topics = [line.strip().lstrip('- •*1234567890.') for line in response.split('\n') if line.strip()]
        return topics[:8]
    
    def analyze_sentiment(self, text: str) -> str:
        """Analiza el sentimiento general del texto"""
        system_prompt = """Eres un experto en análisis de sentimientos. Determinas el tono emocional de textos."""
        
        # Para textos largos, analizar una muestra
        sample_text = text[:2000] if len(text) > 2000 else text
        
        prompt = f"""
        Analiza el sentimiento o tono emocional general del siguiente texto:
        
        OPCIONES: Positivo, Neutral, Negativo, Mixto
        
        TEXTO:
        {sample_text}
        
        Responde solo con una palabra del listado de opciones:
        """
        
        response = self._call_ollama(prompt, system_prompt)
        sentiment = response.strip().lower()
        
        # Mapear a opciones válidas
        if any(word in sentiment for word in ['positivo', 'positive']):
            return "Positivo"
        elif any(word in sentiment for word in ['negativo', 'negative']):
            return "Negativo"
        elif any(word in sentiment for word in ['mixto', 'mixed']):
            return "Mixto"
        else:
            return "Neutral"
    
    def identify_speakers(self, text: str) -> List[str]:
        """Identifica hablantes en transcripciones (si aplica)"""
        system_prompt = """Eres un experto en análisis de transcripciones. Identificas a los diferentes hablantes en el texto."""
        
        # Buscar patrones típicos de transcripción
        speaker_patterns = re.findall(r'^([A-Z][^:]+):', text, re.MULTILINE)
        if speaker_patterns:
            return list(set(speaker_patterns))
        
        # Si no hay patrones claros, usar IA para detectar
        sample_text = text[:2000]
        prompt = f"""
        Analiza si el siguiente texto es una transcripción con múltiples hablantes.
        Si es así, lista los nombres o roles de los hablantes que puedas identificar.
        
        TEXTO:
        {sample_text}
        
        Si no hay múltiples hablantes, responde "NO APLICA".
        Si los hay, lista los nombres/roles separados por comas:
        """
        
        response = self._call_ollama(prompt, system_prompt)
        if "no aplica" in response.lower():
            return []
        
        speakers = [s.strip() for s in response.split(',') if s.strip()]
        return speakers[:10]  # Limitar a 10 hablantes máximo
    
    def analyze_text(self, text: str) -> TextAnalysis:
        """Realiza un análisis completo del texto"""
        print("🔍 Iniciando análisis completo del texto...")
        
        print("📝 Calculando estadísticas básicas...")
        word_count = len(text.split())
        reading_time = max(1, word_count // 200)  # ~200 palabras por minuto
        
        print("🎯 Extrayendo palabras clave...")
        keywords = self.extract_keywords(text)
        
        print("📋 Generando resumen detallado...")
        summary = self.generate_detailed_summary(text)
        
        print("🏷️ Identificando temas principales...")
        key_topics = self.extract_key_topics(text)
        
        print("💭 Analizando sentimiento...")
        sentiment = self.analyze_sentiment(text)
        
        print("👥 Identificando hablantes...")
        speakers = self.identify_speakers(text)
        
        return TextAnalysis(
            keywords=keywords,
            summary=summary,
            key_topics=key_topics,
            sentiment=sentiment,
            word_count=word_count,
            reading_time=reading_time,
            speakers=speakers
        )
    
    def save_analysis_report(self, analysis: TextAnalysis, output_file: str):
        """Guarda el análisis en un archivo de reporte"""
        report = f"""
# REPORTE DE ANÁLISIS DE TEXTO LARGO

## 📊 ESTADÍSTICAS GENERALES
- **Número de palabras**: {analysis.word_count:,}
- **Tiempo de lectura estimado**: {analysis.reading_time} minutos
- **Sentimiento general**: {analysis.sentiment}

## 🎯 PALABRAS CLAVE
{', '.join(analysis.keywords)}

## 🏷️ TEMAS PRINCIPALES
{chr(10).join([f"• {topic}" for topic in analysis.key_topics])}

{'## 👥 HABLANTES IDENTIFICADOS' + chr(10) + chr(10).join([f"• {speaker}" for speaker in analysis.speakers]) + chr(10) if analysis.speakers else ''}

## 📋 RESUMEN DETALLADO

{analysis.summary}

---
*Reporte generado con Long Text Analyzer - Ollama*
        """
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report.strip())
        
        print(f"📄 Reporte guardado en: {output_file}")

def main():
    parser = argparse.ArgumentParser(description="Analizador de textos largos con Ollama")
    parser.add_argument("input_file", help="Archivo de texto a analizar")
    parser.add_argument("-o", "--output", help="Archivo de salida para el reporte")
    parser.add_argument("-m", "--model", default="llama3.1", help="Modelo de Ollama a usar")
    parser.add_argument("--url", default="http://localhost:11434", help="URL del servidor Ollama")
    
    args = parser.parse_args()
    
    # Verificar que el archivo existe
    input_path = Path(args.input_file)
    if not input_path.exists():
        print(f"❌ Error: No se encontró el archivo {args.input_file}")
        sys.exit(1)
    
    # Leer el archivo
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            text = f.read()
    except Exception as e:
        print(f"❌ Error leyendo el archivo: {e}")
        sys.exit(1)
    
    if not text.strip():
        print("❌ Error: El archivo está vacío")
        sys.exit(1)
    
    # Crear el analizador
    analyzer = LongTextAnalyzer(model_name=args.model, ollama_url=args.url)
    
    try:
        # Realizar el análisis
        analysis = analyzer.analyze_text(text)
        
        # Mostrar resultados en consola
        print("\n" + "="*60)
        print("📊 RESULTADOS DEL ANÁLISIS")
        print("="*60)
        
        print(f"\n📈 ESTADÍSTICAS:")
        print(f"  • Palabras: {analysis.word_count:,}")
        print(f"  • Tiempo de lectura: {analysis.reading_time} min")
        print(f"  • Sentimiento: {analysis.sentiment}")
        
        if analysis.speakers:
            print(f"\n👥 HABLANTES:")
            for speaker in analysis.speakers:
                print(f"  • {speaker}")
        
        print(f"\n🎯 PALABRAS CLAVE:")
        print(f"  {', '.join(analysis.keywords)}")
        
        print(f"\n🏷️ TEMAS PRINCIPALES:")
        for topic in analysis.key_topics:
            print(f"  • {topic}")
        
        print(f"\n📋 RESUMEN:")
        print(f"  {analysis.summary[:200]}...")
        
        # Guardar reporte si se especifica
        if args.output:
            analyzer.save_analysis_report(analysis, args.output)
        else:
            # Auto-generar nombre de archivo
            output_file = input_path.stem + "_analysis_report.md"
            analyzer.save_analysis_report(analysis, output_file)
        
        print(f"\n✅ Análisis completado exitosamente")
        
    except Exception as e:
        print(f"❌ Error durante el análisis: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()