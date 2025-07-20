# 🖥️ Module 4 – CESGA FinisTerrae III Cluster Execution

## 🎯 Goal

**Run your LLM extraction scripts on CESGA FinisTerrae III:**

- Set up CESGA access and environment.
- Execute LLM extraction interactively on a GPU node.
- Submit batch jobs for automated processing.

> Check the [CESGA FinisTerrae III documentation](https://cesga-docs.gitlab.io/ft3-user-guide/index.html) for more details on cluster usage and job submission.

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

CESGA uses environment modules to manage software versions, allowing users to easily load and switch between different tools.

> **Note**: The current Ollama version may not support the latest models available in the Ollama library.

If you need a different Ollama version, contact CESGA support at [aplicaciones@cesga.es](mailto:aplicaciones@cesga.es) and specify your requirements.

Load the required modules for this workshop:

```bash
module load cesga/2022 ollama/0.6.4 python/3.10.8
```

Check versions:

```bash
python --version
ollama --version
```

✅ **Expected output:**

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

This script </> [`01_test_interactive.py`](./01_test_interactive.py) does the following:

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

This script </> [`run_batch.sh`](./run_batch.sh) does the following:

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

# TODO put results on file. check resukrs other files like slurm out err and id and others. ollama servrr log

---

## 📝 Module Recap

- Connected to the **CESGA FinisTerrae III cluster** via SSH.
- Cloned the repository, configured Ollama and Poetry storage, and loaded required modules.
- Performed an interactive test run on a GPU node to verify LLM functionality.
- Submitted batch jobs for automated LLM extraction and processing.
- Learned how to monitor job outputs and server logs for troubleshooting.

---

## 🔗 Navigation

⬅ [Module 3: Structured LLM Extraction](../03_structured_llm_extraction/README.md) | 🏠 [Home](../README.md)
