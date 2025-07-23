# interview_analyzer.py
"""
Specialized analyzer for interview transcripts
Extension of the long text analysis module
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
    """Extension of analysis specifically for interviews"""

    interview_type: str
    main_insights: List[str]
    quotes_highlights: List[str]
    questions_themes: List[str]
    interaction_style: str
    duration_estimate: int  # in minutes


class InterviewAnalyzer(LongTextAnalyzer):
    """Specialized analyzer for interviews"""

    def __init__(
        self, model_name: str = "llama3.1", ollama_url: str = "http://localhost:11434"
    ):
        super().__init__(model_name, ollama_url)

    def identify_interview_type(self, text: str) -> str:
        """Identifies the type of interview"""
        sample_text = text[:1500]

        system_prompt = "You are an expert in interview analysis and communication."

        prompt = f"""
        Based on the content and style of the following transcript, identify the type of interview:
        
        OPTIONS:
        - Job interview
        - Journalistic interview  
        - Research interview
        - Clinical/therapeutic interview
        - Academic interview
        - Podcast/informal conversation
        - Other (specify)
        
        TRANSCRIPT:
        {sample_text}
        
        Respond only with the identified type:
        """

        response = self._call_ollama(prompt, system_prompt)
        return response.strip()

    def extract_main_insights(self, text: str) -> List[str]:
        """Extracts the main insights from the interview"""
        system_prompt = "You are an expert in qualitative interview analysis."

        prompt = f"""
        Analyze the following interview transcript and identify the 5-7 most important or revealing insights.
        
        INSTRUCTIONS:
        - Look for key ideas, revelations, unique points of view
        - Include important conclusions from the interviewee
        - Identify recurring patterns or themes
        - Focus on the most valuable or surprising
        
        TRANSCRIPT:
        {text[:3000]}...
        
        MAIN INSIGHTS (one per line):
        """

        response = self._call_ollama(prompt, system_prompt)
        insights = [
            line.strip().lstrip("- •*1234567890.")
            for line in response.split("\n")
            if line.strip()
        ]
        return insights[:7]

    def extract_highlight_quotes(self, text: str) -> List[str]:
        """Extracts the most outstanding quotes from the interview"""
        system_prompt = (
            "You are an expert in identifying impactful and memorable quotes."
        )

        prompt = f"""
        From the following interview transcript, identify the 5-8 most impactful, revealing, or memorable quotes.
        
        CRITERIA:
        - Phrases that summarize key points
        - Surprising or controversial statements  
        - Inspirational or emotional quotes
        - Phrases that capture the essence of the message
        
        TRANSCRIPT:
        {text[:4000]}...
        
        Present each quote in quotation marks, one per line:
        """

        response = self._call_ollama(prompt, system_prompt)
        quotes = [
            line.strip().strip('"').strip("'")
            for line in response.split("\n")
            if line.strip() and ('"' in line or "'" in line)
        ]
        return quotes[:8]

    def analyze_question_themes(self, text: str) -> List[str]:
        """Analyzes the themes of the questions asked"""
        system_prompt = (
            "You are an expert in interview analysis and questioning techniques."
        )

        # Try to identify questions in the text
        question_patterns = re.findall(r"[¿?][^¿?]*[?¿]", text)
        questions_text = " ".join(question_patterns[:20])  # First 20 questions

        if not questions_text:
            # If there are no clear question patterns, analyze general themes
            questions_text = text[:2000]

        prompt = f"""
        Analyze the questions or topics addressed in this interview and identify the 5-6 main thematic areas.
        
        QUESTIONS/CONTENT:
        {questions_text}
        
        THEMATIC AREAS (one per line):
        """

        response = self._call_ollama(prompt, system_prompt)
        themes = [
            line.strip().lstrip("- •*1234567890.")
            for line in response.split("\n")
            if line.strip()
        ]
        return themes[:6]

    def analyze_interaction_style(self, text: str) -> str:
        """Analyzes the interaction style in the interview"""
        sample_text = text[:2000]

        system_prompt = (
            "You are an expert in communication analysis and interpersonal dynamics."
        )

        prompt = f"""
        Analyze the interaction style and communication dynamics in this interview:
        
        ASPECTS TO CONSIDER:
        - Formality vs informality
        - Confrontational vs collaborative  
        - Directive vs exploratory
        - Tense vs relaxed
        
        TRANSCRIPT SAMPLE:
        {sample_text}
        
        Describe the style in 2-3 key words:
        """

        response = self._call_ollama(prompt, system_prompt)
        return response.strip()

    def estimate_interview_duration(self, text: str) -> int:
        """Estimates the duration of the interview in minutes"""
        word_count = len(text.split())
        # Average: ~150-180 words per minute in conversation
        estimated_minutes = max(1, word_count // 165)
        return estimated_minutes

    def analyze_interview(self, text: str) -> InterviewAnalysis:
        """Performs a complete analysis specific to interviews"""
        print("🎤 Starting specialized interview analysis...")

        # Base analysis
        base_analysis = self.analyze_text(text)

        print("🔍 Identifying interview type...")
        interview_type = self.identify_interview_type(text)

        print("💡 Extracting main insights...")
        main_insights = self.extract_main_insights(text)

        print("💬 Identifying highlight quotes...")
        quotes_highlights = self.extract_highlight_quotes(text)

        print("❓ Analyzing question themes...")
        questions_themes = self.analyze_question_themes(text)

        print("🤝 Evaluating interaction style...")
        interaction_style = self.analyze_interaction_style(text)

        print("⏱️ Estimating duration...")
        duration_estimate = self.estimate_interview_duration(text)

        return InterviewAnalysis(
            # Inherited fields
            keywords=base_analysis.keywords,
            summary=base_analysis.summary,
            key_topics=base_analysis.key_topics,
            sentiment=base_analysis.sentiment,
            word_count=base_analysis.word_count,
            reading_time=base_analysis.reading_time,
            speakers=base_analysis.speakers,
            # Interview-specific fields
            interview_type=interview_type,
            main_insights=main_insights,
            quotes_highlights=quotes_highlights,
            questions_themes=questions_themes,
            interaction_style=interaction_style,
            duration_estimate=duration_estimate,
        )

    def save_interview_report(self, analysis: InterviewAnalysis, output_file: str):
        """Saves the specialized interview analysis"""
        report = f"""
# INTERVIEW ANALYSIS REPORT

## 📊 GENERAL INFORMATION
- **Interview type**: {analysis.interview_type}
- **Estimated duration**: {analysis.duration_estimate} minutes
- **Word count**: {analysis.word_count:,}
- **Interaction style**: {analysis.interaction_style}
- **Overall sentiment**: {analysis.sentiment}

{'## 👥 PARTICIPANTS' + chr(10) + chr(10).join([f"• {speaker}" for speaker in analysis.speakers]) + chr(10) if analysis.speakers else ''}

## 💡 MAIN INSIGHTS
{chr(10).join([f"• {insight}" for insight in analysis.main_insights])}

## 💬 HIGHLIGHT QUOTES
{chr(10).join([f'• "{quote}"' for quote in analysis.quotes_highlights])}

## ❓ QUESTION/DISCUSSION THEMES
{chr(10).join([f"• {theme}" for theme in analysis.questions_themes])}

## 🎯 KEYWORDS
{', '.join(analysis.keywords)}

## 🏷️ MAIN IDENTIFIED TOPICS
{chr(10).join([f"• {topic}" for topic in analysis.key_topics])}

## 📋 EXECUTIVE SUMMARY

{analysis.summary}

---
*Report generated with Interview Analyzer - Ollama specialized module*
        """

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(report.strip())

        print(f"📄 Interview report saved to: {output_file}")


def main():
    parser = argparse.ArgumentParser(
        description="Specialized interview analyzer with Ollama"
    )
    parser.add_argument("input_file", help="Transcript file to analyze")
    parser.add_argument("-o", "--output", help="Output file for the report")
    parser.add_argument("-m", "--model", default="llama3.1", help="Ollama model to use")
    parser.add_argument(
        "--url", default="http://localhost:11434", help="Ollama server URL"
    )

    args = parser.parse_args()

    # Check file
    input_path = Path(args.input_file)
    if not input_path.exists():
        print(f"❌ Error: File {args.input_file} not found")
        sys.exit(1)

    # Read transcript
    try:
        with open(input_path, "r", encoding="utf-8") as f:
            text = f.read()
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        sys.exit(1)

    # Create analyzer
    analyzer = InterviewAnalyzer(model_name=args.model, ollama_url=args.url)

    try:
        # Perform analysis
        analysis = analyzer.analyze_interview(text)

        # Show results
        print("\n" + "=" * 60)
        print("🎤 INTERVIEW ANALYSIS COMPLETED")
        print("=" * 60)

        print(f"\n📊 GENERAL INFORMATION:")
        print(f"  • Type: {analysis.interview_type}")
        print(f"  • Estimated duration: {analysis.duration_estimate} min")
        print(f"  • Style: {analysis.interaction_style}")
        print(f"  • Sentiment: {analysis.sentiment}")

        if analysis.speakers:
            print(f"\n👥 PARTICIPANTS:")
            for speaker in analysis.speakers:
                print(f"  • {speaker}")

        print(f"\n💡 KEY INSIGHTS:")
        for insight in analysis.main_insights[:3]:
            print(f"  • {insight}")

        print(f"\n💬 HIGHLIGHT QUOTES:")
        for quote in analysis.quotes_highlights[:2]:
            print(f'  • "{quote[:100]}..."')

        # Save report
        if args.output:
            analyzer.save_interview_report(analysis, args.output)
        else:
            output_file = input_path.stem + "_interview_analysis.md"
            analyzer.save_interview_report(analysis, output_file)

        print(f"\n✅ Interview analysis completed successfully")

    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
