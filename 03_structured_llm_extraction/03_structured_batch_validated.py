import ollama
from ollama import ChatResponse
from pydantic import BaseModel, ValidationError
from typing import List
import csv

MODEL_NAME = "gemma3"

INPUT_FILE = "data/book_reviews.txt"
OUTPUT_CSV = "data/book_reviews_response.csv"
ERROR_LOG = "data/book_reviews_response_errors.txt"

PROMPT_TEMPLATE = "Extract the book information from this review: {review}. "


class BookReview(BaseModel):
    title: str
    author: str
    genre: List[str]
    publication_year: int
    sentiment: str


# Read reviews from file
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    reviews = [line.strip() for line in f if line.strip()]

valid_entries = []
errors = []

for review in reviews:
    # Format the prompt using the template
    PROMPT = PROMPT_TEMPLATE.format(review=review)
    try:
        response: ChatResponse = ollama.chat(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": PROMPT}],
            format=BookReview.model_json_schema(),
        )
        valid_entries.append(
            BookReview.model_validate_json(response["message"]["content"])
        )
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

print(
    f"Saved {len(valid_entries)} valid entries to {OUTPUT_CSV} and logged {len(errors)} errors."
)
