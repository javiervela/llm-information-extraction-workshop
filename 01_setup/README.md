# 🛠️ Module 1 – Setup & Environment

Ensure you can run LLMs locally with **Ollama** and access the remote **CESGA FinisTerrae III cluster**.

---

## 🎯 Goal

You will install Ollama, verify Python & Poetry, and confirm CESGA access. Completing this module ensures you’re ready for local and cluster-based LLM extractions.

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

The course uses the **Ollama Python library**: [https://github.com/ollama/ollama-python](https://github.com/ollama/ollama-python).

This library allows you to:

- Interact with the Ollama server from Python.
- Send prompts and retrieve responses programmatically.

# TODO OTHER ALTERNATIVES

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

### **2.5 Test Ollama Python Installation**

The script `01_setup/test_ollama.py` is used to verify that the Ollama Python library and the model are working correctly.

Run it:

```bash
poetry run python 01_setup/test_ollama.py
```

If everything is set up, you should see the model respond with a greeting.

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

## 🔗 Navigation

⬅ [Back to Overview](../README.md) | ➡ [Next Module: Basic LLM Extraction](../02_basic_llm_extraction/README.md)
