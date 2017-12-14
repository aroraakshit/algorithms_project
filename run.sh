#!/bin/bash
#SBATCH --nodes=10
#SBATCH --partition=shas
#SBATCH --output=/projects/akar9135/algos/output.txt
module load gcc
module load python/3.5.1
source activate /projects/akar9135/test
python MiniMaxAlgorithm.py
source deactivate