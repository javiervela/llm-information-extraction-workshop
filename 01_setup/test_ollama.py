import ollama

try:
    response = ollama.chat(
        model="gemma3",
        messages=[{"role": "user", "content": "Say hello!"}],
    )
    print("Ollama is working correctly.")
    print("Model response:\n", response["message"]["content"])
except Exception as e:
    print("There was a problem communicating with Ollama:", e)
