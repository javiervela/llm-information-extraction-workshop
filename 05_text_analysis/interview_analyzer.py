# interview_analyzer.py
"""
Analizador especializado para transcripciones de entrevistas
Extensión del módulo de análisis de textos largos
"""

from long_text_analyzer import LongTextAnalyzer, TextAnalysis
from dataclasses import dataclass
from typing import Dict, List, Tuple
import re
import argparse
import sys
from pathlib import Path


@dataclass
class InterviewAnalysis(TextAnalysis):
    """Extensión del análisis para entrevistas específicamente"""

    interview_type: str
    main_insights: List[str]
    quotes_highlights: List[str]
    questions_themes: List[str]
    interaction_style: str
    duration_estimate: int  # en minutos


class InterviewAnalyzer(LongTextAnalyzer):
    """Analizador especializado en entrevistas"""

    def __init__(
        self, model_name: str = "llama3.1", ollama_url: str = "http://localhost:11434"
    ):
        super().__init__(model_name, ollama_url)

    def identify_interview_type(self, text: str) -> str:
        """Identifica el tipo de entrevista"""
        sample_text = text[:1500]

        system_prompt = "Eres un experto en análisis de entrevistas y comunicación."

        prompt = f"""
        Basándote en el contenido y estilo de la siguiente transcripción, identifica el tipo de entrevista:
        
        OPCIONES:
        - Entrevista laboral
        - Entrevista periodística  
        - Entrevista de investigación
        - Entrevista clínica/terapéutica
        - Entrevista académica
        - Podcast/conversación informal
        - Otro (especifica)
        
        TRANSCRIPCIÓN:
        {sample_text}
        
        Responde solo con el tipo identificado:
        """

        response = self._call_ollama(prompt, system_prompt)
        return response.strip()

    def extract_main_insights(self, text: str) -> List[str]:
        """Extrae los insights principales de la entrevista"""
        system_prompt = "Eres un experto en análisis cualitativo de entrevistas."

        prompt = f"""
        Analiza la siguiente transcripción de entrevista e identifica los 5-7 insights más importantes o reveladores.
        
        INSTRUCCIONES:
        - Busca ideas clave, revelaciones, puntos de vista únicos
        - Incluye conclusiones importantes del entrevistado
        - Identifica patrones o temas recurrentes
        - Enfócate en lo más valioso o sorprendente
        
        TRANSCRIPCIÓN:
        {text[:3000]}...
        
        INSIGHTS PRINCIPALES (uno por línea):
        """

        response = self._call_ollama(prompt, system_prompt)
        insights = [
            line.strip().lstrip("- •*1234567890.")
            for line in response.split("\n")
            if line.strip()
        ]
        return insights[:7]

    def extract_highlight_quotes(self, text: str) -> List[str]:
        """Extrae las citas más destacadas de la entrevista"""
        system_prompt = "Eres un experto en identificar citas impactantes y memorables."

        prompt = f"""
        De la siguiente transcripción de entrevista, identifica las 5-8 citas más impactantes, reveladoras o memorables.
        
        CRITERIOS:
        - Frases que resuman puntos clave
        - Declaraciones sorprendentes o controversiales  
        - Citas inspiradoras o emotivas
        - Frases que capturen la esencia del mensaje
        
        TRANSCRIPCIÓN:
        {text[:4000]}...
        
        Presenta cada cita entre comillas, una por línea:
        """

        response = self._call_ollama(prompt, system_prompt)
        quotes = [
            line.strip().strip('"').strip("'")
            for line in response.split("\n")
            if line.strip() and ('"' in line or "'" in line)
        ]
        return quotes[:8]

    def analyze_question_themes(self, text: str) -> List[str]:
        """Analiza los temas de las preguntas realizadas"""
        system_prompt = (
            "Eres un experto en análisis de entrevistas y técnicas de interrogación."
        )

        # Intentar identificar preguntas en el texto
        question_patterns = re.findall(r"[¿?][^¿?]*[?¿]", text)
        questions_text = " ".join(question_patterns[:20])  # Primeras 20 preguntas

        if not questions_text:
            # Si no hay patrones de preguntas claros, analizar temas generales
            questions_text = text[:2000]

        prompt = f"""
        Analiza las preguntas o temas tratados en esta entrevista e identifica las 5-6 áreas temáticas principales.
        
        PREGUNTAS/CONTENIDO:
        {questions_text}
        
        ÁREAS TEMÁTICAS (una por línea):
        """

        response = self._call_ollama(prompt, system_prompt)
        themes = [
            line.strip().lstrip("- •*1234567890.")
            for line in response.split("\n")
            if line.strip()
        ]
        return themes[:6]

    def analyze_interaction_style(self, text: str) -> str:
        """Analiza el estilo de interacción en la entrevista"""
        sample_text = text[:2000]

        system_prompt = (
            "Eres un experto en análisis de comunicación y dinámicas interpersonales."
        )

        prompt = f"""
        Analiza el estilo de interacción y dinámicas de comunicación en esta entrevista:
        
        ASPECTOS A CONSIDERAR:
        - Formalidad vs informalidad
        - Confrontacional vs colaborativo  
        - Directivo vs exploratorio
        - Tenso vs relajado
        
        MUESTRA DE LA TRANSCRIPCIÓN:
        {sample_text}
        
        Describe el estilo en 2-3 palabras clave:
        """

        response = self._call_ollama(prompt, system_prompt)
        return response.strip()

    def estimate_interview_duration(self, text: str) -> int:
        """Estima la duración de la entrevista en minutos"""
        word_count = len(text.split())
        # Promedio: ~150-180 palabras por minuto en conversación
        estimated_minutes = max(1, word_count // 165)
        return estimated_minutes

    def analyze_interview(self, text: str) -> InterviewAnalysis:
        """Realiza un análisis completo específico para entrevistas"""
        print("🎤 Iniciando análisis especializado de entrevista...")

        # Análisis base
        base_analysis = self.analyze_text(text)

        print("🔍 Identificando tipo de entrevista...")
        interview_type = self.identify_interview_type(text)

        print("💡 Extrayendo insights principales...")
        main_insights = self.extract_main_insights(text)

        print("💬 Identificando citas destacadas...")
        quotes_highlights = self.extract_highlight_quotes(text)

        print("❓ Analizando temas de preguntas...")
        questions_themes = self.analyze_question_themes(text)

        print("🤝 Evaluando estilo de interacción...")
        interaction_style = self.analyze_interaction_style(text)

        print("⏱️ Estimando duración...")
        duration_estimate = self.estimate_interview_duration(text)

        return InterviewAnalysis(
            # Campos heredados
            keywords=base_analysis.keywords,
            summary=base_analysis.summary,
            key_topics=base_analysis.key_topics,
            sentiment=base_analysis.sentiment,
            word_count=base_analysis.word_count,
            reading_time=base_analysis.reading_time,
            speakers=base_analysis.speakers,
            # Campos específicos de entrevista
            interview_type=interview_type,
            main_insights=main_insights,
            quotes_highlights=quotes_highlights,
            questions_themes=questions_themes,
            interaction_style=interaction_style,
            duration_estimate=duration_estimate,
        )

    def save_interview_report(self, analysis: InterviewAnalysis, output_file: str):
        """Guarda el análisis especializado de entrevista"""
        report = f"""
# REPORTE DE ANÁLISIS DE ENTREVISTA

## 📊 INFORMACIÓN GENERAL
- **Tipo de entrevista**: {analysis.interview_type}
- **Duración estimada**: {analysis.duration_estimate} minutos
- **Número de palabras**: {analysis.word_count:,}
- **Estilo de interacción**: {analysis.interaction_style}
- **Sentimiento general**: {analysis.sentiment}

{'## 👥 PARTICIPANTES' + chr(10) + chr(10).join([f"• {speaker}" for speaker in analysis.speakers]) + chr(10) if analysis.speakers else ''}

## 💡 INSIGHTS PRINCIPALES
{chr(10).join([f"• {insight}" for insight in analysis.main_insights])}

## 💬 CITAS DESTACADAS
{chr(10).join([f'• "{quote}"' for quote in analysis.quotes_highlights])}

## ❓ TEMAS DE PREGUNTAS/DISCUSIÓN
{chr(10).join([f"• {theme}" for theme in analysis.questions_themes])}

## 🎯 PALABRAS CLAVE
{', '.join(analysis.keywords)}

## 🏷️ TEMAS PRINCIPALES IDENTIFICADOS
{chr(10).join([f"• {topic}" for topic in analysis.key_topics])}

## 📋 RESUMEN EJECUTIVO

{analysis.summary}

---
*Reporte generado con Interview Analyzer - Módulo especializado de Ollama*
        """

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(report.strip())

        print(f"📄 Reporte de entrevista guardado en: {output_file}")


def main():
    parser = argparse.ArgumentParser(
        description="Analizador especializado de entrevistas con Ollama"
    )
    parser.add_argument("input_file", help="Archivo de transcripción a analizar")
    parser.add_argument("-o", "--output", help="Archivo de salida para el reporte")
    parser.add_argument(
        "-m", "--model", default="llama3.1", help="Modelo de Ollama a usar"
    )
    parser.add_argument(
        "--url", default="http://localhost:11434", help="URL del servidor Ollama"
    )

    args = parser.parse_args()

    # Verificar archivo
    input_path = Path(args.input_file)
    if not input_path.exists():
        print(f"❌ Error: No se encontró el archivo {args.input_file}")
        sys.exit(1)

    # Leer transcripción
    try:
        with open(input_path, "r", encoding="utf-8") as f:
            text = f.read()
    except Exception as e:
        print(f"❌ Error leyendo el archivo: {e}")
        sys.exit(1)

    # Crear analizador
    analyzer = InterviewAnalyzer(model_name=args.model, ollama_url=args.url)

    try:
        # Realizar análisis
        analysis = analyzer.analyze_interview(text)

        # Mostrar resultados
        print("\n" + "=" * 60)
        print("🎤 ANÁLISIS DE ENTREVISTA COMPLETADO")
        print("=" * 60)

        print(f"\n📊 INFORMACIÓN GENERAL:")
        print(f"  • Tipo: {analysis.interview_type}")
        print(f"  • Duración estimada: {analysis.duration_estimate} min")
        print(f"  • Estilo: {analysis.interaction_style}")
        print(f"  • Sentimiento: {analysis.sentiment}")

        if analysis.speakers:
            print(f"\n👥 PARTICIPANTES:")
            for speaker in analysis.speakers:
                print(f"  • {speaker}")

        print(f"\n💡 INSIGHTS CLAVE:")
        for insight in analysis.main_insights[:3]:
            print(f"  • {insight}")

        print(f"\n💬 CITAS DESTACADAS:")
        for quote in analysis.quotes_highlights[:2]:
            print(f'  • "{quote[:100]}..."')

        # Guardar reporte
        if args.output:
            analyzer.save_interview_report(analysis, args.output)
        else:
            output_file = input_path.stem + "_interview_analysis.md"
            analyzer.save_interview_report(analysis, output_file)

        print(f"\n✅ Análisis de entrevista completado exitosamente")

    except Exception as e:
        print(f"❌ Error durante el análisis: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
