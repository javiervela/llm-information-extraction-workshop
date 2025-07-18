#!/bin/bash
#----------------------------------------------------
# LLM Extraction Batch Job (CESGA)
#----------------------------------------------------
#SBATCH -J llm_extraction_test
#SBATCH -c 32
#SBATCH --gres=gpu:a100:1
#SBATCH -t 00:30:00
#SBATCH --mem=64G
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=jvela@ipe.csic.es

module load cesga/2022 ollama/0.6.4 python/3.10.8

export OLLAMA_HOST="127.0.0.1:11434"
export OLLAMA_TMPDIR=$TMPDIR
export LOG_DIR=$HOME/llm-information-extraction-workshop/log
export MAX_RETRIES=5

mkdir -p $LOG_DIR

ollama serve >$LOG_DIR/ollama_server.log 2>&1 &

RETRY_COUNT=0
while ! curl -s $OLLAMA_HOST | grep -q "Ollama is running"; do
    echo "Ollama server is not running. Retrying..."
    RETRY_COUNT=$(expr $RETRY_COUNT + 1)
    if [ $RETRY_COUNT -ge $MAX_RETRIES ]; then
        echo "Error: Ollama server is not running after $MAX_RETRIES retries."
        exit 1
    fi
    sleep 1
done

cd $HOME/llm-information-extraction-workshop

poetry run python 04_cluster_execution/01_test_interactive.py