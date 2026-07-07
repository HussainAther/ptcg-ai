from dataclasses import dataclass
from typing import Any, Dict, List
import random


@dataclass
class ActionScore:
    action: Any
    score: float
    reason: str


class PTCGHeuristicAgent:
    def __init__(self, seed: int = 42):
        self.rng = random.Random(seed)

    def featurize_state(self, state: Dict[str, Any]) -> Dict[str, float]:
        return {
            'my_prizes_left': state.get('my_prizes_left', 6),
            'opp_prizes_left': state.get('opp_prizes_left', 6),
            'my_hand_size': len(state.get('my_hand', [])),
            'opp_hand_size_est': state.get('opp_hand_size', 0),
            'my_active_hp': state.get('my_active_hp', 0),
            'opp_active_hp': state.get('opp_active_hp', 0),
        }

    def score_action(self, state: Dict[str, Any], action: Any) -> ActionScore:
        text = str(action).lower()
        score = 0.0
        reasons = []

        if 'attack' in text:
            score += 10
            reasons.append('advances win condition')

        if 'draw' in text or 'search' in text:
            score += 5
            reasons.append('improves options')

        if 'attach' in text or 'energy' in text:
            score += 4
            reasons.append('builds future attack potential')

        if 'retreat' in text or 'switch' in text:
            score += 2
            reasons.append('improves board position')

        if 'discard' in text:
            score -= 1
            reasons.append('resource cost')

        score += self.rng.uniform(-0.1, 0.1)

        return ActionScore(
            action=action,
            score=score,
            reason=', '.join(reasons) or 'neutral'
        )

    def choose_action(self, state: Dict[str, Any], legal_actions: List[Any]) -> Any:
        if not legal_actions:
            return None

        scored = [self.score_action(state, action) for action in legal_actions]
        scored.sort(key=lambda x: x.score, reverse=True)
        return scored[0].action


if __name__ == '__main__':
    agent = PTCGHeuristicAgent()

    dummy_state = {
        'my_prizes_left': 5,
        'opp_prizes_left': 6,
        'my_hand': ['Professor Research', 'Energy', 'Nest Ball'],
        'opp_hand_size': 4,
        'my_active_hp': 120,
        'opp_active_hp': 80,
    }

    legal_actions = [
        'attack with active Pokemon',
        'draw cards',
        'attach energy',
        'retreat',
        'discard card',
    ]

    print('Chosen action:', agent.choose_action(dummy_state, legal_actions))
