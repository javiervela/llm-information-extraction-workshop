# 🧩 Module 3 – Structured LLM Extraction

## 🎯 Goal

**Extract structured information from book reviews with reliable validation:**

- Start with manual JSON parsing to understand basic extraction.
- Switch to **Pydantic** models for robust data validation.
- Ensure all outputs are correctly formatted before saving.

---

## 🔍 Manual JSON vs Pydantic

When extracting structured data from LLMs, you can use manual JSON parsing or schema-based validation with Pydantic:

| Method          | Pros                                   | Cons                           |
| --------------- | -------------------------------------- | ------------------------------ |
| **Manual JSON** | Quick to implement                     | No type checks; fails silently |
| **Pydantic**    | Validates structure and types reliably | Requires schema definition     |

**Manual JSON Parsing:**  
Fast and simple—just parse with `json.loads()`. But malformed or unexpected data can slip through, risking errors or silent failures.

**Pydantic Validation:**  
Define a schema and validate LLM output, catching missing fields or wrong types early. This makes extraction robust, especially for batch or complex data.

**Ollama Integration:**  
Ollama can automatically validate LLM responses against Pydantic models, streamlining schema enforcement and improving reliability.

**Why Pydantic?**  
Enforcing a schema reduces bugs, improves data quality, and makes downstream processing safer.

---

## 1. 📦 Basic Manual JSON Parsing

You will prompt the LLM to return structured JSON explicitly and parse it manually with `json.loads()`.

</> **See the script** [`01_structured_basic.py`](./01_structured_basic.py) that does the following:

1. Builds a prompt explicitly requesting JSON.
2. Calls the LLM and manually parses the JSON with `json.loads()`.
3. Prints the parsed dictionary or an error if the output isn’t valid JSON.

🏃‍♂️ **Run the script**:

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

</> **See the script** [`02_structured_single_validated.py`](./02_structured_single_validated.py) that does the following:

1. Defines a `BookReview` Pydantic model.
2. Uses `format=BookReview.model_json_schema()` to guide the LLM.
3. Validates the response with `model_validate_json()` and prints the structured object.

🏃‍♂️ **Run the script**:

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

📄 **See the file** `data/book_reviews.txt` that contains:

```txt
I loved Tolkien’s fantasy classic 'The Hobbit', first published in 1937. Such a charming adventure!
George Orwell’s '1984' is a chilling dystopian masterpiece from 1949 that feels frighteningly relevant today.
Jane Austen’s 'Pride and Prejudice' is a timeless romantic classic that brilliantly critiques social norms.
```

</> **See the script** [`03_structured_batch_validated.py`](./03_structured_batch_validated.py) that does the following:

1. Reads reviews from the input file.
2. Validates each response with Pydantic.
3. Saves valid entries to a CSV file and logs invalid ones to a separate error file.

🏃‍♂️ **Run the script**:

```bash
poetry run python 03_structured_llm_extraction/03_structured_batch_validated.py
```

✅ **Expected output** in CSV file `data/book_reviews_response.csv`:

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
