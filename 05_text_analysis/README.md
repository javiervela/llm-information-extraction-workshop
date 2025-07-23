# 📚 Module 5 – Long Text Analysis

This module extends the information extraction workshop with specialized capabilities for analyzing long texts and interview transcripts using local LLM models with Ollama.

## 🚀 Features

### General Analyzer (`long_text_analyzer.py`)

- **Long text processing**: Handles large documents by splitting content into manageable chunks
- **Keyword extraction**: Identifies the most relevant terms and phrases
- **Detailed summary**: Generates comprehensive syntheses while retaining crucial information
- **Thematic analysis**: Identifies main topics and content structure
- **Sentiment analysis**: Assesses the overall emotional tone
- **Speaker detection**: Identifies participants in transcripts
- **Statistics**: Word count and estimated reading time

### Specialized Interview Analyzer (`interview_analyzer.py`)

- **Interview classification**: Identifies the type (job, journalistic, academic, etc.)
- **Insight extraction**: Finds key revelations and points
- **Highlighted quotes**: Identifies impactful and memorable statements
- **Question analysis**: Categorizes topics of the questions asked
- **Interaction style**: Evaluates communication dynamics
- **Duration estimation**: Calculates approximate interview time

## 🎯 Usage

### General Long Text Analysis

```bash
# Basic analysis
python long_text_analyzer.py my_document.txt

# Specify output file
python long_text_analyzer.py transcript.txt -o analysis_report.md

# Use specific model
python long_text_analyzer.py document.txt -m mixtral

# Custom Ollama server
python long_text_analyzer.py text.txt --url http://192.168.1.100:11434
```

### Specialized Interview Analysis

```bash
# Interview analysis
python interview_analyzer.py interview.txt

# With custom output file
python interview_analyzer.py interview_transcript.txt -o interview_analysis.md
```

## 📄 Input Formats

### Plain Text

```
This is a long document we want to analyze...
The content may include multiple paragraphs...
```

### Interview Transcript

```
INTERVIEWER: What is your experience in the field?

INTERVIEWEE: Well, I have worked for over 10 years...

INTERVIEWER: Interesting, could you tell me more about...
```

## 📊 Example Output

### General Report

```markdown
# LONG TEXT ANALYSIS REPORT

## 📊 GENERAL STATISTICS

- **Word count**: 2,547
- **Estimated reading time**: 13 minutes
- **Overall sentiment**: Neutral

## 🎯 KEYWORDS

artificial intelligence, machine learning, data, algorithms, technology

## 🏷️ MAIN TOPICS

• Development of artificial intelligence
• Impact on the tech industry
• Ethical and regulatory challenges
• Future of automation

## 📋 DETAILED SUMMARY

The document discusses recent advances in artificial intelligence...
```

### Interview Report

```markdown
# INTERVIEW ANALYSIS REPORT

## 📊 GENERAL INFORMATION

- **Interview type**: Job interview
- **Estimated duration**: 25 minutes
- **Interaction style**: Formal collaborative

## 💡 MAIN INSIGHTS

• The candidate has solid experience in backend development
• Shows genuine interest in continuous learning
• Highlights teamwork skills

## 💬 HIGHLIGHTED QUOTES

• "My passion for technology drives me to always stay up to date"
• "I believe collaboration is key to the success of any project"
```

## ⚙️ Advanced Configuration

### Customize Model Parameters

You can modify the parameters in the code:

```python
analyzer = LongTextAnalyzer(
    model_name="llama3.1",
    ollama_url="http://localhost:11434"
)

# Customize call parameters
payload = {
    "model": self.model_name,
    "prompt": prompt,
    "options": {
        "temperature": 0.1,      # Creativity (0.0-1.0)
        "top_p": 0.9,           # Token diversity
        "num_ctx": 8192         # Context window
    }
}
```

### Adjust Chunk Size

```python
# In the LongTextAnalyzer class
self.max_chunk_size = 4000  # Adjust according to the model
```

## 🚨 Troubleshooting

### Ollama Connection Error

```bash
# Check that Ollama is running
ollama list

# Start Ollama if stopped
ollama serve
```

### Model Not Found

```bash
# List available models
ollama list

# Download required model
ollama pull llama3.1
```

### Insufficient Memory

- Use smaller models: `llama3.2:1b`
- Reduce `max_chunk_size` in the code
- Process shorter texts

### Slow Analysis

- Use faster but less accurate models
- Reduce chunk size
- Process in parallel (advanced modification)

## 🔄 Integration with the Workshop

This module integrates seamlessly with the existing workshop:

```python
# Example usage in a custom script
from long_text_analyzer import LongTextAnalyzer
from interview_analyzer import InterviewAnalyzer

# General analysis
analyzer = LongTextAnalyzer(model_name="llama3.1")
analysis = analyzer.analyze_text(long_text)

# Specialized analysis
interview_analyzer = InterviewAnalyzer(model_name="llama3.1")
interview_analysis = interview_analyzer.analyze_interview(transcript)
```

## 🎨 Use Cases

### Academic Research

- Analysis of focus group transcripts
- Summarizing long research documents
- Extracting topics from qualitative interviews

### Journalism and Media

- Analysis of journalistic interviews
- Summarizing press conferences
- Extracting highlighted quotes

### Human Resources

- Analysis of job interviews
- Evaluation of employee feedback
- Processing open-ended surveys

### Consulting and Business

- Analysis of meeting transcripts
- Processing customer feedback
- Summarizing corporate documents

## 🛠️ Extensibility

The module is designed to be extensible:

```python
# Create a custom analyzer
class CustomAnalyzer(LongTextAnalyzer):
    def custom_analysis(self, text: str):
        # Implement specific analysis
        pass
```

## 📈 Future Improvements

- [ ] Support for multiple languages
- [ ] More granular emotion analysis
- [ ] Automatic detection of emerging topics
- [ ] Integration with databases
- [ ] REST API for remote use
- [ ] Web interface for interactive analysis

## 🔗 Navigation

⬅ [Module 4: Cluster Execution](../04_cluster_execution/README.md) | 🏠 [Home](../README.md)
