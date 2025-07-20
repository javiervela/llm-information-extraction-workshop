# 🧩 Module 3 – Structured LLM Extraction

## 🎯 Goal

**Extract structured information from book reviews with reliable validation:**

- Start with manual JSON parsing to understand basic extraction.
- Switch to **Pydantic** models for robust data validation.
- Ensure all outputs are correctly formatted before saving.

---

## 🔍 Manual JSON vs Pydantic

When extracting structured data from LLMs, you have two main approaches: manual JSON parsing and schema-based validation with Pydantic. Each has its strengths and trade-offs:

| Method          | Pros                                             | Cons                                                      |
| --------------- | ------------------------------------------------ | --------------------------------------------------------- |
| **Manual JSON** | Simple and quick to implement                    | Fails silently if output is malformed; no type validation |
| **Pydantic**    | Ensures well-formed and valid data before saving | Requires defining a schema                                |

**Manual JSON Parsing:**  
This approach is fast and easy to set up. You simply ask the LLM for JSON and parse it with `json.loads()`. However, if the LLM returns malformed or unexpected data, your code may break or, worse, accept invalid data without warning. There’s no guarantee that types or required fields are correct.

**Pydantic Validation:**  
Pydantic lets you define a schema for your expected data. When you validate LLM output against this schema, you catch errors early—missing fields, wrong types, or malformed structures. This makes your extraction pipeline much more robust and reliable, especially as you scale to batch processing or more complex data.

**Ollama Library Integration:**  
The Ollama library supports automatic validation of LLM responses against Pydantic models. This means you can directly enforce schema validation as part of your workflow, reducing manual checks and further improving reliability.

**Why Pydantic?**  
_"Pydantic ensures the LLM outputs are well-formed and valid before saving."_  
By enforcing a schema, you reduce bugs, improve data quality, and make downstream processing safer and easier.

---

## 1. 📦 Basic Manual JSON Parsing

You will prompt the LLM to return structured JSON explicitly and parse it manually with `json.loads()`. This is the simplest approach and shows why better validation is needed.

### **1.1 Example Script**

The script </> [`01_structured_basic.py`](./01_structured_basic.py) does the following:

- Builds a prompt explicitly requesting JSON.
- Calls the LLM and manually parses the JSON with `json.loads()`.
- Prints the parsed dictionary or an error if the output isn’t valid JSON.

### **1.2 Run the Script**

Make sure your Ollama server is running (`ollama serve`). Then execute:

```bash
poetry run python 03_structured_llm_extraction/01_structured_basic.py
```

✅ **Expected output:**

```txt
Parsed data: {'title': 'The Hobbit', 'author': 'J.R.R. Tolkien', 'genre': ['fantasy', 'adventure'], 'publication_year': 1937, 'sentiment_positive': True}
```

---

## 2. ✅ Single Review with Pydantic Validation

You will use a **Pydantic model** to ensure the LLM returns correctly structured data.

### **2.1 Example Script**

The script </> [`02_structured_single_validated.py`](./02_structured_single_validated.py) does the following:

- Defines a `BookReview` Pydantic model.
- Uses `format=BookReview.model_json_schema()` to guide the LLM.
- Validates the response with `model_validate_json()` and prints the structured object.

### **2.2 Run the Script**

Make sure your Ollama server is running (`ollama serve`). Then execute:

```bash
poetry run python 03_structured_llm_extraction/02_structured_single_validated.py
```

✅ **Expected output:**

```txt
Parsed data: title='1984' author='George Orwell' genre=['dystopian', 'political fiction'] publication_year=1949 sentiment_positive=True
```

---

## 3. 📊 Batch Processing Reviews & Saving to CSV

You will process multiple reviews, validate each, save valid entries to a CSV, and log invalid ones.

### **3.1 Input File**

The file `data/book_reviews.txt` is already provided in the repository and contains:

```txt
I loved Tolkien’s fantasy classic 'The Hobbit', first published in 1937. Such a charming adventure!
George Orwell’s '1984' is a chilling dystopian masterpiece from 1949 that feels frighteningly relevant today.
Jane Austen’s 'Pride and Prejudice' is a timeless romantic classic that brilliantly critiques social norms.
```

### **3.2 Example Script**

This script </> [`03_structured_batch_validated.py`](./03_structured_batch_validated.py) does the following:

- Reads reviews from the input file.
- Validates each response with Pydantic.
- Saves valid entries to a CSV file and logs invalid ones to a separate error file.

### **3.3 Run the Script**

Make sure your Ollama server is running (`ollama serve`). Then execute:

```bash
poetry run python 03_structured_llm_extraction/03_structured_batch_validated.py
```

✅ **Expected output:**

```txt
Saved 3 valid entries to data/book_reviews_response.csv and logged 0 errors.
```

The generated CSV will look similar to:

```csv
title,author,genre,publication_year,sentiment_positive
The Hobbit,J.R.R. Tolkien,"['fantasy', 'adventure']",1937,True
1984,George Orwell,"['dystopian', 'political fiction']",1949,True
Pride and Prejudice,Jane Austen,"['romance', 'classic']",1813,True
```

---

## 📝 Module Recap

- Compared manual JSON parsing with Pydantic validation for extracting structured data.
- Implemented basic extraction using `json.loads()` to highlight common pitfalls.
- Defined and used a **Pydantic** model for robust validation of LLM outputs.
- Processed and validated multiple book reviews in batch, saving results to CSV and logging errors.

---

## 🔗 Navigation

⬅ [Module 2: Basic LLM Extraction](../02_basic_llm_extraction/README.md) | 🏠 [Home](../README.md) | ➡ [Module 4: CESGA Cluster Execution](../04_cluster_execution/README.md)
