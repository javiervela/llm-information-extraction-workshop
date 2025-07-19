import ollama
from ollama import ChatResponse

# Define the input and output files
INPUT_FILE = "data/book_names.txt"
OUTPUT_FILE = "data/book_authors_response.txt"

# Define the model and prompt template
MODEL_NAME = "gemma3"
PROMPT_TEMPLATE = (
    "Who is the author of the book '{book}', what is its main genre, "
    "and in which year was it first published? "
    "Answer in one concise sentence."
)

# Read book titles from the input file
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    books = [line.strip() for line in f if line.strip()]

responses = {}

# Query the model for each book
total_books = len(books)
for idx, book in enumerate(books, start=1):
    print(f"Processing {idx}/{total_books}: {book}")

    # Format the prompt with the book title
    PROMPT = PROMPT_TEMPLATE.format(book=book)

    # Send the prompt to the LLM and get the response
    response: ChatResponse = ollama.chat(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": PROMPT}],
    )

    # Extract the content from the response
    content = response["message"]["content"]
    responses[book] = content


# Save responses to the output file
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    for book, content in responses.items():
        f.write(f"{book}: {content}\n")

print(f"Responses saved to {OUTPUT_FILE}")
