#!/bin/bash
#SBATCH --job-name=BA_transcribe  # Kurzname des Jobs
#SBATCH --nodes=1                 # Anzahl benötigter Knoten
#SBATCH --ntasks=1                # Gesamtzahl der Tasks über alle Knoten hinweg
#SBATCH --partition=p2            # Verwendete Partition (z.B. p0, p1, p2 oder all)
#SBATCH --time=16:00:00           # Gesamtlimit für Laufzeit des Jobs (Format: HH:MM:SS)
#SBATCH --cpus-per-task=8         # Rechenkerne pro Task
#SBATCH --mem=48G                 # Gesamter Hauptspeicher pro Knoten
#SBATCH --gres=gpu:1              # Gesamtzahl GPUs pro Knoten
#SBATCH --qos=basic               # Quality-of-Service
#SBATCH --mail-type=ALL           # Art des Mailversands (gültige Werte z.B. ALL, BEGIN, END, FAIL oder REQUEUE)
#SBATCH --mail-user=neumannvi84434@th-nuernberg.de # Emailadresse für Statusmails
#SBATCH --output=/home/neumannvi84434/Bachelorarbeit/Bachelorarbeit/logs/slurm-%j.out

echo "=================================================================="
echo "Starting Batch Job at $(date)"
echo "Job submitted to partition ${SLURM_JOB_PARTITION} on ${SLURM_CLUSTER_NAME}"
echo "Job name: ${SLURM_JOB_NAME}, Job ID: ${SLURM_JOB_ID}"
echo "Requested ${SLURM_CPUS_ON_NODE} CPUs on compute node $(hostname)"
echo "Working directory: $(pwd)"
echo "=================================================================="

###################### Optional for Pythonnutzer*innen #######################
# Die folgenden Umgebungsvariablen stellen sicher, dass
# Modellgewichte von Huggingface und PIP Packages nicht unter 
# /home/$USER/.cache landen. 
CACHE_DIR=/nfs/scratch/students/$USER/.cache
export PIP_CACHE_DIR=$CACHE_DIR
export TRANSFORMERS_CACHE=$CACHE_DIR
export HF_HOME=$CACHE_DIR
mkdir -p CACHE_DIR

# Load necessary modules
# module load cuda/11.0  # Load the CUDA module if needed
# module load python/3.8  # Load the Python module if needed

# Activate your Python environment (if using one)
source /home/neumannvi84434/Bachelorarbeit/Bachelorarbeit/.venv/bin/activate

export PYTHONPATH=/home/neumannvi84434/Bachelorarbeit/Bachelorarbeit/scripts

########################################################

############### Starte eigenen Job hier ################
# Navigate to your script's directory
cd /home/neumannvi84434/Bachelorarbeit/Bachelorarbeit/scripts

# Run your script with any necessary arguments
python audio_transcription/transcribe_all_audios.py
########################################################


################ deactivieren des venv #################
# source deactivate 
########################################################
