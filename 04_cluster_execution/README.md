# 🖥️ Module 4 – CESGA FinisTerrae III Cluster Execution

## 🎯 Goal

**Run your LLM extraction scripts on CESGA FinisTerrae III:**

- Set up CESGA access and environment.
- Execute LLM extraction interactively on a GPU node.
- Submit batch jobs for automated processing.

> Check the [CESGA FinisTerrae III documentation](https://cesga-docs.gitlab.io/ft3-user-guide/index.html) for more details on cluster usage and job submission.

---

## 1. ⚙️ Prepare the Environment

### **1.1 Clone the Repository**

SSH into CESGA:

```bash
ssh your_user@ft3.cesga.es
```

Clone the repository:

```bash
git clone git@github.com:javiervela/llm-information-extraction-workshop.git
cd llm-information-extraction-workshop
```

### **1.2 Configure Storage for Ollama & Poetry**

```bash
mkdir -p $LUSTRE/.ollama
ln -sfn $LUSTRE/.ollama $HOME/.ollama

mkdir -p $STORE/.cache/pypoetry
mkdir -p $HOME/.cache
ln -sfn $STORE/.cache/pypoetry $HOME/.cache/pypoetry
```

> 🗒️ **Note**:
> Having the Poetry storage on the `STORE` filesystem is recommended by CESGA to avoid file system quota issues, but it can slow down the installation process. If you prefer to use the `HOME` filesystem, you can skip this step.

### **1.3 Load Required Modules**

CESGA uses environment modules to manage software versions, allowing users to easily load and switch between different tools.

> 🗒️ **Note**:
> The current Ollama version may not support the latest models available in the Ollama library.
>
> If you need a different Ollama version, contact CESGA support at [aplicaciones@cesga.es](mailto:aplicaciones@cesga.es) and specify your requirements.

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

## 2. 🧪 Interactive Test Run (GPU Node)

We are going to run a simple interactive test to ensure everything is set up correctly before submitting batch jobs.

> 🗒️ **Note**:
> The setup (pulling LLM models) can be done from any login node, but the actual execution of LLM extraction scripts should be done on a GPU node for performance.

### **2.1 Start a GPU Session**

Request an interactive GPU node:

```bash
compute --gpu
```

Check available GPUs:

```bash
nvidia-smi
```

### **2.2 Start the Ollama Server**

Set environment variables and start the server:

```bash
module load cesga/2022 ollama/0.6.4 python/3.10.8

export OLLAMA_HOST="127.0.0.1:11433"
export OLLAMA_TMPDIR=$TMPDIR

ollama serve &
```

> 🗒️ **Note**:
> The Ollama server runs on port `11434` by default. On shared nodes, this port may be busy if another process is already using it. To avoid conflicts, it’s advisable to set the `OLLAMA_HOST` environment variable dynamically, for example by using a port based on your job ID:
>
> ```bash
> export OLLAMA_HOST="127.0.0.1:$((11434 + $SLURM_JOB_ID % 1000))"
> ```
>
> This ensures each job uses a unique port and prevents collisions with other users’ processes.

Confirm it’s running:

```bash
ollama pull qwen2.5
ollama list
ollama run qwen2.5 "Hello"
```

### **2.3 Install Poetry Dependencies**

Install the required Python packages using Poetry:

```bash
poetry install
```

> 🗒️ **Note**:
> If the poetry installation fails, you can try installing in CESGA the latest version of Poetry manually.
>
> To install Poetry manually, run:
>
> ```bash
> curl -sSL https://install.python-poetry.org | python3 -
> alias poetry="$HOME/.local/bin/poetry"
> ```

### **2.4 Run the Script**

For the interactive test, run a simple script to check the LLM works correctly.

</> **See the script** [`01_test_interactive.py`](./01_test_interactive.py) that does the following:

- Prompts the LLM to return a simple fact.
- Prints the response.

🏃‍♂️ **Run the script**:

```bash
poetry run python 04_cluster_execution/01_test_interactive.py
```

✅ **Expected output:**

```txt
Model response: 'Pride and Prejudice' was written by Jane Austen.
```

> 🗒️ **Note**:
> Make sure you stop the Ollama server after running the script:
>
> ```bash
> fg # to bring the Ollama server to the foreground
> Ctrl+C # to stop the server
> ```
>
> This ensures the server is properly shut down and frees up resources.

---

## 3. 🧾 Batch Job Submission

</> **See the script** [`run_batch.sh`](./run_batch.sh) that does the following:

1. Starts the Ollama server.
2. Handles retries if the server is not ready.
3. Runs the LLM extraction script.

🚀 **Submit the job**:

```bash
export LOG_DIR=$HOME/llm-information-extraction-workshop/log
mkdir -p $LOG_DIR

sbatch \
    -o $LOG_DIR/slurm.out \
    -e $LOG_DIR/slurm.err \
    04_cluster_execution/run_batch.sh
```

> 🗒️ **Note**:
> You can pass SBATCH options directly to `sbatch` to parameterize your job with variables and pass arguments to the script.

🔍 **Monitor job Status**:

```bash
squeue
```

You can also check the output files generated by the job:

```bash
cat $LOG_DIR/slurm.out
```

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
