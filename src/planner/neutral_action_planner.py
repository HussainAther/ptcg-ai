from src.interfaces.legal_action import ActionType


class NeutralActionPlanner:
    def score(self, action):
        scores = {
            ActionType.ATTACK: 100,
            ActionType.PLAY_CARD: 60,
            ActionType.ATTACH_ENERGY: 50,
            ActionType.USE_ABILITY: 45,
            ActionType.RETREAT: 20,
            ActionType.END_TURN: 0,
            ActionType.PASS: -10,
        }
        return scores.get(action.action_type, 0)

    def choose(self, actions):
        if not actions:
            return None
        return max(actions, key=self.score)