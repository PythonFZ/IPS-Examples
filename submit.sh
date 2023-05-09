#!/bin/bash
#SBATCH --partition=gpu
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=64
#SBATCH --time=20:00:00

dvc repro
