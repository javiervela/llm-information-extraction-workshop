# 💻 Module 2 – Basic LLM Extraction

## 🎯 Goal

**Learn to run basic LLM jobs locally using Ollama:**

- Write scripts that **interact with LLMs**
- Process single inputs and **batch queries** using **prompt templates**
- **Save responses** to files

---

## 1. 📦 Running Your First Local LLM Script

### **1.1 Overview**

Run a Python script that asks the LLM a simple question and prints the response.

### **1.2 Example Script**

The script </> [`01_simple_extractor.py`](./01_simple_extractor.py) does the following:

- Sends a simple question to the LLM
- Prints the response.

### **1.2 Run the Script**

Make sure `ollama serve` is running, then:

```bash
poetry run python 02_basic_llm_extraction/01_simple_extractor.py
```

✅ **Expected output:**

```txt
Model response: 'Pride and Prejudice' was written by Jane Austen.
```

---

## 2. 🗂️ Batch Processing with Prompt Templates

### **2.1 Overview**

1. Read book titles from a file.
2. Use a prompt template to request structured info.
3. Save all responses to an output file.

### **2.2 Input File**

`data/book_names.txt`:

```txt
Pride and Prejudice
1984
The Hobbit
```

### **2.3 Example Script**

The script </> [`02_batch_query.py`](./02_batch_query.py) does the following:

- Reads book titles from a TXT file.
- Uses a prompt template to query the LLM for structured information.
- Saves all responses to an output file.

### **2.4 Run the Script**

```bash
poetry run python 02_basic_llm_extraction/02_batch_query.py
```

✅ **Expected output:**

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
