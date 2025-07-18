# 🛠️ Module 1 – Setup & Environment

## 🎯 Goal

Ensure you can run LLMs locally and access the remote **CESGA FinisTerrae III cluster**.

---

## 1. 🤖 Install and Test Ollama

### **1.1 Install Ollama**

Follow the official instructions for your OS:
[https://ollama.com/download](https://ollama.com/download)

After installation, start the Ollama server (it usually starts automatically):

```bash
ollama serve
```

If it’s running correctly, you should see logs indicating the server is listening locally.

### **1.2 Explore Available Models**

Visit [https://ollama.com/library](https://ollama.com/library) to browse available models.

### **1.3 Pull and Run a Model from the CLI**

Example with **Gemma 3**:

```bash
ollama pull gemma3
ollama list
ollama run gemma3
```

You can then type any question interactively. Exit with `Ctrl+D`.

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

The script `01_setup/test_ollama.py` is used to verify that the Ollama Python library and the model are working correctly:

```python
import ollama

try:
    response = ollama.chat(
        model="gemma3", messages=[{"role": "user", "content": "Say hello!"}]
    )
    print(
        "Ollama is working correctly. Model response:", response["message"]["content"]
    )
except Exception as e:
    print("There was a problem communicating with Ollama:", e)

```

Run it:

```bash
poetry run python 01_setup/test_ollama.py
```

If everything is set up, you should see the model respond with a greeting.

---

## 3. 🌐 Check Access to the CESGA FinisTerrae III Cluster

Ensure you have SSH access:

```bash
ssh your_user@ft3.cesga.es
```

Replace `your_user` with your CESGA username. If successful, you’ll see the welcome banner of the cluster.

You can simplify SSH connections by adding an entry to your SSH config file (`~/.ssh/config`):

```ssh
Host ft3.cesga.es cesga
    HostName ft3.cesga.es
    User your_user
    PubkeyAuthentication yes
    IdentityFile /home/javier/.ssh/id_ed25519
```

Replace `your_user` with your CESGA username. After this, you can connect using:

```bash
ssh cesga
```

---

[⬅ Back to Course Overview](../README.md)

[➡ Next Module: 2: Basic LLM Extraction (Basics)](../02_basic_llm_extraction/README.md)
