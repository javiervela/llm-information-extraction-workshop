# batch_analyzer.py
"""
Script para análisis en lote de múltiples archivos de texto
Útil para procesar varios documentos o transcripciones de una vez
"""

import os
import sys
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict
import argparse
import json
from datetime import datetime

from long_text_analyzer import LongTextAnalyzer
from interview_analyzer import InterviewAnalyzer


class BatchAnalyzer:
    """Procesador en lote para análisis de textos largos"""

    def __init__(
        self,
        model_name: str = "llama3.1",
        ollama_url: str = "http://localhost:11434",
        max_workers: int = 2,
    ):
        self.model_name = model_name
        self.ollama_url = ollama_url
        self.max_workers = max_workers
        self.results = []

    def find_text_files(
        self, directory: str, extensions: List[str] = [".txt", ".md"]
    ) -> List[Path]:
        """Encuentra todos los archivos de texto en un directorio"""
        directory_path = Path(directory)
        text_files = []

        for ext in extensions:
            text_files.extend(directory_path.glob(f"**/*{ext}"))

        return sorted(text_files)

    def analyze_single_file(
        self, file_path: Path, analysis_type: str = "general"
    ) -> Dict:
        """Analiza un solo archivo y retorna los resultados"""
        try:
            print(f"📄 Procesando: {file_path.name}")

            # Leer archivo
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()

            if not text.strip():
                return {
                    "file": str(file_path),
                    "status": "error",
                    "error": "Archivo vacío",
                    "timestamp": datetime.now().isoformat(),
                }

            # Crear analizador apropiado
            if analysis_type == "interview":
                analyzer = InterviewAnalyzer(self.model_name, self.ollama_url)
                analysis = analyzer.analyze_interview(text)
            else:
                analyzer = LongTextAnalyzer(self.model_name, self.ollama_url)
                analysis = analyzer.analyze_text(text)

            # Generar reporte
            output_file = (
                file_path.parent / f"{file_path.stem}_{analysis_type}_report.md"
            )

            if analysis_type == "interview":
                analyzer.save_interview_report(analysis, str(output_file))
            else:
                analyzer.save_analysis_report(analysis, str(output_file))

            return {
                "file": str(file_path),
                "status": "success",
                "output_report": str(output_file),
                "word_count": analysis.word_count,
                "keywords_count": len(analysis.keywords),
                "topics_count": len(analysis.key_topics),
                "sentiment": analysis.sentiment,
                "timestamp": datetime.now().isoformat(),
                "analysis_type": analysis_type,
            }

        except Exception as e:
            return {
                "file": str(file_path),
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
            }

    def process_files(
        self, files: List[Path], analysis_type: str = "general"
    ) -> List[Dict]:
        """Procesa múltiples archivos en paralelo"""
        results = []

        print(f"🚀 Iniciando análisis en lote de {len(files)} archivos...")
        print(f"📊 Tipo de análisis: {analysis_type}")
        print(f"🔧 Modelo: {self.model_name}")
        print(f"⚡ Workers: {self.max_workers}")
        print("-" * 60)

        start_time = time.time()

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Enviar tareas
            future_to_file = {
                executor.submit(
                    self.analyze_single_file, file_path, analysis_type
                ): file_path
                for file_path in files
            }

            # Recoger resultados
            completed = 0
            for future in as_completed(future_to_file):
                file_path = future_to_file[future]
                try:
                    result = future.result()
                    results.append(result)
                    completed += 1

                    status_icon = "✅" if result["status"] == "success" else "❌"
                    print(f"{status_icon} [{completed}/{len(files)}] {file_path.name}")

                except Exception as e:
                    results.append(
                        {
                            "file": str(file_path),
                            "status": "error",
                            "error": str(e),
                            "timestamp": datetime.now().isoformat(),
                        }
                    )
                    print(
                        f"❌ [{completed+1}/{len(files)}] {file_path.name} - Error: {e}"
                    )
                    completed += 1

        elapsed_time = time.time() - start_time
        print("-" * 60)
        print(f"⏱️  Tiempo total: {elapsed_time:.2f} segundos")
        print(
            f"📈 Archivos procesados: {len([r for r in results if r['status'] == 'success'])}/{len(files)}"
        )

        return results

    def generate_batch_summary(self, results: List[Dict], output_file: str):
        """Genera un resumen del análisis en lote"""
        successful = [r for r in results if r["status"] == "success"]
        failed = [r for r in results if r["status"] == "error"]

        # Estadísticas agregadas
        total_words = sum(r.get("word_count", 0) for r in successful)
        avg_keywords = (
            sum(r.get("keywords_count", 0) for r in successful) / len(successful)
            if successful
            else 0
        )
        sentiment_counts = {}
        for r in successful:
            sentiment = r.get("sentiment", "Unknown")
            sentiment_counts[sentiment] = sentiment_counts.get(sentiment, 0) + 1

        summary_report = f"""
# RESUMEN DE ANÁLISIS EN LOTE

**Fecha de procesamiento**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Modelo utilizado**: {self.model_name}

## 📊 ESTADÍSTICAS GENERALES

- **Archivos procesados**: {len(results)}
- **Exitosos**: {len(successful)} ({len(successful)/len(results)*100:.1f}%)
- **Fallidos**: {len(failed)} ({len(failed)/len(results)*100:.1f}%)
- **Palabras totales**: {total_words:,}
- **Promedio de palabras clave por archivo**: {avg_keywords:.1f}

## 😊 DISTRIBUCIÓN DE SENTIMIENTOS

{chr(10).join([f"- **{sentiment}**: {count} archivos" for sentiment, count in sentiment_counts.items()])}

## ✅ ARCHIVOS PROCESADOS EXITOSAMENTE

{chr(10).join([f"- `{Path(r['file']).name}` → `{Path(r['output_report']).name}`" for r in successful])}

{"## ❌ ARCHIVOS CON ERRORES" + chr(10) + chr(10) + chr(10).join([f"- `{Path(r['file']).name}`: {r['error']}" for r in failed]) + chr(10) if failed else ""}

## 📁 ARCHIVOS DE REPORTE GENERADOS

Los reportes individuales se encuentran en los mismos directorios que los archivos originales con el sufijo `_report.md`.

---
*Resumen generado por Batch Analyzer - Módulo de análisis en lote*
        """

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(summary_report.strip())

        print(f"📋 Resumen del lote guardado en: {output_file}")

    def save_results_json(self, results: List[Dict], output_file: str):
        """Guarda los resultados detallados en JSON"""
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)

        print(f"💾 Resultados detallados guardados en: {output_file}")


def main():
    parser = argparse.ArgumentParser(
        description="Análisis en lote de textos largos con Ollama"
    )
    parser.add_argument(
        "directory", help="Directorio que contiene los archivos a analizar"
    )
    parser.add_argument(
        "-t",
        "--type",
        choices=["general", "interview"],
        default="general",
        help="Tipo de análisis (general o interview)",
    )
    parser.add_argument(
        "-m", "--model", default="llama3.1", help="Modelo de Ollama a usar"
    )
    parser.add_argument(
        "-w", "--workers", type=int, default=2, help="Número de workers paralelos"
    )
    parser.add_argument(
        "--url", default="http://localhost:11434", help="URL del servidor Ollama"
    )
    parser.add_argument("-o", "--output-dir", help="Directorio para archivos de salida")
    parser.add_argument(
        "--extensions",
        nargs="+",
        default=[".txt", ".md"],
        help="Extensiones de archivo a procesar",
    )

    args = parser.parse_args()

    # Verificar directorio
    if not Path(args.directory).exists():
        print(f"❌ Error: El directorio {args.directory} no existe")
        sys.exit(1)

    # Crear analizador en lote
    batch_analyzer = BatchAnalyzer(
        model_name=args.model, ollama_url=args.url, max_workers=args.workers
    )

    # Encontrar archivos
    files = batch_analyzer.find_text_files(args.directory, args.extensions)

    if not files:
        print(
            f"❌ No se encontraron archivos con extensiones {args.extensions} en {args.directory}"
        )
        sys.exit(1)

    print(f"📂 Encontrados {len(files)} archivos en {args.directory}")

    # Confirmar antes de procesar
    response = input(f"¿Proceder con el análisis de {len(files)} archivos? (y/N): ")
    if response.lower() not in ["y", "yes", "s", "si", "sí"]:
        print("❌ Análisis cancelado por el usuario")
        sys.exit(0)

    try:
        # Procesar archivos
        results = batch_analyzer.process_files(files, args.type)

        # Determinar directorio de salida
        output_dir = Path(args.output_dir) if args.output_dir else Path(args.directory)
        output_dir.mkdir(exist_ok=True)

        # Generar archivos de resumen
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        summary_file = output_dir / f"batch_analysis_summary_{timestamp}.md"
        batch_analyzer.generate_batch_summary(results, str(summary_file))

        json_file = output_dir / f"batch_analysis_results_{timestamp}.json"
        batch_analyzer.save_results_json(results, str(json_file))

        print("\n" + "=" * 60)
        print("🎉 ANÁLISIS EN LOTE COMPLETADO")
        print("=" * 60)
        print(f"📋 Resumen: {summary_file}")
        print(f"💾 Datos JSON: {json_file}")

    except KeyboardInterrupt:
        print("\n❌ Análisis interrumpido por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error durante el análisis en lote: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
