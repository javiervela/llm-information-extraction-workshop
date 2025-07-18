import ollama

MODEL_NAME = "gemma3"
INPUT_FILE = "data/book_names.txt"
OUTPUT_FILE = "data/book_authors_response.txt"

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
    prompt = PROMPT_TEMPLATE.format(book=book)
    response = ollama.chat(
        model=MODEL_NAME, messages=[{"role": "user", "content": prompt}]
    )
    # TODO ENSURE CONSISTENR FORMATTING
    # TODO print in all execrrcises results
    answer = response["message"]["content"]
    responses[book] = answer
    print(f"{book}: {answer}")


# Save responses to the output file
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    for book, answer in responses.items():
        f.write(f"{book}: {answer}\n")

print(f"All responses saved to {OUTPUT_FILE}")
