# 🖥️ Module 4 – CESGA FinisTerrae III Cluster Execution

Run your LLM extraction scripts on **CESGA FinisTerrae III**, first interactively on a GPU node and then as a batch job.

---

## 🎯 Goal

You will process multiple reviews using an LLM and save structured outputs to a CSV.

---

## 1. 📥 Clone the Repository

SSH into CESGA:

```bash
ssh your_user@ft3.cesga.es
```

Clone the repository:

```bash
git clone git@github.com:javiervela/llm-information-extraction-workshop.git
cd llm-information-extraction-workshop
```

---

## 2. ⚙️ Prepare the Environment

### **2.1 Configure Storage for Ollama & Poetry**

```bash
mkdir -p $LUSTRE/.ollama
ln -sfn $LUSTRE/.ollama $HOME/.ollama

mkdir -p $STORE/.cache/pypoetry
mkdir -p $HOME/.cache
ln -sfn $STORE/.cache/pypoetry $HOME/.cache/pypoetry
```

### **2.2 Load Required Modules**

```bash
module load cesga/2022 ollama/0.6.4 python/3.10.8
```

Check versions:

```bash
python --version
ollama --version
```

Expected output:

```txt
Python 3.10.8
Warning: could not connect to a running Ollama instance
Warning: client version is 0.6.4
```

---

## 3. 🧪 Interactive Test Run (GPU Node)

### **3.1 Start a GPU Session**

Request an interactive GPU node:

```bash
compute --gpu
```

Check available GPUs:

```bash
nvidia-smi
```

### **3.2 Start the Ollama Server**

Set environment variables and start the server:

```bash
module load cesga/2022 ollama/0.6.4 python/3.10.8

export OLLAMA_HOST="127.0.0.1:11433"
export OLLAMA_TMPDIR=$TMPDIR

ollama serve &
```

Confirm it’s running:

```bash
ollama pull qwen2.5
ollama list
ollama run qwen2.5 "Hello"
```

### **3.3 Run the Script**

For the interactive test, run a simple script to check the LLM works correctly.

See [🧑‍💻 `01_test_interactive.py`](./01_test_interactive.py) — This script:

- Prompts the LLM to return a simple fact.
- Prints the response.

Run it:

```bash
poetry install
poetry run python 04_cluster_execution/01_test_interactive.py
```

✅ **Expected output:**

```txt
Model response: 'Pride and Prejudice' was written by Jane Austen.
```

---

## 4. 🧾 Batch Job Submission

### **4.1 Example Batch Script: `run_batch.sh`**

See [🧑‍💻 `run_batch.sh`](./run_batch.sh) — This script:

- Starts the Ollama server.
- Handles retries if the server is not ready.
- Runs the LLM extraction script.

### **4.2 Submit the Job**

Submit the batch job:

```bash
sbatch run_batch.sh
```

✅ **Tip:** You can also pass SBATCH options directly:

```bash
sbatch --mail-type=END --mail-user=youremail@example.com run_batch.sh
```

---

## 🔗 Navigation

⬅ [Back to Structured Extraction](../03_structured_llm_extraction/README.md)
