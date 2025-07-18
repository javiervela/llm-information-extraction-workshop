
# 💻 Module 2 – Basic LLM Extraction

Learn to run basic LLM jobs locally using **Ollama**. You will query single inputs and process batches using prompt templates.

---

## 🎯 Goal

You will write scripts that interact with LLMs, process files, and save responses.

---

## 1. 📦 Running Your First Local LLM Script

### **1.1 What You’ll Do**

Run a Python script that asks the LLM a simple question and prints the response.

### **1.2 Example Script**

See [`01_simple_extractor.py`](./01_simple_extractor.py).
This script sends a simple question to the LLM and prints the response.

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

### **2.1 What You’ll Do**

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

See [`02_batch_query.py`](./02_batch_query.py).

# TODO explain what the script does. add emojis to script links 

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

## 🔗 Navigation

⬅ [Back to Setup](../01_setup/README.md) | ➡ [Next Module: Structured LLM Extraction](../03_structured_llm_extraction/README.md)

# TODO add a overview of what we have done


---
