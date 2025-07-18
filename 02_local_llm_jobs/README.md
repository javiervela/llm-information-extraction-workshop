# 💻 Module 2 – Local LLM Jobs (Basics)

## 🎯 Goal

Learn to run basic and slightly advanced LLM jobs locally using the **Ollama Python client**, including prompt templates, reading prompts from a file, and saving responses.

---

## 1. 📦 Running Your First Local LLM Script

### **1.1 What You’ll Do**

You will run a Python script that asks the **Gemma 3** model a simple question and prints the response.

### **1.2 Example Script**

See [🧑‍💻 `01_simple_extractor.py`](./01_simple_extractor.py) — This script sends a prompt to the model and prints the answer.

### **1.3 Run the Script**

Make sure your Ollama server is running (`ollama serve`). Then execute:

```bash
poetry run python 02_local_llm_jobs/01_simple_extractor.py
```

You should see an answer similar to:

```txt
Model response: 'Pride and Prejudice' was written by Jane Austen.
```

---

## 2. 🗂️ Advanced Exercise: Batch Processing with Prompt Templates

### **2.1 What You’ll Do**

You will:

1. Read a list of book titles from a file.
2. Use a prompt template to ask for author, genre, and year of publication.
3. Query the model for each prompt.
4. Save all responses in an output file.

### **2.2 Input File**

The file `data/book_names.txt` is already provided in the repository and contains:

```txt
Pride and Prejudice
1984
The Hobbit
```

### **2.3 Example Script**

See [🧑‍💻 `02_batch_query.py`](./02_batch_query.py) — This script reads book titles, queries the model for each, and saves the responses to a file.

### **2.4 Run the Script**

Run the script with:

```bash
poetry run python 02_local_llm_jobs/02_batch_query.py
```

You should see the responses printed in the console and saved to `book_names.txt`.

Example output:

```txt
Pride and Prejudice: Written by Jane Austen, it is a classic romance novel first published in 1813.
1984: Written by George Orwell, it is a dystopian political fiction first published in 1949.
The Hobbit: Written by J.R.R. Tolkien, it is a fantasy adventure first published in 1937.
```

---

[⬅ Back to Course Overview](../README.md)

[➡ Next Module: 3: Output Parsing (Advanced)](../03_output_parsing/README.md)
