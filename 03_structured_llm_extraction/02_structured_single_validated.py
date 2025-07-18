import ollama
from ollama import ChatResponse
from pydantic import BaseModel
from typing import List

MODEL_NAME = "gemma3"
REVIEW = "George Orwell’s '1984' is a chilling dystopian masterpiece from 1949 that feels frighteningly relevant today."

# Define the prompt template separately
PROMPT_TEMPLATE = "Extract the book information from this review: {review}. "

# Format the prompt using the template
PROMPT = PROMPT_TEMPLATE.format(review=REVIEW)


class BookReview(BaseModel):
    title: str
    author: str
    genre: List[str]
    publication_year: int
    sentiment_positive: bool


response: ChatResponse = ollama.chat(
    model=MODEL_NAME,
    messages=[{"role": "user", "content": PROMPT}],
    format=BookReview.model_json_schema(),
)

print("Model response:")
print(response["message"]["content"])

book_review = BookReview.model_validate_json(response["message"]["content"])
print("\nParsed response:")
print(book_review)
