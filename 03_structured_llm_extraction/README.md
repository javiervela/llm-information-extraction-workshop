
# 🧩 Module 3 – Structured LLM Extraction

Extract **structured information** from book reviews. Start with manual JSON parsing, then switch to **Pydantic** for reliable validation.

---

## 🎯 Goal

Ensure your outputs are correctly formatted before saving them.

---

## 0. 🔍 Manual JSON vs Pydantic

| Method                         | Pros                                               | Cons                                                      |
| ------------------------------ | -------------------------------------------------- | --------------------------------------------------------- |
| **Manual JSON (`json.loads`)** | Simple and quick to implement                      | Fails silently if output is malformed; no type validation |
| **Pydantic**                   | ✅ Ensures well-formed and valid data before saving | Requires defining a schema                                |

**Why Pydantic?**
*"Pydantic ensures the LLM outputs are well-formed and valid before saving."*

---

## 1. 📦 Basic Manual JSON Parsing

### **1.1 What You’ll Do**

You will prompt the LLM to return structured JSON explicitly and parse it manually with `json.loads()`. This is the simplest approach and shows why better validation is needed.

### **1.2 Example Script**

See [🧑‍💻 `01_structured_basic.py`](./01_structured_basic.py) — This script:

- Builds a prompt explicitly requesting JSON.
- Calls the LLM and manually parses the JSON with `json.loads()`.
- Prints the parsed dictionary or an error if the output isn’t valid JSON.

### **1.3 Run the Script**

Make sure your Ollama server is running (`ollama serve`). Then execute:

```bash
poetry run python 03_structured_llm_extraction/01_structured_basic.py
```

✅ **Expected output:**

```txt
Parsed data: {'title': 'The Hobbit', 'author': 'J.R.R. Tolkien', 'genre': ['fantasy', 'adventure'], 'publication_year': 1937, 'sentiment': 'positive'}
```

---

## 2. ✅ Single Review with Pydantic Validation

### **2.1 What You’ll Do**

You will use a **Pydantic model** to ensure the LLM returns correctly structured data.

### **2.2 Example Script**

See [🧑‍💻 `02_structured_single_validated.py`](./02_structured_single_validated.py) — This script:

- Defines a `BookReview` Pydantic model.
- Uses `format=BookReview.model_json_schema()` to guide the LLM.
- Validates the response with `model_validate_json()` and prints the structured object.

### **2.3 Run the Script**

Make sure your Ollama server is running (`ollama serve`). Then execute:

```bash
poetry run python 03_advanced_llm_jobs/02_structured_single_validated.py
```

✅ **Expected output:**

```txt
title='1984' author='George Orwell' genre=['dystopian', 'political fiction'] publication_year=1949 sentiment='positive'
```

---

## 3. 📊 Batch Processing Reviews & Saving to CSV

### **3.1 What You’ll Do**

You will process multiple reviews, validate each, save valid entries to a CSV, and log invalid ones.

### **3.2 Input File**

The file `data/book_reviews.txt` is already provided in the repository and contains:

```txt
I loved Tolkien’s fantasy classic 'The Hobbit', first published in 1937. Such a charming adventure!
George Orwell’s '1984' is a chilling dystopian masterpiece from 1949 that feels frighteningly relevant today.
Jane Austen’s 'Pride and Prejudice' is a timeless romantic classic that brilliantly critiques social norms.
```

### **3.3 Example Script**

See [🧑‍💻 `03_structured_batch_validated.py`](./03_structured_batch_validated.py) — This script:

- Reads reviews from the input file.
- Validates each response with Pydantic.
- Saves valid entries to a CSV file and logs invalid ones to a separate error file.

### **3.4 Run the Script**

Make sure your Ollama server is running (`ollama serve`). Then execute:

```bash
poetry run python 03_advanced_llm_jobs/03_structured_batch_validated.py
```

✅ **Expected output:**

```txt
Saved 3 valid entries to data/book_reviews_response.csv and logged 0 errors.
```

The generated CSV will look similar to:

```csv
title,author,genre,publication_year,sentiment
The Hobbit,J.R.R. Tolkien,"['fantasy', 'adventure']",1937,positive
1984,George Orwell,"['dystopian', 'political fiction']",1949,positive
Pride and Prejudice,Jane Austen,"['romance', 'classic']",1813,positive
```

---

## 🔗 Navigation

⬅ [Back to Basic Extraction](../02_basic_llm_extraction/README.md) | ➡ [Next Module: CESGA Cluster Execution](../04_cluster_execution/README.md)
