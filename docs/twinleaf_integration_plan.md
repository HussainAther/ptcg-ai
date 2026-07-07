# Twinleaf Integration Plan

Twinleaf remains the rules engine. This repo provides the AI planner.

## Boundary

Twinleaf handles:
- legal actions
- card effects
- rule enforcement
- state transitions
- prompts and serialization

This repo handles:
- neutral state representation
- card knowledge graph
- board evaluation
- heuristic planning
- lookahead
- MCTS
- future value network

## Adapter Flow

Twinleaf serialized state
-> TwinleafAdapter
-> NeutralGameState
-> Planner
-> LegalAction
-> Twinleaf action payload

## Next Implementation Goal

Find Twinleaf's state serializer and action payload format, then map real Twinleaf JSON into `NeutralGameState`.