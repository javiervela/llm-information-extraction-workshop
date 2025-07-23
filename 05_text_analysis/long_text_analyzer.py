# long_text_analyzer.py
"""
Module for long text analysis with Ollama
Extracts keywords and generates detailed summaries of transcripts and long documents
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
    """Structure to store analysis results"""

    keywords: List[str]
    summary: str
    key_topics: List[str]
    sentiment: str
    word_count: int
    reading_time: int
    speakers: List[str]  # For transcripts with multiple speakers


class LongTextAnalyzer:
    """Long text analyzer using Ollama"""

    def __init__(
        self, model_name: str = "llama3.1", ollama_url: str = "http://localhost:11434"
    ):
        self.model_name = model_name
        self.ollama_url = ollama_url
        self.max_chunk_size = 4000  # Maximum chunk size to avoid context limits

    def _call_ollama(self, prompt: str, system_prompt: str = "") -> str:
        """Makes a call to Ollama and returns the response"""
        try:
            payload = {
                "model": self.model_name,
                "prompt": prompt,
                "stream": False,
                "system": system_prompt,
                "options": {"temperature": 0.1, "top_p": 0.9, "num_ctx": 8192},
            }

            response = requests.post(
                f"{self.ollama_url}/api/generate", json=payload, timeout=120
            )
            response.raise_for_status()
            return response.json()["response"].strip()

        except requests.exceptions.RequestException as e:
            raise Exception(f"Error connecting to Ollama: {e}")

    def _chunk_text(self, text: str) -> List[str]:
        """Splits text into manageable chunks"""
        # Split by paragraphs first
        paragraphs = text.split("\n\n")
        chunks = []
        current_chunk = ""

        for paragraph in paragraphs:
            # If the paragraph is very long, split by sentences
            if len(paragraph) > self.max_chunk_size:
                sentences = re.split(r"[.!?]+", paragraph)
                for sentence in sentences:
                    if len(current_chunk + sentence) > self.max_chunk_size:
                        if current_chunk:
                            chunks.append(current_chunk.strip())
                            current_chunk = sentence
                        else:
                            # If a single sentence is too long, forcibly split
                            chunks.append(sentence[: self.max_chunk_size])
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
        """Extracts keywords from the text"""
        chunks = self._chunk_text(text)
        all_keywords = []

        system_prompt = """You are an expert in text analysis. Your task is to extract the most important and relevant keywords from the provided text."""

        for chunk in chunks:
            prompt = f"""
            Analyze the following text and extract the 10-15 most important keywords.
            
            INSTRUCTIONS:
            - Include both single terms and key phrases
            - Prioritize concepts, proper names, and central topics
            - Avoid stopwords or very generic words
            - Present the keywords separated by commas
            - Do not include additional explanations
            
            TEXT TO ANALYZE:
            {chunk}
            
            KEYWORDS:
            """

            response = self._call_ollama(prompt, system_prompt)
            chunk_keywords = [kw.strip() for kw in response.split(",")]
            all_keywords.extend(chunk_keywords)

        # Consolidate and filter duplicate keywords
        unique_keywords = list(set(all_keywords))

        # If we have many keywords, select the most relevant ones
        if len(unique_keywords) > 20:
            consolidation_prompt = f"""
            From the following list of keywords, select the 15-20 most important and relevant for the text:
            
            {', '.join(unique_keywords)}
            
            Present only the selected keywords, separated by commas:
            """

            response = self._call_ollama(consolidation_prompt, system_prompt)
            unique_keywords = [kw.strip() for kw in response.split(",")]

        return unique_keywords[:20]  # Limit to max 20 keywords

    def generate_detailed_summary(self, text: str) -> str:
        """Generates a detailed summary of the text"""
        chunks = self._chunk_text(text)
        chunk_summaries = []

        system_prompt = """You are an expert in synthesis and content analysis. You create detailed, structured, and comprehensive summaries."""

        # Generate summary for each chunk
        for i, chunk in enumerate(chunks):
            prompt = f"""
            Create a detailed summary of the following text fragment (part {i+1} of {len(chunks)}):
            
            INSTRUCTIONS:
            - Include the most important points and relevant details
            - Maintain the logical structure of the content
            - Do not omit crucial information
            - Use a clear and professional style
            
            TEXT:
            {chunk}
            
            DETAILED SUMMARY:
            """

            chunk_summary = self._call_ollama(prompt, system_prompt)
            chunk_summaries.append(chunk_summary)

        # Consolidate all summaries
        if len(chunk_summaries) > 1:
            consolidation_prompt = f"""
            Consolidate the following partial summaries into a final cohesive and well-structured summary:
            
            PARTIAL SUMMARIES:
            {' '.join([f"PART {i+1}: {summary}" for i, summary in enumerate(chunk_summaries)])}
            
            INSTRUCTIONS FOR THE FINAL SUMMARY:
            - Create a fluent and well-structured summary
            - Remove redundancies between parts
            - Keep all important points
            - Organize the information logically
            - Include an introduction and conclusion if appropriate
            
            FINAL SUMMARY:
            """

            final_summary = self._call_ollama(consolidation_prompt, system_prompt)
            return final_summary
        else:
            return chunk_summaries[0]

    def extract_key_topics(self, text: str) -> List[str]:
        """Identifies the key topics of the text"""
        system_prompt = """You are an expert in thematic analysis. You identify the main topics covered in a text."""

        # For long texts, use a representative sample
        sample_text = text[:3000] + "..." + text[-1000:] if len(text) > 4000 else text

        prompt = f"""
        Identify the 5-8 main topics covered in the following text:
        
        INSTRUCTIONS:
        - List specific and concrete topics
        - Use clear descriptive phrases
        - Order by importance/relevance
        - Avoid overly generic topics
        
        TEXT:
        {sample_text}
        
        MAIN TOPICS (one per line):
        """

        response = self._call_ollama(prompt, system_prompt)
        topics = [
            line.strip().lstrip("- •*1234567890.")
            for line in response.split("\n")
            if line.strip()
        ]
        return topics[:8]

    def analyze_sentiment(self, text: str) -> str:
        """Analyzes the general sentiment of the text"""
        system_prompt = """You are an expert in sentiment analysis. You determine the emotional tone of texts."""

        # For long texts, analyze a sample
        sample_text = text[:2000] if len(text) > 2000 else text

        prompt = f"""
        Analyze the general sentiment or emotional tone of the following text:
        
        OPTIONS: Positive, Neutral, Negative, Mixed
        
        TEXT:
        {sample_text}
        
        Respond only with one word from the options list:
        """

        response = self._call_ollama(prompt, system_prompt)
        sentiment = response.strip().lower()

        # Map to valid options
        if any(word in sentiment for word in ["positivo", "positive"]):
            return "Positive"
        elif any(word in sentiment for word in ["negativo", "negative"]):
            return "Negative"
        elif any(word in sentiment for word in ["mixto", "mixed"]):
            return "Mixed"
        else:
            return "Neutral"

    def identify_speakers(self, text: str) -> List[str]:
        """Identifies speakers in transcripts (if applicable)"""
        system_prompt = """You are an expert in transcript analysis. You identify the different speakers in the text."""

        # Look for typical transcript patterns
        speaker_patterns = re.findall(r"^([A-Z][^:]+):", text, re.MULTILINE)
        if speaker_patterns:
            return list(set(speaker_patterns))

        # If there are no clear patterns, use AI to detect
        sample_text = text[:2000]
        prompt = f"""
        Analyze if the following text is a transcript with multiple speakers.
        If so, list the names or roles of the speakers you can identify.
        
        TEXT:
        {sample_text}
        
        If there are no multiple speakers, respond "NOT APPLICABLE".
        If there are, list the names/roles separated by commas:
        """

        response = self._call_ollama(prompt, system_prompt)
        if "not applicable" in response.lower() or "no aplica" in response.lower():
            return []

        speakers = [s.strip() for s in response.split(",") if s.strip()]
        return speakers[:10]  # Limit to max 10 speakers

    def analyze_text(self, text: str) -> TextAnalysis:
        """Performs a complete analysis of the text"""
        print("🔍 Starting full text analysis...")

        print("📝 Calculating basic statistics...")
        word_count = len(text.split())
        reading_time = max(1, word_count // 200)  # ~200 words per minute

        print("🎯 Extracting keywords...")
        keywords = self.extract_keywords(text)

        print("📋 Generating detailed summary...")
        summary = self.generate_detailed_summary(text)

        print("🏷️ Identifying main topics...")
        key_topics = self.extract_key_topics(text)

        print("💭 Analyzing sentiment...")
        sentiment = self.analyze_sentiment(text)

        print("👥 Identifying speakers...")
        speakers = self.identify_speakers(text)

        return TextAnalysis(
            keywords=keywords,
            summary=summary,
            key_topics=key_topics,
            sentiment=sentiment,
            word_count=word_count,
            reading_time=reading_time,
            speakers=speakers,
        )

    def save_analysis_report(self, analysis: TextAnalysis, output_file: str):
        """Saves the analysis to a report file"""
        report = f"""
# LONG TEXT ANALYSIS REPORT

## 📊 GENERAL STATISTICS
- **Word count**: {analysis.word_count:,}
- **Estimated reading time**: {analysis.reading_time} minutes
- **General sentiment**: {analysis.sentiment}

## 🎯 KEYWORDS
{', '.join(analysis.keywords)}

## 🏷️ MAIN TOPICS
{chr(10).join([f"• {topic}" for topic in analysis.key_topics])}

{'## 👥 IDENTIFIED SPEAKERS' + chr(10) + chr(10).join([f"• {speaker}" for speaker in analysis.speakers]) + chr(10) if analysis.speakers else ''}

## 📋 DETAILED SUMMARY

{analysis.summary}

---
*Report generated with Long Text Analyzer - Ollama*
        """

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(report.strip())

        print(f"📄 Report saved to: {output_file}")


def main():
    parser = argparse.ArgumentParser(description="Long text analyzer with Ollama")
    parser.add_argument("input_file", help="Text file to analyze")
    parser.add_argument("-o", "--output", help="Output file for the report")
    parser.add_argument("-m", "--model", default="llama3.1", help="Ollama model to use")
    parser.add_argument(
        "--url", default="http://localhost:11434", help="Ollama server URL"
    )

    args = parser.parse_args()

    # Check that the file exists
    input_path = Path(args.input_file)
    if not input_path.exists():
        print(f"❌ Error: File not found {args.input_file}")
        sys.exit(1)

    # Read the file
    try:
        with open(input_path, "r", encoding="utf-8") as f:
            text = f.read()
    except Exception as e:
        print(f"❌ Error reading the file: {e}")
        sys.exit(1)

    if not text.strip():
        print("❌ Error: The file is empty")
        sys.exit(1)

    # Create the analyzer
    analyzer = LongTextAnalyzer(model_name=args.model, ollama_url=args.url)

    try:
        # Perform the analysis
        analysis = analyzer.analyze_text(text)

        # Show results in console
        print("\n" + "=" * 60)
        print("📊 ANALYSIS RESULTS")
        print("=" * 60)

        print(f"\n📈 STATISTICS:")
        print(f"  • Words: {analysis.word_count:,}")
        print(f"  • Reading time: {analysis.reading_time} min")
        print(f"  • Sentiment: {analysis.sentiment}")

        if analysis.speakers:
            print(f"\n👥 SPEAKERS:")
            for speaker in analysis.speakers:
                print(f"  • {speaker}")

        print(f"\n🎯 KEYWORDS:")
        print(f"  {', '.join(analysis.keywords)}")

        print(f"\n🏷️ MAIN TOPICS:")
        for topic in analysis.key_topics:
            print(f"  • {topic}")

        print(f"\n📋 SUMMARY:")
        print(f"  {analysis.summary[:200]}...")

        # Save report if specified
        if args.output:
            analyzer.save_analysis_report(analysis, args.output)
        else:
            # Auto-generate file name
            output_file = input_path.stem + "_analysis_report.md"
            analyzer.save_analysis_report(analysis, output_file)

        print(f"\n✅ Analysis completed successfully")

    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
