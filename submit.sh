#!/bin/bash
#SBATCH --partition=gpu
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=32
#SBATCH --time=06:00:00
#SBATCH --gres=gpu:1

dvc repro
