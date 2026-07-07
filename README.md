# PTCG AI Battle Strategy

This repo is for the Kaggle Pokemon TCG AI Battle Challenge Strategy competition.

## Core Strategy

Build a hybrid Pokemon TCG agent using:

1. Rule-safe heuristic policy
2. Game-state featurization
3. Monte Carlo rollout search
4. Learned value estimation
5. Opponent/deck archetype belief tracking

## Why this makes sense

Pokemon TCG involves hidden information, stochastic draws, branching tactical choices, and long-horizon planning. A strong agent should combine fast heuristics with simulation and learned evaluation.

## Current Files

- src/check_gpu.py: verifies CUDA/GPU
- src/strategy_skeleton.py: starter heuristic agent
- notebooks/: exploration notebooks
- data/: local datasets, ignored by git
- models/: saved models, ignored by git
- outputs/: generated results, ignored by git
