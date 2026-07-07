from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class BoardEvaluation:
    score: float
    components: Dict[str, float]


class BoardEvaluator:
    def evaluate(self, state: Dict[str, Any]) -> BoardEvaluation:
        my_prizes = state.get('my_prizes_left', 6)
        opp_prizes = state.get('opp_prizes_left', 6)
        my_hp = state.get('my_active_hp', 0)
        opp_hp = state.get('opp_active_hp', 0)
        my_hand = len(state.get('my_hand', []))
        my_bench = len(state.get('my_bench', []))
        opp_bench = len(state.get('opp_bench', []))

        components = {
            'prize_race': (opp_prizes - my_prizes) * 20,
            'active_hp_advantage': (my_hp - opp_hp) * 0.10,
            'hand_quality_proxy': my_hand * 2,
            'board_development': my_bench * 3,
            'opponent_board_pressure': -opp_bench * 1,
        }

        return BoardEvaluation(
            score=sum(components.values()),
            components=components,
        )
