# LLM Information Extraction Workshop

Hands-on training on extracting structured information with LLMs.
The objective is to learn how to run LLMs locally using **Ollama**, how to extract structured information from LLM responses, and how to run remote LLM jobs on the **CESGA FinisTerrae III cluster**.

---

## 🎯 Learning Outcomes

By the end of this workshop, you will:

- Run and interact with LLMs locally using Ollama.
- Design prompts to extract structured information.
- Parse and validate LLM responses.
- Run and monitor batch jobs on the CESGA FinisTerrae III cluster.

---

## 📋 Prerequisites

- Basic knowledge of Python programming.
- Familiarity with command line operations.
- A CESGA FinisTerrae III account (if you want to run jobs on the cluster).

---

## 📖 Course Modules

### 🛠️ **Module 1 – Setup & Environment**

- **Goal:** Get ready to run LLMs locally and access the CESGA FinisTerrae III cluster.
- **Contents:**
  - Install and test Ollama (local LLM server).
  - Check available models and run LLM from CLI.
  - Set up Python 3.10+ and Poetry for dependency management.
  - Install the Ollama Python library and verify with a test script.
  - Ensure SSH access to the CESGA cluster and configure SSH for convenience.
- **Module Link:** [➡ 01_setup/](01_setup/)

### 💻 **Module 2 – Local LLM Jobs (Basics)**

- **Goal:** Learn to run basic and batch LLM jobs locally using the Ollama Python client, prompt templates, and file I/O.
- **Contents:**
  - Run a Python script to query the LLM and print the response.
  - Use a prompt template to batch-query book info from a file and save results.
- **Module Link:** [➡ 02_local_llm_jobs/](02_local_llm_jobs/)

### 🧩 **Module 3 – Output Parsing (Advanced)**

- **Goal:** Extract structured information from book reviews using manual JSON parsing and Pydantic validation.
- **Contents:**
  - Prompt LLMs for explicit JSON and parse with `json.loads()`.
  - Use Pydantic models to validate and structure single review outputs.
  - Batch process multiple reviews, validate, and save results to CSV.
- **Module Link:** [➡ 03_advanced_llm_jobs/](03_advanced_llm_jobs/)

### 🖥️ **Module 4 – CESGA FinisTerrae III Cluster Execution**

- **Goal:** Run LLM extraction scripts on CESGA FinisTerrae III, both interactively and as batch jobs, using the `qwen2.5` model to process reviews and save outputs.
- **Contents:**
  - Clone the repository and set up storage for Ollama and Poetry.
  - Load required modules and verify environment.
  - Start an interactive GPU session, launch Ollama, and test with a sample script.
  - Submit batch jobs using SLURM and monitor results.
- **Module Link:** [➡ 04_cluster_execution/](04_cluster_execution/)

---

## 📂 Repository Structure

```txt
01_setup/                → Environment setup & cluster access guides
02_local_llm_jobs/       → Basic & advanced local scripts (prompt templates, parsing)
03_advanced_llm_jobs/    → Advanced local jobs with structured output parsing
04_cluster_execution/    → Running and monitoring batch jobs on the CESGA cluster
data/                    → Sample texts & expected outputs
```
