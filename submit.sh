#!/bin/bash
#SBATCH --partition=cpu-long
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=32
#SBATCH --time=48:00:00

dvc repro
