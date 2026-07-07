# PTCG AI Battle Strategy Draft

## Thesis

A strong Pokemon TCG agent should not rely on a single model. The game combines hidden information, random draws, evolving board states, resource sequencing, prize-race pressure, and opponent adaptation. My proposed agent uses a hybrid architecture:

1. Card knowledge base
2. Strategic card tagging
3. Board-state encoding
4. Legal action generation
5. Heuristic action evaluation
6. Search/planning
7. Learned value estimation as a later upgrade

## Card Knowledge Layer

The English card database contains 2,022 card rows. The card pool is mostly Pokemon, with 958 Basic Pokemon, 618 Stage 1 Pokemon, and 229 Stage 2 Pokemon. The database also includes Item, Supporter, Pokemon Tool, Stadium, Special Energy, and Basic Energy rows.

The rule labels include 270 Pokemon ex, 54 Mega Pokemon ex, and 29 ACE SPEC cards. This matters because the agent must understand high-value threats, high-risk prizes, and unique card constraints.

## Strategic Tags

Initial keyword mining shows that the most common strategic concepts are damage, energy, bench interaction, discard, attach effects, search, switching, healing, and evolution. These are converted into reusable strategic tags:

- damage_pressure
- bench_pressure
- draw_engine
- deck_search
- energy_acceleration
- discard_synergy
- switching_mobility
- healing_sustain
- status_control
- evolution_support
- hand_disruption
- damage_prevention

These tags let the agent reason about card function instead of only card names.

## State Encoding

The agent converts the board into numeric and symbolic features:

- prize cards remaining
- active Pokemon HP
- bench size
- hand size
- estimated opponent hand size
- turn number
- available actions
- known card tags in hand, discard, board, and deck

This representation supports both heuristic scoring and later machine learning models.

## Action Evaluation

The first policy is intentionally simple and safe. It rewards actions that:

- advance the prize race
- develop energy
- improve draw/search consistency
- preserve damaged attackers
- improve board position
- set up future knockouts

This creates an interpretable baseline before adding search or neural models.

## Planning Upgrade

The next layer is limited-depth search or Monte Carlo Tree Search. Instead of choosing only the best immediate action, the agent simulates likely continuations:

current action -> opponent response -> next draw -> board evaluation

This is useful because Pokemon TCG rewards sequencing. A move that looks weaker now may create a stronger knockout, evolution, or energy line next turn.

## Final Architecture

Game State
-> State Encoder
-> Legal Action Generator
-> Action Evaluator
-> Planner/Search
-> Chosen Action

The system starts with transparent heuristics and can later plug in learned value functions trained from simulated games or expert game logs.
