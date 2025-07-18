import ollama

MODEL_NAME = "qwen2.5"
PROMPT = "Who is the author of 'Pride and Prejudice'?"

response = ollama.chat(
    model=MODEL_NAME,
    messages=[{"role": "user", "content": PROMPT}],
)

print("Model response:", response["message"]["content"])