import ollama
import json
import re

MODEL_NAME = "gemma3"
REVIEW = "I loved Tolkien's fantasy classic 'The Hobbit', first published in 1937. Such a charming adventure!"

# Define the prompt template separately
PROMPT_TEMPLATE = (
    "Extract the book information from this review: {review}. "
    "Return ONLY JSON with the following keys: title, author, "
    "genre (as a list of strings), publication_year (integer), "
    "and sentiment_positive (boolean, true if positive sentiment, false if negative)."
)

# Format the prompt using the template
PROMPT = PROMPT_TEMPLATE.format(review=REVIEW)

# Send the prompt to the LLM and get the response
response = ollama.chat(
    model=MODEL_NAME,
    messages=[{"role": "user", "content": PROMPT}],
)
content = response["message"]["content"]

# Remove code block markers if present
match = re.search(r"```(?:json)?\s*(.*?)\s*```", content, re.DOTALL)
if match:
    content = match.group(1)

try:
    # Parse the JSON response from the model
    data = json.loads(content)
    print("Parsed data:", data)
except json.JSONDecodeError:
    print("The response was not valid JSON:", response["message"]["content"])
