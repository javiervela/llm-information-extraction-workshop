import ollama
from ollama import ChatResponse
from pydantic import BaseModel, ValidationError
from typing import List
import csv

# Define the input, output, and error log files
INPUT_FILE = "data/book_reviews.txt"
OUTPUT_CSV = "data/book_reviews_response.csv"
ERROR_LOG = "data/book_reviews_response_errors.txt"

# Define the model and prompt template
MODEL_NAME = "gemma3"
PROMPT_TEMPLATE = "Extract the book information from this review: {review}. "


# Define the Pydantic model for structured output
class BookReview(BaseModel):
    title: str
    author: str
    genre: List[str]
    publication_year: int
    sentiment_positive: bool


# Read reviews from file
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    reviews = [line.strip() for line in f if line.strip()]

valid_entries = []
errors = []

for review in reviews:
    # Format the prompt using the template
    PROMPT = PROMPT_TEMPLATE.format(review=review)

    try:
        # Send the prompt to the LLM and get the response
        response: ChatResponse = ollama.chat(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": PROMPT}],
            format=BookReview.model_json_schema(),
        )

        # Extract the content from the response
        content = response["message"]["content"]
        valid_entries.append(BookReview.model_validate_json(content))

    except ValidationError as e:
        errors.append((review, str(e)))

# Save valid entries to CSV
with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=BookReview.model_fields.keys())
    writer.writeheader()
    for entry in valid_entries:
        writer.writerow(entry.model_dump())

# Log errors
with open(ERROR_LOG, "w", encoding="utf-8") as f:
    for r, e in errors:
        f.write(f"Review: {r}\nError: {e}\n---\n")

print(f"Parsed responses saved to {OUTPUT_CSV}.")
print(f"Logged {len(errors)} errors.")
