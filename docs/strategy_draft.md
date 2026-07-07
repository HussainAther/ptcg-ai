# Hybrid Search-and-Knowledge Agent for Pokemon TCG

## Summary

My strategy is to build a hybrid Pokemon TCG agent that combines structured card knowledge, interpretable heuristics, one-step lookahead, and Monte Carlo Tree Search. Pokemon TCG is not just a damage race. It requires planning under hidden information, stochastic draws, evolving board states, once-per-turn rules, resource limits, prize sequencing, and opponent adaptation.

The proposed agent is intentionally modular:

Card database -> strategic tags -> game state -> legal actions -> board evaluator -> planner/search -> selected action

This lets the system begin as a transparent rule-safe baseline, then improve through simulation, self-play, and learned value estimation.

## Data Understanding

The English card database contains 2,022 rows. The card pool includes:

- 958 Basic Pokemon
- 618 Stage 1 Pokemon
- 229 Stage 2 Pokemon
- 82 Item cards
- 61 Supporter cards
- 28 Pokemon Tool cards
- 26 Stadium cards
- 12 Special Energy cards
- 8 Basic Energy cards

The rule labels include 270 Pokemon ex, 54 Mega Pokemon ex, and 29 ACE SPEC cards.

Keyword analysis of effect text shows the most common strategic concepts are damage, energy, bench interaction, discard, deck search, status control, switching, draw, prevention, evolution, and healing. This suggests the agent should reason about tempo, prize pressure, energy development, bench pressure, and consistency rather than simply selecting the highest-damage attack.

## Card Knowledge Layer

Each card is loaded into a structured database with fields such as card ID, name, stage, rule, HP, type, attack name, cost, damage, effect text, and inferred strategic tags.

Current strategic tags include:

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

For example, Greninja ex is recognized as a Stage 2 Pokemon with tags including bench pressure, damage pressure, damage prevention, deck search, discard synergy, and energy acceleration. This lets the agent reason about card function instead of memorizing card names.

## Game-State Representation

The simulator represents both players with:

- deck
- hand
- discard pile
- prize count
- active Pokemon
- bench
- once-per-turn energy attachment flag
- once-per-turn supporter flag

Pokemon in play track HP, attached energy, status conditions, evolution status, and knockout state.

The state encoder converts board state into features such as prize count, active HP, hand size, bench size, estimated opponent hand size, and turn number. This supports both heuristic planning and future neural value models.

## Action Generation

The action generator enumerates legal candidate actions such as:

- attack
- attach energy
- play supporter
- play item
- retreat
- pass

The long-term version would expand these into card-specific legal actions, including attack choices, ability usage, retreat costs, evolution legality, item effects, supporter effects, stadium replacement, and search targets.

## Board Evaluation

The board evaluator scores positions using interpretable components:

- prize race
- active HP advantage
- hand quality proxy
- board development
- opponent board pressure

This is intentionally simple but useful. It separates position evaluation from action choice, which is important because the best action is not always the one with the best immediate effect. The agent should choose the action that leads to the best resulting board state.

## Planning Methods

The current framework supports three planners.

### 1. Heuristic Planner

The heuristic planner directly scores actions using tactical rules. It rewards attacks, energy development, consistency actions, retreat when damaged, and potential knockouts.

### 2. Lookahead Planner

The lookahead planner simulates each candidate action, evaluates the resulting board, and chooses the best next state. This already catches important prize-race logic. For example, after fixing the simulator, the planner correctly prefers an attack that takes a knockout over drawing extra cards.

### 3. Monte Carlo Tree Search

The MCTS planner builds a search tree over actions. Each node tracks visits, total value, average value, and UCT score. It repeatedly selects promising nodes, expands actions, performs rollouts, evaluates final states, and backpropagates values.

This is important because Pokemon TCG rewards sequencing. A strong move might not be the best immediate board score; it may create a stronger future knockout, evolution line, or energy curve.

## Learning Upgrade

The next upgrade is a neural value function trained from simulated games. The current value network skeleton uses PyTorch and can run on an NVIDIA RTX 4070. The learning loop would generate encoded board states through self-play, label them with win/loss or expected value, and train a value network to replace or augment the hand-built board evaluator.

The final decision policy would combine:

- hard legality checks
- card knowledge graph
- heuristic priors
- MCTS rollouts
- neural value estimation

## Why This Strategy Is Strong

This approach is robust because it does not depend on one brittle model. Rule-based logic prevents illegal actions. Strategic tags give the agent card-level understanding. Board evaluation gives interpretability. MCTS handles long-horizon planning. A neural value model can improve performance over time through self-play.

The system also supports clear debugging. In one test case, a one-step lookahead planner initially undervalued a knockout because the simulator reduced the wrong player's prize count. The bug was caught by comparing heuristic and lookahead behavior, then locked with a regression test. This is exactly why a modular, testable architecture matters.

## Current Implementation

The current repository includes:

- card database loader
- strategic tag extractor
- card knowledge graph
- game-state models
- player and Pokemon models
- rules module
- game engine
- board evaluator
- heuristic planner
- lookahead planner
- MCTS planner
- PyTorch value network skeleton
- regression tests for knockout, prize updates, energy attachment, supporter usage, retreat, and MCTS knockout preference

## Limitations

The current simulator is a scaffold, not a full Pokemon TCG engine. It does not yet fully model exact card text, weakness/resistance, retreat costs, abilities, special conditions, evolution timing, prize-card selection, deck search choices, stadium rules, or opponent hidden-information beliefs.

Those are engineering extensions, not architectural blockers. The framework is designed so each of these can be added incrementally while preserving test coverage.

## Conclusion

The best Pokemon TCG AI should combine symbolic rules, card knowledge, search, and learned evaluation. My strategy starts with an interpretable and testable system, then scales toward stronger planning through MCTS and self-play. This gives the agent a practical path from legal baseline play to adaptive, long-horizon competitive decision-making.
