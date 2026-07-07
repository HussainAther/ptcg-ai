# Architecture

Twinleaf / Rules Engine
-> Serialized state + legal actions
-> TwinleafAdapter
-> NeutralGameState + LegalAction
-> NeutralActionPlanner / MCTS / Value Network
-> Selected LegalAction
-> Twinleaf-compatible action payload