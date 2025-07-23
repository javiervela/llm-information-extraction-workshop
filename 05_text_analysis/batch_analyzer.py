# batch_analyzer.py
"""
Batch analysis script for multiple text files.
Useful for processing several documents or transcripts at once.
"""

import argparse
import json
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path
from typing import List, Dict

from interview_analyzer import InterviewAnalyzer
from long_text_analyzer import LongTextAnalyzer


class BatchAnalyzer:
    """Batch processor for long text analysis"""

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
        """Finds all text files in a directory"""
        directory_path = Path(directory)
        text_files = []

        for ext in extensions:
            text_files.extend(directory_path.glob(f"**/*{ext}"))

        return sorted(text_files)

    def analyze_single_file(
        self, file_path: Path, analysis_type: str = "general"
    ) -> Dict:
        """Analyzes a single file and returns the results"""
        try:
            print(f"📄 Processing: {file_path.name}")

            # Read file
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()

            if not text.strip():
                return {
                    "file": str(file_path),
                    "status": "error",
                    "error": "Empty file",
                    "timestamp": datetime.now().isoformat(),
                }

            # Create appropriate analyzer
            if analysis_type == "interview":
                analyzer = InterviewAnalyzer(self.model_name, self.ollama_url)
                analysis = analyzer.analyze_interview(text)
            else:
                analyzer = LongTextAnalyzer(self.model_name, self.ollama_url)
                analysis = analyzer.analyze_text(text)

            # Generate report
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
        """Processes multiple files in parallel"""
        results = []

        print(f"🚀 Starting batch analysis of {len(files)} files...")
        print(f"📊 Analysis type: {analysis_type}")
        print(f"🔧 Model: {self.model_name}")
        print(f"⚡ Workers: {self.max_workers}")
        print("-" * 60)

        start_time = time.time()

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit tasks
            future_to_file = {
                executor.submit(
                    self.analyze_single_file, file_path, analysis_type
                ): file_path
                for file_path in files
            }

            # Collect results
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
        print(f"⏱️  Total time: {elapsed_time:.2f} seconds")
        print(
            f"📈 Files processed: {len([r for r in results if r['status'] == 'success'])}/{len(files)}"
        )

        return results

    def generate_batch_summary(self, results: List[Dict], output_file: str):
        """Generates a summary of the batch analysis"""
        successful = [r for r in results if r["status"] == "success"]
        failed = [r for r in results if r["status"] == "error"]

        # Aggregate statistics
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
# BATCH ANALYSIS SUMMARY

**Processing date**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Model used**: {self.model_name}

## 📊 GENERAL STATISTICS

- **Files processed**: {len(results)}
- **Successful**: {len(successful)} ({len(successful)/len(results)*100:.1f}%)
- **Failed**: {len(failed)} ({len(failed)/len(results)*100:.1f}%)
- **Total words**: {total_words:,}
- **Average keywords per file**: {avg_keywords:.1f}

## 😊 SENTIMENT DISTRIBUTION

{chr(10).join([f"- **{sentiment}**: {count} files" for sentiment, count in sentiment_counts.items()])}

## ✅ SUCCESSFULLY PROCESSED FILES

{chr(10).join([f"- `{Path(r['file']).name}` → `{Path(r['output_report']).name}`" for r in successful])}

{"## ❌ FILES WITH ERRORS" + chr(10) + chr(10) + chr(10).join([f"- `{Path(r['file']).name}`: {r['error']}" for r in failed]) + chr(10) if failed else ""}

## 📁 GENERATED REPORT FILES

Individual reports are located in the same directories as the original files with the suffix `_report.md`.

---
*Summary generated by Batch Analyzer - Batch analysis module*
        """

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(summary_report.strip())

        print(f"📋 Batch summary saved to: {output_file}")

    def save_results_json(self, results: List[Dict], output_file: str):
        """Saves detailed results in JSON"""
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)

        print(f"💾 Detailed results saved to: {output_file}")


def main():
    parser = argparse.ArgumentParser(
        description="Batch analysis of long texts with Ollama"
    )
    parser.add_argument("directory", help="Directory containing the files to analyze")
    parser.add_argument(
        "-t",
        "--type",
        choices=["general", "interview"],
        default="general",
        help="Type of analysis (general or interview)",
    )
    parser.add_argument("-m", "--model", default="llama3.1", help="Ollama model to use")
    parser.add_argument(
        "-w", "--workers", type=int, default=2, help="Number of parallel workers"
    )
    parser.add_argument(
        "--url", default="http://localhost:11434", help="Ollama server URL"
    )
    parser.add_argument("-o", "--output-dir", help="Directory for output files")
    parser.add_argument(
        "--extensions",
        nargs="+",
        default=[".txt", ".md"],
        help="File extensions to process",
    )

    args = parser.parse_args()

    # Check directory
    if not Path(args.directory).exists():
        print(f"❌ Error: Directory {args.directory} does not exist")
        sys.exit(1)

    # Create batch analyzer
    batch_analyzer = BatchAnalyzer(
        model_name=args.model, ollama_url=args.url, max_workers=args.workers
    )

    # Find files
    files = batch_analyzer.find_text_files(args.directory, args.extensions)

    if not files:
        print(
            f"❌ No files found with extensions {args.extensions} in {args.directory}"
        )
        sys.exit(1)

    print(f"📂 Found {len(files)} files in {args.directory}")

    # Confirm before processing
    response = input(f"Proceed with analysis of {len(files)} files? (y/N): ")
    if response.lower() not in ["y", "yes", "s", "si", "sí"]:
        print("❌ Analysis cancelled by user")
        sys.exit(0)

    try:
        # Process files
        results = batch_analyzer.process_files(files, args.type)

        # Determine output directory
        output_dir = Path(args.output_dir) if args.output_dir else Path(args.directory)
        output_dir.mkdir(exist_ok=True)

        # Generate summary files
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        summary_file = output_dir / f"batch_analysis_summary_{timestamp}.md"
        batch_analyzer.generate_batch_summary(results, str(summary_file))

        json_file = output_dir / f"batch_analysis_results_{timestamp}.json"
        batch_analyzer.save_results_json(results, str(json_file))

        print("\n" + "=" * 60)
        print("🎉 BATCH ANALYSIS COMPLETED")
        print("=" * 60)
        print(f"📋 Summary: {summary_file}")
        print(f"💾 JSON Data: {json_file}")

    except KeyboardInterrupt:
        print("\n❌ Analysis interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error during batch analysis: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
