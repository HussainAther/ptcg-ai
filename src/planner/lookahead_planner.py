from typing import Any, Dict
from src.planner.action_generator import ActionGenerator
from src.simulation.simple_simulator import SimpleSimulator
from src.evaluation.board_evaluator import BoardEvaluator


class LookaheadPlanner:
    def __init__(self):
        self.generator = ActionGenerator()
        self.simulator = SimpleSimulator()
        self.evaluator = BoardEvaluator()

    def choose_action(self, state: Dict[str, Any]) -> Any:
        actions = self.generator.legal_actions(state)
        scored = []

        for action in actions:
            next_state = self.simulator.step(state, action)
            eval_result = self.evaluator.evaluate(next_state)
            scored.append((action, eval_result.score, eval_result.components))

        scored.sort(key=lambda x: x[1], reverse=True)

        best_action, best_score, components = scored[0]
        return {
            'action': best_action,
            'score': best_score,
            'components': components,
            'all_scores': scored,
        }
