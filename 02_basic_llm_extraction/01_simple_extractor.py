import ollama
from ollama import ChatResponse

# Define the model and prompt
MODEL_NAME = "gemma3"
PROMPT = "Who is the author of 'Pride and Prejudice'?"

# Send the prompt to the LLM and get the response
response: ChatResponse = ollama.chat(
    model=MODEL_NAME,
    messages=[{"role": "user", "content": PROMPT}],
)

# Extract the content from the response and print it
content = response["message"]["content"]
print("Model response:\n", content)
