# PTCG AI
### Engine-Agnostic Pokémon TCG AI Research Framework

A research framework for developing competitive AI agents for the Pokémon Trading Card Game.

Originally created for the **Kaggle Pokémon TCG AI Battle Challenge Strategy** competition, this project has evolved into a modular architecture for game AI research. The framework separates **game rules** from **decision making**, allowing planners and learning algorithms to work with different Pokémon TCG engines through adapter interfaces.

---

# Project Goals

Build a competitive Pokémon TCG AI by combining:

- Knowledge-based reasoning
- Heuristic planning
- Monte Carlo Tree Search (MCTS)
- Learned value networks
- Engine-independent state representations

The long-term goal is to support multiple Pokémon TCG simulators without changing the AI algorithms.

---

# Architecture

```
                Pokémon TCG Engine
             (Twinleaf / Future Engines)
                       │
                       ▼
              Serialized Game State
                       │
                       ▼
                Twinleaf Adapter
                       │
                       ▼
              NeutralGameState
              + LegalAction API
                       │
        ┌──────────────┼──────────────┐
        ▼              ▼              ▼
   Heuristic      Lookahead        MCTS
    Planner        Planner         Search
        └──────────────┼──────────────┘
                       ▼
                Value Network
                 (future work)
                       ▼
               Selected Legal Action
                       ▼
                Engine Action Payload
                       ▼
                Rules Engine Executes
```

The engine remains the **rules authority** while the Python framework focuses entirely on planning and learning.

---

# Current Features

## Knowledge Layer

- Card database
- Strategic keyword mining
- Card tagging
- Card knowledge graph

## Simulation

- Neutral game-state representation
- Player/Pokémon abstractions
- State encoder
- Lightweight simulator

## Planning

- Heuristic planner
- Lookahead planner
- Neutral action planner
- Modular planning interfaces

## Evaluation

- Board evaluator
- Prize race evaluation
- Board development heuristics

## Engine Integration

- Engine adapter interface
- Twinleaf adapter prototype
- Neutral action abstraction
- Twinleaf-compatible action payload generation

---

# Repository Structure

```
src/
    adapters/
    evaluation/
    interfaces/
    knowledge/
    planner/
    simulation/
    utils/

tests/
docs/
fixtures/
outputs/
```

---

# Running

Run the demonstration:

```bash
python -m src.run_framework_demo
```

Run the Twinleaf adapter prototype:

```bash
python -m src.adapters.run_twinleaf_adapter_demo
```

Run all tests:

```bash
pytest
```

---

# Design Philosophy

Instead of implementing thousands of Pokémon card rules in Python, this project treats an external simulator (currently Twinleaf) as the **rules engine**.

The AI operates only on:

- game state
- legal actions
- action outcomes

This separation allows planners and future neural models to remain independent of any specific simulator.

---

# Roadmap

## Near Term

- Improve board evaluation
- Stronger heuristic planner
- Full MCTS implementation
- Richer state encoding
- Better card synergy modeling

## Mid Term

- Self-play framework
- Neural value network (PyTorch)
- Policy learning
- Deck archetype recognition
- Opponent belief modeling

## Long Term

- Twinleaf live integration
- Engine-independent AI interface
- Reinforcement learning
- Large-scale self-play training
- Competitive Pokémon TCG agent

---

# Competition

Built for:

**Kaggle — Pokémon TCG AI Battle Challenge Strategy**

---

# License

MIT License
