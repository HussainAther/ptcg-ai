# Twinleaf Integration Plan

## Goal

Use Twinleaf as a reference implementation for faithful Pokemon TCG rules while keeping this repository focused on AI planning, evaluation, and strategy.

## Why

A faithful Pokemon TCG simulator is difficult because card-specific effects, timing rules, replacement effects, game phases, hidden information, and edge cases are extremely complex. Rather than reimplement every rule immediately, this project treats Twinleaf as a reference engine.

## Integration Strategy

1. Study `ptcg-server` game-state representation.
2. Identify how legal actions are represented.
3. Identify how card effects are implemented.
4. Export game states and legal actions into a neutral JSON schema.
5. Feed that JSON into this repo's planners.
6. Return selected actions back to the engine.

## Proposed Boundary

Twinleaf handles:
- legal move generation
- rules enforcement
- card effects
- turn phases
- game-state mutation

This project handles:
- card knowledge graph
- board evaluation
- heuristic planning
- MCTS
- future neural value estimation
- move explanation

## Ideal API

Input:

```json
{
  "game_state": {},
  "legal_actions": [],
  "history": []
}