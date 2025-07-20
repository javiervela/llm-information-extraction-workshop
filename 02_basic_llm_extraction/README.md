# 💻 Module 2 – Basic LLM Extraction

## 🎯 Goal

**Learn to run basic LLM jobs locally using Ollama:**

- Write scripts that **interact with LLMs**
- Process single inputs and **batch queries** using **prompt templates**
- **Save responses** to files

---

## 1. 📦 Running Your First Local LLM Script

You will run a simple Python script that interacts with a local LLM using Ollama.

</> **See the script** [`01_simple_extractor.py`](./01_simple_extractor.py) that does the following:

1. Prompts the LLM to return a simple fact.
2. Prints the response.

🏃‍♂️ **Run the script**:

```bash
poetry run python 02_basic_llm_extraction/01_simple_extractor.py
```

✅ **Expected output:**

```txt
Model response: 'Pride and Prejudice' was written by Jane Austen.
```

---

## 2. 🗂️ Batch Processing with Prompt Templates

You will process multiple inputs using prompt templates to extract structured information from the LLM.

The script expects a plain text file containing a list of book titles.

📄 **See the file** [`data/book_names.txt`](./data/book_names.txt) that looks like:

```txt
Pride and Prejudice
1984
The Hobbit
```

</> **See the script** [`02_batch_query.py`](./02_batch_query.py) that does the following:

1. Reads the book titles from the text file.
2. Uses a prompt template to format the query for each title.
3. Sends the query to the LLM and prints the response.
4. Saves the responses to a file.

🏃‍♂️ **Run the script**:

```bash
poetry run python 02_basic_llm_extraction/02_batch_query.py
```

✅ **Expected output** in TXT file `data/book_authors_response.txt`:

```txt
Pride and Prejudice: Written by Jane Austen, it is a classic romance novel first published in 1813.
1984: Written by George Orwell, it is a dystopian political fiction first published in 1949.
The Hobbit: Written by J.R.R. Tolkien, it is a fantasy adventure first published in 1937.
```

---

## 📝 Module Recap

- Ran your first Python script to interact with a local LLM using Ollama.
- Sent single queries and printed LLM responses.
- Processed multiple inputs using prompt templates for batch extraction.
- Saved structured LLM outputs to files for further analysis.
- Practiced basic automation for local LLM-powered information extraction.

---

## 🔗 Navigation

⬅ [Module 1: Setup & Environment](../01_setup/README.md) | 🏠 [Home](../README.md) | ➡ [Module 3: Structured LLM Extraction](../03_structured_llm_extraction/README.md)

---
