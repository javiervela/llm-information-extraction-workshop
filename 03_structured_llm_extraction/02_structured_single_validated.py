import ollama
from ollama import ChatResponse
from pydantic import BaseModel
from typing import List

# Define the model, review, and prompt template
MODEL_NAME = "gemma3"
REVIEW = "George Orwell's '1984' is a chilling dystopian masterpiece from 1949 that feels frighteningly relevant today."
PROMPT_TEMPLATE = "Extract the book information from this review: {review}. "

# Format the prompt using the template
PROMPT = PROMPT_TEMPLATE.format(review=REVIEW)


# Define the Pydantic model for structured output
class BookReview(BaseModel):
    title: str
    author: str
    genre: List[str]
    publication_year: int
    sentiment_positive: bool


# Send the prompt to the LLM and get the response
response: ChatResponse = ollama.chat(
    model=MODEL_NAME,
    messages=[{"role": "user", "content": PROMPT}],
    format=BookReview.model_json_schema(),
)

# Extract the content from the response
content = response["message"]["content"]

print("Model response:\n", content)

book_review = BookReview.model_validate_json(content)
print("\nParsed data:\n", book_review)
