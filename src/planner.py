from typing import Any, Dict
from action_generator import ActionGenerator
from action_evaluator import ActionEvaluator


class HeuristicPlanner:
    def __init__(self):
        self.generator = ActionGenerator()
        self.evaluator = ActionEvaluator()

    def choose_action(self, state: Dict[str, Any]) -> Any:
        actions = self.generator.legal_actions(state)
        scored = [self.evaluator.evaluate(state, action) for action in actions]
        scored.sort(key=lambda x: x.score, reverse=True)
        return scored[0]

    def explain_policy(self) -> str:
        return (
            'The planner generates legal actions, scores each action using tempo, '
            'resource development, prize pressure, survivability, and consistency, '
            'then selects the highest-scoring action.'
        )
