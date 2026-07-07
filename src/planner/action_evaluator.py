from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class ActionEvaluation:
    action: Any
    score: float
    reason: str


class ActionEvaluator:
    def evaluate(self, state: Dict[str, Any], action: Any) -> ActionEvaluation:
        action_text = str(action).lower()
        score = 0.0
        reasons = []

        if 'attack' in action_text:
            score += 10
            reasons.append('advances prize race')

        if 'attach' in action_text or 'energy' in action_text:
            score += 5
            reasons.append('develops future attacks')

        if 'supporter' in action_text or 'item' in action_text:
            score += 4
            reasons.append('improves consistency')

        if 'retreat' in action_text:
            score += 2
            reasons.append('improves board position')

        if state.get('opp_active_hp', 999) <= 60 and 'attack' in action_text:
            score += 8
            reasons.append('potential knockout')

        if state.get('my_active_hp', 999) <= 40 and 'retreat' in action_text:
            score += 6
            reasons.append('preserves attacker')

        return ActionEvaluation(
            action=action,
            score=score,
            reason=', '.join(reasons) or 'neutral'
        )
