import math
import random
from copy import deepcopy
from dataclasses import dataclass, field
from typing import Any, Dict, Optional

from src.planner.action_generator import ActionGenerator
from src.simulation.simple_simulator import SimpleSimulator
from src.evaluation.board_evaluator import BoardEvaluator


@dataclass
class MCTSNode:
    state: Dict[str, Any]
    parent: Optional["MCTSNode"] = None
    action_taken: Optional[str] = None
    children: list = field(default_factory=list)
    untried_actions: list = field(default_factory=list)
    visits: int = 0
    total_value: float = 0.0

    def value(self) -> float:
        if self.visits == 0:
            return 0.0
        return self.total_value / self.visits

    def uct_score(self, exploration: float = 1.41) -> float:
        if self.visits == 0:
            return float("inf")
        parent_visits = max(1, self.parent.visits if self.parent else 1)
        return self.value() + exploration * math.sqrt(math.log(parent_visits) / self.visits)


class MCTSPlanner:
    def __init__(self, simulations: int = 100, rollout_depth: int = 4, seed: int = 42):
        self.simulations = simulations
        self.rollout_depth = rollout_depth
        self.rng = random.Random(seed)
        self.generator = ActionGenerator()
        self.simulator = SimpleSimulator()
        self.evaluator = BoardEvaluator()

    def choose_action(self, state: Dict[str, Any]) -> Dict[str, Any]:
        root = MCTSNode(
            state=deepcopy(state),
            untried_actions=self.generator.legal_actions(state),
        )

        for _ in range(self.simulations):
            node = self._select(root)
            value = self._rollout(deepcopy(node.state))
            self._backpropagate(node, value)

        best_child = max(root.children, key=lambda child: child.visits, default=None)

        if best_child is None:
            return {
                "action": None,
                "score": 0.0,
                "visits": 0,
                "reason": "no legal actions",
            }

        return {
            "action": best_child.action_taken,
            "score": best_child.value(),
            "visits": best_child.visits,
            "children": [
                {
                    "action": child.action_taken,
                    "visits": child.visits,
                    "value": child.value(),
                }
                for child in sorted(root.children, key=lambda c: c.visits, reverse=True)
            ],
        }

    def _select(self, node: MCTSNode) -> MCTSNode:
        while True:
            if node.untried_actions:
                return self._expand(node)

            if not node.children:
                return node

            node = max(node.children, key=lambda child: child.uct_score())

    def _expand(self, node: MCTSNode) -> MCTSNode:
        action = node.untried_actions.pop(0)
        next_state = self.simulator.step(node.state, action)

        child = MCTSNode(
            state=next_state,
            parent=node,
            action_taken=action,
            untried_actions=self.generator.legal_actions(next_state),
        )

        node.children.append(child)
        return child

    def _rollout(self, state: Dict[str, Any]) -> float:
        for _ in range(self.rollout_depth):
            actions = self.generator.legal_actions(state)
            if not actions:
                break

            action = self.rng.choice(actions)
            state = self.simulator.step(state, action)

        return self.evaluator.evaluate(state).score

    def _backpropagate(self, node: MCTSNode, value: float) -> None:
        while node is not None:
            node.visits += 1
            node.total_value += value
            node = node.parent
