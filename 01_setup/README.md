# 🛠️ Module 1 – Setup & Environment

## 🎯 Goal

**Set up your local environment for LLM extraction:**

- Install **Ollama** for local LLM serving.
- Verify your **Python** and **Poetry** setup for dependency management.
- Confirm access to the **CESGA FinisTerrae III** cluster for remote computation.

---

## 1. 🤖 Install and Test Ollama

### **1.1 Install Ollama**

Follow the official instructions for your OS:
[https://ollama.com/download](https://ollama.com/download)

Start the Ollama server:

```bash
ollama serve
```

✅ **If running correctly:** You will see logs confirming the server is listening locally.

⚠ **If the default port is already in use:** run:

```bash
export OLLAMA_HOST=127.0.0.1:11433  # Change to any free port
ollama serve
```

---

### **1.2 Explore & Pull Models**

Browse available models: [https://ollama.com/library](https://ollama.com/library)

Example with **Gemma 3**:

```bash
ollama pull gemma3
ollama list
ollama run gemma3
```

Exit interactive mode with `Ctrl+D`.

---

## 2. 🐍 Python & Poetry Setup

### **2.1 Python Version**

Ensure you have **Python 3.10 or higher**:

```bash
python --version
```

If not, install the latest version from [https://www.python.org](https://www.python.org).

### **2.2 Install Poetry**

We use **Poetry** for dependency management. Install it with:

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

Check installation:

```bash
poetry --version
```

### **2.3 Install Dependencies**

From the repo root, install all dependencies:

```bash
poetry install
```

### **2.4 Running Python Commands with Poetry**

You can run scripts using:

```bash
poetry run python your_script.py
```

Or activate the Poetry shell for convenience:

```bash
poetry shell
python your_script.py
```

### **2.5 Ollama Python**

For Python integration, this course uses the **Ollama Python library**: [https://github.com/ollama/ollama-python](https://github.com/ollama/ollama-python).

This library lets you:

- Interact with the Ollama server directly from Python code.
- Send prompts and receive responses programmatically.

To verify your setup, run the provided test script:

```bash
poetry run python 01_setup/test_ollama.py
```

If successful, you’ll see a greeting from the model.

#### 🛠️ Alternatives

- **Direct API requests:** You can use Python’s `requests` or similar libraries to call Ollama’s REST API, but this requires manual handling of endpoints and payloads.
- **Frameworks:** Advanced frameworks like LangChain or LlamaIndex offer powerful orchestration and chaining, but may be overkill for simple tasks.

For most workshop exercises, the Ollama Python library is the simplest and most convenient option.

---

## 3. 🌐 Access the CESGA FinisTerrae III Cluster

SSH into the cluster:

```bash
ssh your_user@ft3.cesga.es
```

To simplify connections, add to `~/.ssh/config`:

```ssh
Host cesga
    HostName ft3.cesga.es
    User your_user
    PubkeyAuthentication yes
    IdentityFile ~/.ssh/id_rsa
```

Now you can connect with:

```bash
ssh cesga
```

---

## 📝 Module Recap

- Installed and tested **Ollama** for local LLM serving.
- Explored and pulled models from the Ollama library.
- Verified your **Python** version and installed **Poetry** for dependency management.
- Integrated Python with Ollama using the official library.
- Connected to the **CESGA FinisTerrae III cluster** via SSH for remote computation.

---

## 🔗 Navigation

🏠 [Home](../README.md) | ➡ [Module 2: Basic LLM Extraction](../02_basic_llm_extraction/README.md)
